import fs from 'fs';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);

// Categories for classification
const CATEGORIES = {
  traffic: 'Traffic & Transport (accidents, bus routes, taxi, MTR tips)',
  restaurant: 'Restaurants & Food (recommendations, OpenRice links, deals)',
  doctor: 'Doctors & Medical (clinics, recommendations, health tips)',
  tech_tip: 'Tech Tips (phone plans, apps, gadgets, comparisons)',
  shopping: 'Shopping & Deals (promo codes, coupons, where to buy)',
  service: 'Services (delivery, logistics, repairs, rentals)',
  community: 'Community & Estate (management, facilities, issues)',
  event: 'Events & Activities (BBQ, gatherings, sports, classes)',
  news: 'News & Articles (local news, school info, important updates)',
  repair: 'Home Repairs (plumbers, electricians, AC, locksmith - for 愉城社區)',
  education: 'Education (tutors, schools, courses, materials)',
  childcare: 'Childcare & Kids (toys, schools, activities, parenting tips)',
};

// Classification prompt for LLM
function buildPrompt(messages) {
  return `You are classifying WhatsApp messages from a Hong Kong neighborhood community group (愉景新城/愉城).

CATEGORIES:
${Object.entries(CATEGORIES).map(([key, desc]) => `- ${key}: ${desc}`).join('\n')}

RULES:
1. Only mark as "useful: true" if the message contains actionable information (recommendations, tips, alerts, links to resources)
2. Casual chat, greetings, jokes, opinions without facts → useful: false
3. Extract entity names (businesses, people, places, products)
4. Summarize in English (concise, 1 line)
5. Detect language: "zh" (Chinese), "en" (English), "mixed"

Return a JSON array. Each item:
{
  "index": <original array index>,
  "category": "<one category or null if noise>",
  "useful": true/false,
  "summary": "<English summary, only if useful=true>",
  "entities": ["<extracted names>"],
  "language": "zh" | "en" | "mixed"
}

MESSAGES TO CLASSIFY:
${messages.map((m, i) => `[${i}] [${m.date} ${m.time}] ${m.sender}: ${m.text}`).join('\n')}

Respond with ONLY the JSON array, no other text.`;
}

async function classifyBatch(messages, apiKey) {
  const prompt = buildPrompt(messages);
  
  // Use Aliyun DashScope Coding API (Qwen3.5 model, excellent Chinese support)
  const response = await fetch('https://coding.dashscope.aliyuncs.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'qwen3.5-plus',  // Aliyun Qwen3.5, excellent Chinese/English bilingual
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.1,  // Low temp for consistent classification
      max_tokens: 2000
    })
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
  
  const data = await response.json();
  const content = data.choices[0].message.content;
  
  // Parse JSON from response (sometimes wrapped in markdown)
  const jsonMatch = content.match(/\[[\s\S]*\]/);
  if (!jsonMatch) {
    console.error('Failed to parse JSON from response:', content);
    return null;
  }
  
  return JSON.parse(jsonMatch[0]);
}

async function classifyAll(inputPath, outputPath, apiKey) {
  console.log(`📖 Loading parsed messages from ${inputPath}...`);
  const messages = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));
  
  console.log(`📊 Total messages to classify: ${messages.length}`);
  
  const BATCH_SIZE = 25;  // Keep batches small for reliable parsing
  const results = [];
  let totalCost = 0;
  
  for (let i = 0; i < messages.length; i += BATCH_SIZE) {
    const batch = messages.slice(i, i + BATCH_SIZE);
    const batchNum = Math.floor(i / BATCH_SIZE) + 1;
    const totalBatches = Math.ceil(messages.length / BATCH_SIZE);
    
    console.log(`\n🔄 Processing batch ${batchNum}/${totalBatches} (messages ${i}-${Math.min(i + BATCH_SIZE, messages.length)})...`);
    
    try {
      const batchResults = await classifyBatch(batch, apiKey);
      
      if (batchResults) {
        // Merge results back with original messages
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
        
        // Estimate cost (~$0.00014/1K tokens input, ~$0.00028/1K tokens output for DeepSeek)
        // Rough estimate: ~500 tokens per batch
        totalCost += 0.0005;
        
        console.log(`✅ Batch ${batchNum} complete. Running total: ${results.length} classified`);
      }
    } catch (error) {
      console.error(`❌ Batch ${batchNum} failed:`, error.message);
      // Continue with next batch
    }
    
    // Rate limiting: wait 1 second between batches
    if (i + BATCH_SIZE < messages.length) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    // Save progress every 10 batches
    if (batchNum % 10 === 0) {
      fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
      const useful = results.filter(r => r.useful && r.category);
      const usefulPath = outputPath.replace('.json', '_useful.json');
      fs.writeFileSync(usefulPath, JSON.stringify(useful, null, 2));
      console.log(`💾 Progress saved: ${results.length} classified, ${useful.length} useful`);
    }
  }
  
  // Separate useful vs not useful
  const useful = results.filter(r => r.useful && r.category);
  const notUseful = results.filter(r => !r.useful || !r.category);
  
  console.log(`\n📊 Classification Summary:`);
  console.log(`   Total processed: ${results.length}`);
  console.log(`   Useful tips: ${useful.length} (${(useful.length / results.length * 100).toFixed(1)}%)`);
  console.log(`   Not useful: ${notUseful.length}`);
  console.log(`   Estimated cost: $${totalCost.toFixed(3)}`);
  
  // Category breakdown
  const categoryCounts = {};
  for (const r of useful) {
    categoryCounts[r.category] = (categoryCounts[r.category] || 0) + 1;
  }
  console.log(`\n📁 By Category:`);
  for (const [cat, count] of Object.entries(categoryCounts).sort((a, b) => b[1] - a[1])) {
    console.log(`   ${cat}: ${count}`);
  }
  
  // Save all results
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log(`\n💾 Saved all results to ${outputPath}`);
  
  // Save only useful tips
  const usefulPath = outputPath.replace('.json', '_useful.json');
  fs.writeFileSync(usefulPath, JSON.stringify(useful, null, 2));
  console.log(`💾 Saved useful tips to ${usefulPath}`);
  
  return { results, useful, notUseful };
}

// Main
const inputPath = process.argv[2] || './output/parsed_messages.json';
const outputPath = process.argv[3] || './output/classified_messages.json';
const apiKey = process.env.ALIYUN_API_KEY;

if (!apiKey) {
  console.error('❌ Missing ALIYUN_API_KEY environment variable');
  console.error('   Set it: export ALIYUN_API_KEY=your_key_here');
  process.exit(1);
}

classifyAll(inputPath, outputPath, apiKey);
