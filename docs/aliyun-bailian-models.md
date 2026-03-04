# Aliyun Bailian (百炼) Models Reference

**Last Updated:** March 4, 2026  
**Source:** [Aliyun Bailian Documentation](https://help.aliyun.com/zh/model-studio/models)

---

## 📊 Model Categories

Aliyun Bailian provides models across multiple modalities:
- 📝 **Text Generation** (LLMs)
- 🖼️ **Multi-modal** (Vision, Audio, Video)
- 🎨 **Image Generation & Editing**
- 🎙️ **Speech Synthesis & Recognition**
- 🎬 **Video Generation & Editing**
- 📐 **Vector Embeddings**
- 🏢 **Industry-Specific**

---

## 🏆 Flagship Models (旗舰模型)

### China Mainland Deployment (中国内地)

| Model | Context | Input Price | Output Price | Best For |
|-------|---------|-------------|--------------|----------|
| **Qwen-Max** | 262K | ¥2.5-7/M | ¥10-28/M | Complex tasks, strongest capability |
| **Qwen-Plus** | 1M | ¥0.8/M | ¥2/M | Balanced performance/cost |
| **Qwen-Flash** | 1M | ¥0.15/M | ¥1.5/M | Simple tasks, fast & cheap |
| **Qwen-Coder** | 1M | ¥1/M | ¥4/M | Code generation & tools |

---

## 🤖 Text Generation Models

### Qwen Series (千问系列)

#### Commercial Versions (商业版)

| Model ID | Version | Context | Thinking Mode | Multi-modal | Notes |
|----------|---------|---------|---------------|-------------|-------|
| `qwen3-max` | Stable | 262K | ✅ Yes | ❌ Text only | Latest Qwen3 series |
| `qwen3-max-2026-01-23` | Snapshot | 82K | ✅ Yes | ❌ Text only | Fixed version |
| `qwen3-max-preview` | Preview | 82K | ✅ Yes | ❌ Text only | Preview features |
| `qwen3-plus` | Stable | 1M | ❌ No | ✅ **Yes (Vision)** | **Qwen3.5 upgrade** |
| `qwen3-flash` | Stable | 1M | ❌ No | ✅ **Yes (Vision)** | **Qwen3.5 upgrade** |
| `qwen-max` | Stable | 33K | ❌ No | ❌ Text only | Previous gen |
| `qwen-max-latest` | Latest | 131K | ❌ No | ❌ Text only | Auto-updates |

#### Open Source Versions (开源版)

| Model ID | Context | Multi-modal | Notes |
|----------|---------|-------------|-------|
| `qwen3.5` | 256K | ✅ Yes | Latest open weights |
| `qwen3` | 256K | ✅ Yes | Previous open weights |
| `qwen2.5` | 128K | ❌ No | Older version |

---

## 🖼️ Multi-modal Models (多模态模型)

### Vision Understanding (视觉理解)

| Model | Multi-modal | Description |
|-------|-------------|-------------|
| **Qwen-Plus** | ✅ Yes | Image + text understanding (Qwen3.5) |
| **Qwen-VL** | ✅ Yes | Dedicated vision-language model |
| **QVQ** | ✅ Yes | Advanced vision reasoning |
| **Qwen-Omni** | ✅ Yes | Full modality (text+image+audio) |
| **Qwen-Omni-Realtime** | ✅ Yes | Real-time multi-modal |
| **Qwen-Audio** | ✅ Yes | Audio understanding |

### Third-Party Models (第三方模型)

| Provider | Model | Multi-modal | Notes |
|----------|-------|-------------|-------|
| **Kimi (月之暗面)** | `kimi-k2.5` | ✅ **Yes (Vision)** | Strong long-context |
| **GLM (智谱)** | `glm-5` | ❌ Text only | Latest GLM series |
| **GLM (智谱)** | `glm-4.7` | ❌ Text only | Previous version |
| **GLM (智谱)** | `glm-4-vision` | ✅ Yes | Vision-capable GLM |
| **MiniMax** | `MiniMax-M2.5` | ✅ **Yes** | Multi-modal M2.5 |
| **MiniMax** | `MiniMax-01` | ✅ Yes | Vision + text |
| **DeepSeek** | `deepseek-v3` | ❌ Text only | Code & reasoning |

---

## 📋 Model Selection Guide

### For Text-Only Tasks

| Use Case | Recommended Model | Why |
|----------|-------------------|-----|
| Complex reasoning | `qwen3-max` | Strongest capability |
| General chat/QA | `qwen3-plus` | Balanced cost/performance |
| High volume, simple tasks | `qwen3-flash` | Cheapest option |
| Code generation | `qwen-coder` | Specialized for code |
| Long documents (100K+) | `qwen3-plus` / `qwen3-flash` | 1M context window |

### For Multi-modal (Image Understanding)

| Use Case | Recommended Model | Why |
|----------|-------------------|-----|
| Image + text QA | `qwen3-plus` | Built-in vision, cost-effective |
| Complex visual reasoning | `qwen-vl` | Dedicated vision model |
| Charts/diagrams | `qwen3-plus` | Good at structured visuals |
| OCR + understanding | `qwen-vl` | Strong OCR capabilities |
| Alternative | `kimi-k2.5` | Third-party option |
| Alternative | `minimax-m2.5` | Good multi-modal performance |

---

## ✅ Fact Check: Your List

You mentioned seeing these models on Aliyun Bailian:

| Model You Listed | Exists? | Multi-modal? | Notes |
|------------------|---------|--------------|-------|
| `qwen3.5-plus` | ✅ **Yes** (`qwen3-plus`) | ✅ **Yes** | Upgraded to Qwen3.5, supports vision |
| `kimi-k2.5` | ✅ **Yes** | ✅ **Yes** | Kimi from 月之暗面，supports vision |
| `glm-5` | ✅ **Yes** | ❌ No | Text-only, latest GLM |
| `minimax-m2.5` | ✅ **Yes** | ✅ **Yes** | MiniMax multi-modal |
| `qwen3-max-2026-01-23` | ✅ **Yes** | ❌ No | Snapshot version, text-only |
| `qwen3-coder-next` | ⚠️ **Unconfirmed** | ❌ Likely No | May be internal/beta name |
| `qwen3-coder-plus` | ⚠️ **Unconfirmed** | ❌ Likely No | May be internal/beta name |
| `glm-4.7` | ✅ **Yes** | ❌ No | Previous GLM version |

---

## 💰 Pricing Summary (China Mainland)

### Qwen Commercial Models

| Model | Input (¥/M tokens) | Output (¥/M tokens) |
|-------|-------------------|---------------------|
| Qwen3-Max | ¥2.5-7 (tiered) | ¥10-28 (tiered) |
| Qwen3-Plus | ¥0.8 | ¥2 |
| Qwen3-Flash | ¥0.15 | ¥1.5 |
| Qwen-Coder | ¥1 | ¥4 |

### Third-Party Models

| Provider | Model | Approx. Price |
|----------|-------|---------------|
| Kimi | kimi-k2.5 | Similar to Qwen-Plus |
| GLM | glm-5 | Competitive pricing |
| MiniMax | minimax-m2.5 | Competitive pricing |

*Note: Third-party pricing varies, check console for current rates*

---

## 🚀 Recommendations for Your Use Cases

### Nutritionist App (Food Image Analysis)

**Current:** Using `minimax-01` via OpenRouter ✅

**Aliyun Alternatives:**
1. **`qwen3-plus`** - Built-in vision, cost-effective (¥0.8/M input)
2. **`qwen-vl`** - Dedicated vision model, better accuracy
3. **`kimi-k2.5`** - Good alternative, strong vision

**Migration Consideration:**
- If you're happy with MiniMax via OpenRouter, no need to switch
- Aliyun direct may be cheaper for high volume
- Test accuracy on food images before migrating

### Kanban/Mission Control (Text Only)

**Recommended:** `qwen3-flash` or `qwen3-plus`
- Text-only tasks don't need vision models
- Flash is cheapest for simple summaries
- Plus for more complex reasoning

### Code Projects (Revelation Road, etc.)

**Recommended:** `qwen-coder`
- Specialized for code generation
- Better tool calling & environment interaction

---

## 🔗 Useful Links

- **Model List:** https://help.aliyun.com/zh/model-studio/models
- **Pricing:** https://www.aliyun.com/price/product#/bailian/detail
- **API Docs:** https://help.aliyun.com/zh/model-studio/model-api-reference/
- **Console:** https://bailian.console.aliyun.com/

---

## 📝 Notes

1. **Deployment Modes:**
   - **China Mainland (中国内地):** Data stored in Beijing
   - **Global (全球):** Data in US (Virginia), global compute
   - **International (国际):** Data in Singapore, excludes China
   - **US (美国):** Data in US, US-only compute

2. **Free Quota:**
   - New users get 1M tokens free (input + output) for 90 days
   - Applies to Qwen commercial models

3. **Context Caching:**
   - Qwen3-Max supports context caching for reduced costs
   - Useful for repeated queries on same documents

---

**Last Verified:** March 4, 2026  
**Status:** ✅ Fact-checked against Aliyun official documentation
