# Aliyun Model Tester

Test and compare Aliyun Bailian models on food image analysis.

## Features

- 📸 Upload food images for analysis
- 👁️ Auto-filter vision models when image uploaded
- 🧪 Test multiple models in parallel
- 📊 Side-by-side comparison of results
- ⚡ Performance metrics (latency, token usage)
- 🎨 Clean, modern UI

## Setup

### 1. Install Dependencies

```bash
cd model-tester
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Aliyun API key:

```env
ALIYUN_API_KEY=sk-your-api-key-here
PORT=3005
```

### 3. Get Aliyun API Key

1. Go to https://bailian.console.aliyun.com/
2. Navigate to API Key management
3. Create a new API key
4. Copy and paste into `.env`

### 4. Run Locally

```bash
npm start
```

Open http://localhost:3005

## Deployment (Zeabur)

### 1. Push to GitHub

```bash
git add model-tester/
git commit -m "feat: Add Aliyun Model Tester"
git push
```

### 2. Deploy on Zeabur

1. Go to https://zeabur.com
2. Create new project from GitHub repo
3. Select `model-tester` folder
4. Add environment variable: `ALIYUN_API_KEY`
5. Deploy!

### 3. Environment Variables on Zeabur

```
ALIYUN_API_KEY=sk-your-api-key-here
PORT=3005
NODE_ENV=production
```

## Available Models

### Vision Models (for food images)
- ✅ qwen3.5-plus (Aliyun)
- ✅ kimi-k2.5 (Moonshot AI)

### Text-Only Models
- qwen3-max-2026-01-23 (Aliyun)
- qwen3-coder-plus (Aliyun)
- glm-5 (Zhipu)
- glm-4.7 (Zhipu)
- minimax-m2.5 (MiniMax)

## API Endpoints

### GET /api/models
Get available models
```
?vision=true  - Filter vision models only
?vision=false - Filter text-only models
```

### POST /api/upload
Upload image
```
FormData: image (file)
```

### POST /api/test
Test single model
```
FormData: model, prompt, image (optional)
```

### POST /api/test-batch
Test multiple models
```
FormData: models (JSON array), prompt, image (optional)
```

## Usage

1. **Upload Image**: Drag & drop or click to upload food image
2. **Select Models**: Check models to compare (auto-filters to vision models)
3. **Custom Prompt**: Optional - customize analysis prompt
4. **Run Tests**: Click "Run Tests" to analyze with all selected models
5. **Compare Results**: View side-by-side comparison with metrics

## Default Prompt

```
Analyze this food image and provide nutritional information including 
estimated calories, macronutrients (protein, carbs, fat), and key 
vitamins/minerals.
```

## Tech Stack

- **Frontend**: Vanilla HTML/CSS/JS
- **Backend**: Node.js + Express
- **File Upload**: Multer
- **API**: Aliyun Bailian (DashScope)
- **Hosting**: Zeabur (compatible)

## License

MIT
