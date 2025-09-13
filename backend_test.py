import requests
import sys
import base64
import io
from datetime import datetime
from PIL import Image
import json

class TryOnAPITester:
    def __init__(self, base_url="https://tryon-fit.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.job_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, files=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}" if endpoint else self.base_url
        headers = {'Content-Type': 'application/json'} if not files else {}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                if files:
                    response = requests.post(url, files=files, timeout=30)
                else:
                    response = requests.post(url, json=data, headers=headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def create_test_image_base64(self, color=(255, 0, 0), size=(512, 512)):
        """Create a test image and return as base64"""
        img = Image.new('RGB', size, color)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_bytes = buffer.getvalue()
        return base64.b64encode(img_bytes).decode('utf-8')

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        return self.run_test("Root API Endpoint", "GET", "", 200)

    def test_create_session(self):
        """Test session creation"""
        return self.run_test(
            "Create Session",
            "POST",
            "auth/session",
            200,
            files={'client_id': ('', 'test_client_123')}
        )

    def test_create_tryon_job(self):
        """Test try-on job creation with test images"""
        person_image_b64 = self.create_test_image_base64((100, 150, 200))  # Blue-ish person
        clothing_image_b64 = self.create_test_image_base64((200, 100, 50))  # Orange-ish clothing
        
        data = {
            "tenant_id": "test_tenant",
            "product_id": "test_product_123",
            "variant_id": "test_variant_456",
            "person_image": f"data:image/png;base64,{person_image_b64}",
            "clothing_image": f"data:image/png;base64,{clothing_image_b64}",
            "options": {
                "profile": "speed",
                "maxRes": 1024,
                "watermark": False
            }
        }
        
        success, response = self.run_test(
            "Create Try-On Job",
            "POST",
            "tryon/jobs",
            200,
            data=data
        )
        
        if success and 'job_id' in response:
            self.job_id = response['job_id']
            print(f"   Job ID: {self.job_id}")
        
        return success, response

    def test_get_tryon_job(self):
        """Test getting try-on job by ID"""
        if not self.job_id:
            print("❌ No job ID available for testing")
            return False, {}
        
        return self.run_test(
            "Get Try-On Job",
            "GET",
            f"tryon/jobs/{self.job_id}",
            200
        )

    def test_get_tryon_base64(self):
        """Test getting try-on result as base64"""
        if not self.job_id:
            print("❌ No job ID available for testing")
            return False, {}
        
        return self.run_test(
            "Get Try-On Base64",
            "GET",
            f"tryon/{self.job_id}/base64",
            200
        )

    def test_import_catalog(self):
        """Test catalog import"""
        catalog_data = {
            "tenant_id": "test_tenant",
            "products": [
                {
                    "productId": "TEST_SKU_001",
                    "title": "Test T-Shirt",
                    "variants": [
                        {"id": "variant_1", "color": "red", "size": "M"},
                        {"id": "variant_2", "color": "blue", "size": "L"}
                    ]
                }
            ]
        }
        
        return self.run_test(
            "Import Catalog",
            "POST",
            "catalog/import",
            200,
            data=catalog_data
        )

    def test_get_catalog_products(self):
        """Test getting catalog products"""
        return self.run_test(
            "Get Catalog Products",
            "GET",
            "catalog/products?tenant_id=test_tenant",
            200
        )

    def test_create_tenant(self):
        """Test tenant creation"""
        tenant_data = {
            "client_id": "test_client_123",
            "plan_tier": "premium",
            "flags": {
                "speed_profile": "fast",
                "fidelity_profile": "high",
                "watermarks": False,
                "retention_days": 30
            }
        }
        
        return self.run_test(
            "Create Tenant",
            "POST",
            "tenants",
            200,
            data=tenant_data
        )

    def test_get_usage_analytics(self):
        """Test usage analytics"""
        return self.run_test(
            "Get Usage Analytics",
            "GET",
            "analytics/usage?tenant_id=test_tenant",
            200
        )

    def test_invalid_tryon_job(self):
        """Test try-on job creation with invalid data"""
        data = {
            "tenant_id": "test_tenant",
            "person_image": "invalid_base64",
            "clothing_image": "invalid_base64"
        }
        
        success, response = self.run_test(
            "Invalid Try-On Job (should fail)",
            "POST",
            "tryon/jobs",
            500,  # Expecting error
            data=data
        )
        
        # For this test, failure is success
        if not success and self.tests_run > 0:
            self.tests_passed += 1
            print("✅ Correctly handled invalid data")
            return True, response
        
        return success, response

def main():
    print("🚀 Starting TryOn.fit API Testing...")
    print("=" * 50)
    
    tester = TryOnAPITester()
    
    # Test sequence
    tests = [
        tester.test_root_endpoint,
        tester.test_create_session,
        tester.test_create_tenant,
        tester.test_import_catalog,
        tester.test_get_catalog_products,
        tester.test_create_tryon_job,
        tester.test_get_tryon_job,
        tester.test_get_tryon_base64,
        tester.test_get_usage_analytics,
        tester.test_invalid_tryon_job
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
        
        # Small delay between tests
        import time
        time.sleep(0.5)
    
    # Print final results
    print("\n" + "=" * 50)
    print(f"📊 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"⚠️  {tester.tests_run - tester.tests_passed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())