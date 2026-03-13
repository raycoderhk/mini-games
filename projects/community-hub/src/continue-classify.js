import fs from 'fs';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);

const CATEGORIES = {
  traffic: 'Traffic & Transport',
  restaurant: 'Restaurants & Food',
  doctor: 'Doctors & Medical',
  tech_tip: 'Tech Tips',
  shopping: 'Shopping & Deals',
  service: 'Services',
  community: 'Community & Estate',
  event: 'Events & Activities',
  news: 'News & Articles',
  repair: 'Home Repairs',
  education: 'Education',
  childcare: 'Childcare & Kids',
};

function buildPrompt(messages) {
  return `Classify WhatsApp messages from HK neighborhood group. Return JSON array with: category, useful (true/false), summary (English), entities [], language (zh/en/mixed).

CATEGORIES: ${Object.keys(CATEGORIES).join(', ')}

MESSAGES:
${messages.map((m, i) => `[${i}] [${m.date} ${m.time}] ${m.sender}: ${m.text}`).join('\n')}

Return ONLY JSON array.`;
}

async function classifyBatch(messages, apiKey) {
  const prompt = buildPrompt(messages);
  const response = await fetch('https://coding.dashscope.aliyuncs.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'qwen3.5-plus',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.1,
      max_tokens: 2000
    })
  });
  
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  const data = await response.json();
  const jsonMatch = data.choices[0].message.content.match(/\[[\s\S]*\]/);
  if (!jsonMatch) return null;
  return JSON.parse(jsonMatch[0]);
}

async function continueClassify() {
  const apiKey = process.env.ALIYUN_API_KEY;
  const messages = JSON.parse(fs.readFileSync('./output/parsed_messages.json', 'utf-8'));
  
  // Load existing results
  let results = [];
  if (fs.existsSync('./output/classified_messages.json')) {
    results = JSON.parse(fs.readFileSync('./output/classified_messages.json', 'utf-8'));
  }
  
  const startBatch = Math.floor(results.length / 25);
  console.log(`📊 Existing: ${results.length} messages (${startBatch} batches)`);
  console.log(`🚀 Starting from batch ${startBatch + 1}`);
  
  const BATCH_SIZE = 25;
  
  for (let i = startBatch * BATCH_SIZE; i < messages.length; i += BATCH_SIZE) {
    const batch = messages.slice(i, i + BATCH_SIZE);
    const batchNum = Math.floor(i / BATCH_SIZE) + 1;
    const totalBatches = Math.ceil(messages.length / BATCH_SIZE);
    
    console.log(`\n🔄 Batch ${batchNum}/${totalBatches}...`);
    
    try {
      const batchResults = await classifyBatch(batch, apiKey);
      if (batchResults) {
        for (const result of batchResults) {
          const originalMsg = messages[result.index];
          results.push({
            ...originalMsg,
            category: result.category,
            useful: result.useful,
            summary: result.summary,
            entities: result.entities,
            language: result.language
          });
        }
        
        // Save every 5 batches
        if (batchNum % 5 === 0) {
          fs.writeFileSync('./output/classified_messages.json', JSON.stringify(results, null, 2));
          const useful = results.filter(r => r.useful && r.category);
          fs.writeFileSync('./output/classified_messages_useful.json', JSON.stringify(useful, null, 2));
          console.log(`💾 Saved: ${results.length} total, ${useful.length} useful`);
        }
      }
    } catch (error) {
      console.error(`❌ Batch ${batchNum} failed:`, error.message);
    }
    
    if (i + BATCH_SIZE < messages.length) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  
  // Final save
  fs.writeFileSync('./output/classified_messages.json', JSON.stringify(results, null, 2));
  const useful = results.filter(r => r.useful && r.category);
  fs.writeFileSync('./output/classified_messages_useful.json', JSON.stringify(useful, null, 2));
  console.log(`\n✅ Complete: ${results.length} classified, ${useful.length} useful`);
}

continueClassify();
