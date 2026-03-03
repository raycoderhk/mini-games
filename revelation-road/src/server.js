/**
 * 启示路 (Revelation Road) - Game Server
 * Simple Express server to serve the game
 */

const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// Game state storage (in-memory for MVP)
const gameSessions = new Map();

// API Routes
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    game: '启示路 Revelation Road',
    version: '0.1.0',
    timestamp: new Date().toISOString()
  });
});

app.post('/api/game/start', (req, res) => {
  const { playerName } = req.body;
  const sessionId = Date.now().toString();
  
  const gameState = {
    sessionId,
    playerName: playerName || 'Seeker',
    currentScene: 'arrival',
    currentDialogueIndex: 0,
    relationships: { lina: 0 },
    choices: [],
    startedAt: new Date().toISOString()
  };
  
  gameSessions.set(sessionId, gameState);
  
  res.json({
    success: true,
    sessionId,
    gameState
  });
});

app.get('/api/game/:sessionId', (req, res) => {
  const { sessionId } = req.params;
  const gameState = gameSessions.get(sessionId);
  
  if (!gameState) {
    return res.status(404).json({ error: 'Game session not found' });
  }
  
  res.json({
    success: true,
    gameState
  });
});

app.post('/api/game/:sessionId/choice', (req, res) => {
  const { sessionId } = req.params;
  const { choice } = req.body;
  
  const gameState = gameSessions.get(sessionId);
  if (!gameState) {
    return res.status(404).json({ error: 'Game session not found' });
  }
  
  // Record choice
  gameState.choices.push({
    ...choice,
    timestamp: new Date().toISOString()
  });
  
  // Update relationships
  if (choice.rel) {
    Object.entries(choice.rel).forEach(([npc, delta]) => {
      gameState.relationships[npc] = (gameState.relationships[npc] || 0) + delta;
    });
  }
  
  gameSessions.set(sessionId, gameState);
  
  res.json({
    success: true,
    gameState
  });
});

// Serve game UI
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

// Error handling
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({ 
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🚀 启示路 Revelation Road - Game Server                ║
║                                                           ║
║   Version: 0.1.0 MVP                                     ║
║   Status: Running                                        ║
║   URL: http://localhost:${PORT}                            ║
║                                                           ║
║   Built with ❤️ by OpenClaw + Jarvis                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
  `);
});

module.exports = app;
