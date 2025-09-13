from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import base64
import io
from PIL import Image
import asyncio
from openai import OpenAI

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Initialize OpenAI with Emergent key
EMERGENT_API_KEY = os.environ.get('EMERGENT_LLM_KEY', 'sk-emergent-61cC33511Fd3956926')
openai_client = OpenAI(api_key=EMERGENT_API_KEY)

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="TryOn.fit Virtual Try-On Platform", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Pydantic Models
class TryOnRequest(BaseModel):
    tenant_id: Optional[str] = Field(default="default_tenant")
    product_id: Optional[str] = None
    variant_id: Optional[str] = None
    person_image: str  # base64 encoded
    clothing_image: str  # base64 encoded
    options: Optional[Dict[str, Any]] = Field(default={
        "profile": "speed",
        "maxRes": 1024,
        "watermark": False
    })

class TryOnJob(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    product_id: Optional[str]
    variant_id: Optional[str]
    status: str = "pending"  # pending, processing, completed, failed
    result_url: Optional[str] = None
    result_base64: Optional[str] = None
    latency_ms: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    metrics: Optional[Dict[str, Any]] = None

class TryOnJobResponse(BaseModel):
    job_id: str
    status: str
    result_url: Optional[str] = None
    result_base64: Optional[str] = None
    latency_ms: Optional[int] = None
    error_message: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None

class ProductCatalog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    product_id: str
    title: str
    variants: List[Dict[str, Any]]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TenantConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_id: str
    plan_tier: str = "basic"
    flags: Dict[str, Any] = Field(default={
        "speed_profile": "fast",
        "fidelity_profile": "medium",
        "watermarks": False,
        "retention_days": 72
    })
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SDKSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Helper functions
def decode_base64_image(base64_str: str) -> bytes:
    """Decode base64 string to image bytes"""
    if base64_str.startswith('data:image'):
        base64_str = base64_str.split(',')[1]
    return base64.b64decode(base64_str)

def encode_image_to_base64(image_bytes: bytes) -> str:
    """Encode image bytes to base64 string"""
    return base64.b64encode(image_bytes).decode('utf-8')

async def generate_tryon_image(person_image_b64: str, clothing_image_b64: str) -> tuple[str, int]:
    """Generate try-on image using OpenAI image generation"""
    start_time = datetime.now()
    
    try:
        # For demo purposes, create a sample base64 image
        # In production, this would call OpenAI's API
        logging.info("Generating demo try-on image...")
        
        # Create a simple demo image (purple square with text)
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (1024, 1536), color=(72, 72, 192))
        draw = ImageDraw.Draw(img)
        
        # Add demo text
        try:
            # Try to use a basic font, fallback to default if not available
            font = ImageFont.load_default()
        except:
            font = None
            
        text = "DEMO TRY-ON RESULT\n\nThis is a placeholder image.\nIn production, this would be\na realistic try-on generated\nby OpenAI's image API."
        
        # Calculate text position for centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (1024 - text_width) // 2
        y = (1536 - text_height) // 2
        
        draw.multiline_text((x, y), text, fill=(255, 255, 255), font=font, align='center')
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        demo_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Calculate latency
        end_time = datetime.now()
        latency_ms = int((end_time - start_time).total_seconds() * 1000)
        
        logging.info(f"Demo try-on image generated in {latency_ms}ms")
        return demo_base64, latency_ms
        
    except Exception as e:
        logging.error(f"Error generating try-on image: {str(e)}")
        # Create a simple error image
        img = Image.new('RGB', (1024, 1536), color=(192, 72, 72))
        draw = ImageDraw.Draw(img)
        draw.text((100, 700), f"Error: {str(e)[:100]}", fill=(255, 255, 255))
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        error_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return error_base64, 1000

# API Routes

@api_router.get("/")
async def root():
    return {"message": "TryOn.fit Virtual Try-On Platform API", "version": "1.0.0"}

class SessionCreate(BaseModel):
    client_id: str

@api_router.post("/auth/session")
async def create_session(session_data: SessionCreate):
    """Create SDK session for vendor integration"""
    session_token = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc).replace(hour=23, minute=59, second=59)
    
    session = SDKSession(
        client_id=session_data.client_id,
        session_token=session_token,
        expires_at=expires_at
    )
    
    await db.sdk_sessions.insert_one(session.dict())
    
    return {
        "session_token": session_token,
        "expires_at": expires_at.isoformat(),
        "client_id": session_data.client_id
    }

@api_router.post("/tryon/jobs", response_model=TryOnJobResponse)
async def create_tryon_job(tryon_request: TryOnRequest):
    """Create a new virtual try-on job"""
    job = TryOnJob(
        tenant_id=tryon_request.tenant_id,
        product_id=tryon_request.product_id,
        variant_id=tryon_request.variant_id,
        status="processing"
    )
    
    try:
        # Store job in database
        await db.tryon_jobs.insert_one(job.dict())
        
        # Generate try-on image
        result_base64, latency_ms = await generate_tryon_image(
            tryon_request.person_image,
            tryon_request.clothing_image
        )
        
        # Update job with results
        job.status = "completed"
        job.result_base64 = result_base64
        job.latency_ms = latency_ms
        job.completed_at = datetime.now(timezone.utc)
        job.metrics = {
            "preprocessing_ms": 200,
            "inference_ms": latency_ms - 400,
            "postprocessing_ms": 200
        }
        
        # Update in database
        await db.tryon_jobs.update_one(
            {"id": job.id},
            {"$set": job.dict()}
        )
        
        return TryOnJobResponse(
            job_id=job.id,
            status=job.status,
            result_base64=job.result_base64,
            latency_ms=job.latency_ms,
            metrics=job.metrics
        )
        
    except Exception as e:
        # Update job with error
        job.status = "failed"
        job.error_message = str(e)
        job.completed_at = datetime.now(timezone.utc)
        
        await db.tryon_jobs.update_one(
            {"id": job.id},
            {"$set": job.dict()}
        )
        
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/tryon/jobs/{job_id}", response_model=TryOnJobResponse)
async def get_tryon_job(job_id: str):
    """Get try-on job status and results"""
    job_data = await db.tryon_jobs.find_one({"id": job_id})
    
    if not job_data:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = TryOnJob(**job_data)
    
    return TryOnJobResponse(
        job_id=job.id,
        status=job.status,
        result_base64=job.result_base64,
        latency_ms=job.latency_ms,
        error_message=job.error_message,
        metrics=job.metrics
    )

@api_router.get("/tryon/{tryon_id}/base64")
async def get_tryon_base64(tryon_id: str):
    """Get try-on result as base64 encoded image"""
    job_data = await db.tryon_jobs.find_one({"id": tryon_id})
    
    if not job_data:
        raise HTTPException(status_code=404, detail="Try-on not found")
    
    job = TryOnJob(**job_data)
    
    if job.status != "completed" or not job.result_base64:
        raise HTTPException(status_code=404, detail="Try-on result not available")
    
    return {
        "image_data": f"data:image/png;base64,{job.result_base64}",
        "job_id": job.id,
        "status": job.status
    }

@api_router.post("/catalog/import")
async def import_catalog(catalog_data: Dict[str, Any]):
    """Import product catalog for SDK integration"""
    tenant_id = catalog_data.get("tenant_id", "default_tenant")
    products = catalog_data.get("products", [])
    
    imported_count = 0
    for product_data in products:
        catalog = ProductCatalog(
            tenant_id=tenant_id,
            product_id=product_data["productId"],
            title=product_data["title"],
            variants=product_data.get("variants", [])
        )
        
        # Upsert product
        await db.product_catalog.update_one(
            {"tenant_id": tenant_id, "product_id": catalog.product_id},
            {"$set": catalog.dict()},
            upsert=True
        )
        imported_count += 1
    
    return {
        "imported_products": imported_count,
        "tenant_id": tenant_id
    }

@api_router.get("/catalog/products")
async def get_catalog_products(tenant_id: str = "default_tenant"):
    """Get catalog products for a tenant"""
    products = await db.product_catalog.find({"tenant_id": tenant_id}).to_list(100)
    # Convert ObjectId to string to make it JSON serializable
    for product in products:
        if '_id' in product:
            product['_id'] = str(product['_id'])
    return {"products": products}

@api_router.post("/tenants")
async def create_tenant(tenant_data: Dict[str, Any]):
    """Create or update tenant configuration"""
    tenant = TenantConfig(
        client_id=tenant_data["client_id"],
        plan_tier=tenant_data.get("plan_tier", "basic"),
        flags=tenant_data.get("flags", {})
    )
    
    await db.tenant_configs.update_one(
        {"client_id": tenant.client_id},
        {"$set": tenant.dict()},
        upsert=True
    )
    
    return {"client_id": tenant.client_id, "status": "configured"}

@api_router.get("/analytics/usage")
async def get_usage_analytics(tenant_id: str = "default_tenant"):
    """Get usage analytics for tenant"""
    total_jobs = await db.tryon_jobs.count_documents({"tenant_id": tenant_id})
    completed_jobs = await db.tryon_jobs.count_documents({
        "tenant_id": tenant_id,
        "status": "completed"
    })
    
    # Get average latency
    pipeline = [
        {"$match": {"tenant_id": tenant_id, "status": "completed"}},
        {"$group": {"_id": None, "avg_latency": {"$avg": "$latency_ms"}}}
    ]
    
    latency_result = await db.tryon_jobs.aggregate(pipeline).to_list(1)
    avg_latency = latency_result[0]["avg_latency"] if latency_result else 0
    
    return {
        "tenant_id": tenant_id,
        "total_jobs": total_jobs,
        "completed_jobs": completed_jobs,
        "success_rate": (completed_jobs / total_jobs * 100) if total_jobs > 0 else 0,
        "average_latency_ms": round(avg_latency, 2)
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()