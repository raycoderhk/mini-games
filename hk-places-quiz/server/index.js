const express = require('express');
const { createClient } = require('@supabase/supabase-js');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

// Supabase config
const supabaseUrl = process.env.SUPABASE_URL || 'https://hxrgvuzujvagzlaevwtk.supabase.co';
const supabaseKey = process.env.SUPABASE_KEY || process.env.SUPABASE_SERVICE_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

const PORT = process.env.PORT || 3001;

// Serve static files from parent directory
app.use(express.static(path.join(__dirname, '..')));

// Get vote count for all places
app.get('/api/votes', async (req, res) => {
    try {
        const { data, error } = await supabase
            .from('votes')
            .select('place_id, vote_count')
            .then(async ({ data, error }) => {
                if (error) throw error;
                
                // Aggregate by place_id
                const counts = {};
                for (const row of data) {
                    counts[row.place_id] = (counts[row.place_id] || 0) + row.vote_count;
                }
                
                return { place_counts: counts, total: Object.values(counts).reduce((a, b) => a + b, 0) };
            });
        
        if (error) throw error;
        res.json(data);
    } catch (error) {
        console.error('Error fetching votes:', error);
        res.status(500).json({ error: error.message });
    }
});

// Cast a vote
app.post('/api/votes', async (req, res) => {
    try {
        const { place_id, fingerprint } = req.body;
        
        if (!place_id || !fingerprint) {
            return res.status(400).json({ error: 'Missing place_id or fingerprint' });
        }
        
        // Check cooldown
        const { data: existing } = await supabase
            .from('votes')
            .select('voted_at')
            .eq('place_id', place_id)
            .eq('fingerprint', fingerprint)
            .single();
        
        if (existing) {
            const lastVote = new Date(existing.voted_at);
            const hoursSince = (Date.now() - lastVote.getTime()) / (1000 * 60 * 60);
            
            if (hoursSince < 24) {
                const remaining = Math.ceil(24 - hoursSince);
                return res.json({ 
                    success: false, 
                    cooldown: true, 
                    remaining_hours: remaining,
                    message: `你需要等 ${remaining} 小時後才能再投票`
                });
            }
        }
        
        // Insert or update vote
        const { data, error } = await supabase
            .from('votes')
            .upsert({ 
                place_id, 
                fingerprint, 
                vote_count: 1,
                voted_at: new Date().toISOString()
            }, { 
                onConflict: 'place_id,fingerprint' 
            })
            .select();
        
        if (error) throw error;
        
        // Get new count
        const { data: countResult } = await supabase
            .from('votes')
            .select('vote_count')
            .eq('place_id', place_id);
        
        const totalCount = countResult.reduce((sum, row) => sum + row.vote_count, 0);
        
        res.json({ 
            success: true, 
            count: totalCount,
            message: '投票成功！'
        });
        
    } catch (error) {
        console.error('Error casting vote:', error);
        res.status(500).json({ error: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`HK Places Votes API running on port ${PORT}`);
});
