require('dotenv').config();
const express = require('express');
const multer = require('multer');
const cors = require('cors');
const axios = require('axios');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3005;

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.static('public'));

// File upload config
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, 'uploads');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, uniqueSuffix + '-' + file.originalname);
  }
});

const upload = multer({ 
  storage,
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB limit
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Only image files are allowed'));
    }
  }
});

// Available models configuration
const MODELS = [
  {
    id: 'qwen3.5-plus',
    name: 'Qwen3.5-Plus',
    provider: 'Aliyun',
    vision: true,
    description: 'Balanced performance, supports vision',
    context: '1M tokens',
    price: '¥0.8/M input'
  },
  {
    id: 'qwen3-max-2026-01-23',
    name: 'Qwen3-Max',
    provider: 'Aliyun',
    vision: false,
    description: 'Strongest Qwen model, text only',
    context: '262K tokens',
    price: '¥2.5-7/M input'
  },
  {
    id: 'qwen3-coder-plus',
    name: 'Qwen3-Coder-Plus',
    provider: 'Aliyun',
    vision: false,
    description: 'Code-specialized model',
    context: '1M tokens',
    price: '¥1/M input'
  },
  {
    id: 'glm-5',
    name: 'GLM-5',
    provider: 'Zhipu',
    vision: false,
    description: 'Latest GLM model, text only',
    context: '128K tokens',
    price: 'Competitive'
  },
  {
    id: 'glm-4.7',
    name: 'GLM-4.7',
    provider: 'Zhipu',
    vision: false,
    description: 'Previous GLM version',
    context: '128K tokens',
    price: 'Competitive'
  },
  {
    id: 'kimi-k2.5',
    name: 'Kimi K2.5',
    provider: 'Moonshot AI',
    vision: true,
    description: 'Long context + vision support',
    context: '2M tokens',
    price: 'Competitive'
  },
  {
    id: 'minimax-m2.5',
    name: 'MiniMax-M2.5',
    provider: 'MiniMax',
    vision: false,
    description: 'Multi-modal model (text mode)',
    context: '256K tokens',
    price: 'Competitive'
  }
];

// Aliyun API configuration
const ALIYUN_API_KEY = process.env.ALIYUN_API_KEY;
const ALIYUN_BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1';

// Helper function to encode image to base64
function imageToBase64(filePath) {
  const imageBuffer = fs.readFileSync(filePath);
  return imageBuffer.toString('base64');
}

// Test a single model
async function testModel(modelId, prompt, imagePath = null) {
  const startTime = Date.now();
  
  try {
    const model = MODELS.find(m => m.id === modelId);
    if (!model) {
      throw new Error(`Model ${modelId} not found`);
    }

    // Prepare messages
    let messages = [];
    
    if (imagePath && model.vision) {
      // Vision model with image
      const base64Image = imageToBase64(imagePath);
      const imageExt = path.extname(imagePath).replace('.', '');
      const mimeType = `image/${imageExt === 'jpg' ? 'jpeg' : imageExt}`;
      
      messages = [{
        role: 'user',
        content: [
          {
            type: 'image_url',
            image_url: { url: `data:${mimeType};base64,${base64Image}` }
          },
          {
            type: 'text',
            text: prompt
          }
        ]
      }];
    } else if (imagePath && !model.vision) {
      // Text-only model with image - add note
      messages = [{
        role: 'user',
        content: `${prompt}\n\n[Note: Image was uploaded but this model doesn't support vision]`
      }];
    } else {
      // Text-only
      messages = [{
        role: 'user',
        content: prompt
      }];
    }

    // Call Aliyun API
    const response = await axios.post(
      `${ALIYUN_BASE_URL}/chat/completions`,
      {
        model: modelId,
        messages: messages,
        max_tokens: 2000,
        temperature: 0.7
      },
      {
        headers: {
          'Authorization': `Bearer ${ALIYUN_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 60000
      }
    );

    const endTime = Date.now();
    
    return {
      success: true,
      model: modelId,
      modelName: model.name,
      response: response.data.choices[0].message.content,
      usage: response.data.usage,
      latency: endTime - startTime,
      timestamp: new Date().toISOString()
    };

  } catch (error) {
    const endTime = Date.now();
    return {
      success: false,
      model: modelId,
      modelName: MODELS.find(m => m.id === modelId)?.name || modelId,
      error: error.response?.data?.error?.message || error.message,
      latency: endTime - startTime,
      timestamp: new Date().toISOString()
    };
  }
}

// API Routes

// Get available models
app.get('/api/models', (req, res) => {
  const { vision } = req.query;
  
  let models = MODELS;
  if (vision === 'true') {
    models = models.filter(m => m.vision);
  } else if (vision === 'false') {
    models = models.filter(m => !m.vision);
  }
  
  res.json({ models });
});

// Upload image
app.post('/api/upload', upload.single('image'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No image uploaded' });
  }
  
  res.json({
    success: true,
    filename: req.file.filename,
    path: req.file.path,
    mimetype: req.file.mimetype,
    size: req.file.size
  });
});

// Test single model
app.post('/api/test', upload.single('image'), async (req, res) => {
  const { model, prompt } = req.body;
  
  if (!model) {
    return res.status(400).json({ error: 'Model ID required' });
  }
  
  const testPrompt = prompt || 'Analyze this food image and provide nutritional information including estimated calories, macronutrients (protein, carbs, fat), and key vitamins/minerals.';
  
  const result = await testModel(model, testPrompt, req.file?.path);
  
  res.json(result);
});

// Test multiple models
app.post('/api/test-batch', upload.single('image'), async (req, res) => {
  const { models, prompt } = req.body;
  
  if (!models || !Array.isArray(models) || models.length === 0) {
    return res.status(400).json({ error: 'Models array required' });
  }
  
  const testPrompt = prompt || 'Analyze this food image and provide nutritional information including estimated calories, macronutrients (protein, carbs, fat), and key vitamins/minerals.';
  
  // Test all models in parallel
  const promises = models.map(modelId => testModel(modelId, testPrompt, req.file?.path));
  const results = await Promise.all(promises);
  
  res.json({ results });
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    modelsAvailable: MODELS.length
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Model Tester running at http://localhost:${PORT}`);
  console.log(`📊 Available models: ${MODELS.length}`);
  console.log(`👁️  Vision models: ${MODELS.filter(m => m.vision).length}`);
});
