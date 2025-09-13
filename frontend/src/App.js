import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, Zap, Shield, BarChart, ChevronRight, Sparkles, Image as ImageIcon, User, Shirt } from "lucide-react";
import axios from "axios";
import { useDropzone } from "react-dropzone";
import "./App.css";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Landing Page Component
const LandingPage = () => {
  const navigate = useNavigate();
  
  const features = [
    {
      icon: <Zap className="w-8 h-8 text-purple-400" />,
      title: "Lightning Fast",
      description: "Get try-on results in under 3 seconds with our optimized AI pipeline"
    },
    {
      icon: <Shield className="w-8 h-8 text-blue-400" />,
      title: "Enterprise Ready",
      description: "SOC2 compliant with advanced security and privacy controls"
    },
    {
      icon: <BarChart className="w-8 h-8 text-green-400" />,
      title: "Analytics Dashboard",
      description: "Track usage, performance metrics, and user engagement in real-time"
    }
  ];

  const testimonials = [
    {
      name: "Sarah Chen",
      role: "Fashion Director",
      company: "StyleCorp",
      text: "TryOn.fit transformed our customer experience. 40% increase in conversions!"
    },
    {
      name: "Marcus Rodriguez",
      role: "CTO",
      company: "FashionTech",
      text: "The SDK integration was seamless. Up and running in less than 30 minutes."
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900">
      {/* Navigation */}
      <nav className="flex justify-between items-center p-6 backdrop-blur-sm bg-black/20">
        <div className="text-2xl font-bold text-white flex items-center">
          <Sparkles className="w-8 h-8 mr-2 text-purple-400" />
          TryOn.fit
        </div>
        <div className="flex space-x-6">
          <Link to="/app" className="text-purple-300 hover:text-white transition-colors">
            Try Demo
          </Link>
          <button className="bg-purple-600 hover:bg-purple-700 px-6 py-2 rounded-full text-white transition-colors">
            Get Started
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <motion.section 
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center py-20 px-6"
      >
        <h1 className="text-6xl font-bold text-white mb-6 leading-tight">
          Virtual Try-On
          <span className="block text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400">
            For Fashion Brands
          </span>
        </h1>
        <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
          Integrate photorealistic virtual try-on into your e-commerce platform with just one line of code. 
          Boost conversions and reduce returns with AI-powered fashion visualization.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button 
            onClick={() => navigate('/app')}
            className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 px-8 py-4 rounded-full text-white font-semibold text-lg transition-all transform hover:scale-105 flex items-center justify-center"
          >
            Try Live Demo <ChevronRight className="ml-2 w-5 h-5" />
          </button>
          <button className="border-2 border-purple-400 text-purple-300 hover:bg-purple-400 hover:text-white px-8 py-4 rounded-full font-semibold text-lg transition-all">
            View Documentation
          </button>
        </div>
      </motion.section>

      {/* Features Section */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-white text-center mb-16">
            Why Choose TryOn.fit?
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 text-center hover:bg-white/15 transition-all"
              >
                <div className="flex justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-white mb-4">{feature.title}</h3>
                <p className="text-gray-300">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Integration Preview */}
      <section className="py-20 px-6 bg-black/20">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-8">
            Integrate in Minutes
          </h2>
          <div className="bg-gray-900 rounded-2xl p-8 text-left">
            <div className="text-green-400 mb-2">// Initialize TryOn SDK</div>
            <div className="text-blue-400">TryOn<span className="text-white">.</span><span className="text-yellow-400">init</span><span className="text-white">({</span></div>
            <div className="ml-4 text-white">clientId<span className="text-gray-400">:</span> <span className="text-green-400">'your-client-id'</span><span className="text-white">,</span></div>
            <div className="ml-4 text-white">env<span className="text-gray-400">:</span> <span className="text-green-400">'production'</span></div>
            <div className="text-white">});</div>
            <div className="mt-4 text-green-400">// Open try-on for any product</div>
            <div className="text-blue-400">TryOn<span className="text-white">.</span><span className="text-yellow-400">open</span><span className="text-white">({</span></div>
            <div className="ml-4 text-white">productId<span className="text-gray-400">:</span> <span className="text-green-400">'SKU_1234'</span></div>
            <div className="text-white">});</div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-white text-center mb-16">
            Trusted by Fashion Leaders
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
                className="bg-white/10 backdrop-blur-sm rounded-2xl p-8"
              >
                <p className="text-gray-300 mb-6 text-lg italic">"{testimonial.text}"</p>
                <div>
                  <div className="font-semibold text-white">{testimonial.name}</div>
                  <div className="text-purple-400">{testimonial.role} at {testimonial.company}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Transform Your Fashion Business?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Join hundreds of fashion brands already using TryOn.fit to increase conversions and delight customers.
          </p>
          <button 
            onClick={() => navigate('/app')}
            className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 px-12 py-4 rounded-full text-white font-bold text-xl transition-all transform hover:scale-105"
          >
            Start Your Free Trial
          </button>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="bg-black/30 py-12 px-6">
        <div className="max-w-6xl mx-auto text-center">
          <div className="text-2xl font-bold text-white mb-4 flex items-center justify-center">
            <Sparkles className="w-6 h-6 mr-2 text-purple-400" />
            TryOn.fit
          </div>
          <p className="text-gray-400">
            © 2025 TryOn.fit. Transforming fashion with AI-powered virtual try-on technology.
          </p>
        </div>
      </footer>
    </div>
  );
};

// Try-On App Component
const TryOnApp = () => {
  const [personImage, setPersonImage] = useState(null);
  const [clothingImage, setClothingImage] = useState(null);
  const [personImagePreview, setPersonImagePreview] = useState(null);
  const [clothingImagePreview, setClothingImagePreview] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [error, setError] = useState(null);
  const [generationProgress, setGenerationProgress] = useState('');

  const convertToBase64 = (file) => {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.readAsDataURL(file);
    });
  };

  const handleImageUpload = async (files, type) => {
    if (files.length > 0) {
      const file = files[0];
      const base64 = await convertToBase64(file);
      
      if (type === 'person') {
        setPersonImage(base64);
        setPersonImagePreview(base64);
      } else {
        setClothingImage(base64);
        setClothingImagePreview(base64);
      }
    }
  };

  const PersonDropzone = useDropzone({
    accept: { 'image/*': [] },
    onDrop: (files) => handleImageUpload(files, 'person'),
    multiple: false
  });

  const ClothingDropzone = useDropzone({
    accept: { 'image/*': [] },
    onDrop: (files) => handleImageUpload(files, 'clothing'),
    multiple: false
  });

  const generateTryOn = async () => {
    if (!personImage || !clothingImage) {
      setError('Please upload both person and clothing images');
      return;
    }

    setIsGenerating(true);
    setError(null);
    setGenerationProgress('Initializing try-on process...');

    try {
      setGenerationProgress('Preprocessing images...');
      
      const response = await axios.post(`${API}/tryon/jobs`, {
        tenant_id: 'demo_tenant',
        person_image: personImage,
        clothing_image: clothingImage,
        options: {
          profile: 'speed',
          maxRes: 1024,
          watermark: false
        }
      });

      setGenerationProgress('Generating try-on result...');
      const result = response.data;
      setJobId(result.job_id);

      if (result.status === 'completed' && result.result_base64) {
        setGeneratedImage(`data:image/png;base64,${result.result_base64}`);
        setGenerationProgress('Try-on completed successfully!');
      } else {
        throw new Error('Failed to generate try-on result');
      }

    } catch (err) {
      console.error('Try-on generation error:', err);
      setError(err.response?.data?.detail || 'Failed to generate try-on. Please try again.');
      setGenerationProgress('');
    } finally {
      setIsGenerating(false);
    }
  };

  const resetApp = () => {
    setPersonImage(null);
    setClothingImage(null);
    setPersonImagePreview(null);
    setClothingImagePreview(null);
    setGeneratedImage(null);
    setJobId(null);
    setError(null);
    setGenerationProgress('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900">
      {/* Navigation */}
      <nav className="flex justify-between items-center p-6 backdrop-blur-sm bg-black/20">
        <Link to="/" className="text-2xl font-bold text-white flex items-center">
          <Sparkles className="w-8 h-8 mr-2 text-purple-400" />
          TryOn.fit
        </Link>
        <button 
          onClick={resetApp}
          className="bg-purple-600 hover:bg-purple-700 px-6 py-2 rounded-full text-white transition-colors"
        >
          New Try-On
        </button>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {!generatedImage ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <h1 className="text-4xl font-bold text-white mb-4">
              Virtual Try-On Demo
            </h1>
            <p className="text-xl text-gray-300 mb-8">
              Upload a person's photo and a clothing item to see the magic happen
            </p>

            {/* Upload Section */}
            <div className="grid md:grid-cols-2 gap-8 mb-8">
              {/* Person Image Upload */}
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-white/10 backdrop-blur-sm rounded-2xl p-8"
              >
                <div className="flex items-center justify-center mb-4">
                  <User className="w-8 h-8 text-purple-400 mr-2" />
                  <h3 className="text-xl font-semibold text-white">Person Photo</h3>
                </div>
                
                <div
                  {...PersonDropzone.getRootProps()}
                  className={`border-2 border-dashed rounded-xl p-8 cursor-pointer transition-all ${
                    PersonDropzone.isDragActive 
                      ? 'border-purple-400 bg-purple-400/10' 
                      : 'border-gray-600 hover:border-purple-400'
                  }`}
                >
                  <input {...PersonDropzone.getInputProps()} />
                  {personImagePreview ? (
                    <img 
                      src={personImagePreview} 
                      alt="Person" 
                      className="w-full h-64 object-cover rounded-lg"
                    />
                  ) : (
                    <div className="text-center">
                      <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-gray-300">Drop person image here or click to upload</p>
                    </div>
                  )}
                </div>
              </motion.div>

              {/* Clothing Image Upload */}
              <motion.div
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
                className="bg-white/10 backdrop-blur-sm rounded-2xl p-8"
              >
                <div className="flex items-center justify-center mb-4">
                  <Shirt className="w-8 h-8 text-blue-400 mr-2" />
                  <h3 className="text-xl font-semibold text-white">Clothing Item</h3>
                </div>
                
                <div
                  {...ClothingDropzone.getRootProps()}
                  className={`border-2 border-dashed rounded-xl p-8 cursor-pointer transition-all ${
                    ClothingDropzone.isDragActive 
                      ? 'border-blue-400 bg-blue-400/10' 
                      : 'border-gray-600 hover:border-blue-400'
                  }`}
                >
                  <input {...ClothingDropzone.getInputProps()} />
                  {clothingImagePreview ? (
                    <img 
                      src={clothingImagePreview} 
                      alt="Clothing" 
                      className="w-full h-64 object-cover rounded-lg"
                    />
                  ) : (
                    <div className="text-center">
                      <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-gray-300">Drop clothing image here or click to upload</p>
                    </div>
                  )}
                </div>
              </motion.div>
            </div>

            {/* Generate Button */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
            >
              <button
                onClick={generateTryOn}
                disabled={!personImage || !clothingImage || isGenerating}
                className={`px-12 py-4 rounded-full text-white font-bold text-xl transition-all transform ${
                  (!personImage || !clothingImage || isGenerating)
                    ? 'bg-gray-600 cursor-not-allowed'
                    : 'bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 hover:scale-105'
                }`}
              >
                {isGenerating ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                    Generating...
                  </div>
                ) : (
                  <div className="flex items-center">
                    <Sparkles className="w-6 h-6 mr-2" />
                    Generate Try-On
                  </div>
                )}
              </button>
            </motion.div>

            {/* Progress/Error Messages */}
            <AnimatePresence>
              {generationProgress && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="mt-6 text-purple-300 text-lg"
                >
                  {generationProgress}
                </motion.div>
              )}
              
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="mt-6 bg-red-500/20 border border-red-500 rounded-lg p-4 text-red-300"
                >
                  {error}
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        ) : (
          /* Results Section */
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center"
          >
            <h1 className="text-4xl font-bold text-white mb-8">
              🎉 Your Virtual Try-On Result
            </h1>
            
            <div className="grid md:grid-cols-3 gap-8 mb-8">
              {/* Original Person */}
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
                <h3 className="text-lg font-semibold text-white mb-4">Original</h3>
                <img 
                  src={personImagePreview} 
                  alt="Original Person" 
                  className="w-full h-80 object-cover rounded-lg"
                />
              </div>

              {/* Try-On Result */}
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center justify-center">
                  <Sparkles className="w-5 h-5 mr-2 text-purple-400" />
                  Try-On Result
                </h3>
                <img 
                  src={generatedImage} 
                  alt="Try-On Result" 
                  className="w-full h-80 object-cover rounded-lg border-2 border-purple-400"
                />
              </div>

              {/* Clothing Item */}
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
                <h3 className="text-lg font-semibold text-white mb-4">Clothing Item</h3>
                <img 
                  src={clothingImagePreview} 
                  alt="Clothing Item" 
                  className="w-full h-80 object-cover rounded-lg"
                />
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={resetApp}
                className="bg-purple-600 hover:bg-purple-700 px-8 py-3 rounded-full text-white font-semibold transition-all"
              >
                Try Another Combination
              </button>
              <button
                onClick={() => {
                  const link = document.createElement('a');
                  link.href = generatedImage;
                  link.download = 'tryon-result.png';
                  link.click();
                }}
                className="border-2 border-purple-400 text-purple-300 hover:bg-purple-400 hover:text-white px-8 py-3 rounded-full font-semibold transition-all"
              >
                Download Result
              </button>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

// Main App Component
const App = () => {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/app" element={<TryOnApp />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;