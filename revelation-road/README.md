# 🚀 启示路 (Revelation Road)

**A Dialogue-Based Sci-Fi Interactive Story Game**

---

## 📖 **Story Premise**

**Setting:** Year 2147. 启示路 (Revelation Road) - a massive space station at the edge of explored space, serving as the last outpost before the unknown Void.

**Player Role:** You are a newly arrived "Seeker" - someone searching for answers, redemption, or a fresh start. Every Seeker carries secrets. Every choice matters.

**Core Mystery:** What lies beyond the Void? Why do ships disappear? What is the station really hiding?

---

## 🎮 **Game Features**

### MVP (Current Version)
- ✅ Single opening scene (Station Arrival)
- ✅ 3 NPC characters with AI-powered dialogue
- ✅ Choice-based conversation system
- ✅ Basic relationship tracking
- ✅ Multiple dialogue paths

### Planned Features
- 🔄 Full story chapters (5 planned)
- 🔄 Complex relationship web
- 🔄 Inventory & quest system
- 🔄 Multiple endings (8+ planned)
- 🔄 Save/load system

---

## 🎭 **Main Characters (MVP)**

| Character | Role | Secret |
|---|---|---|
| **林娜 (Lina)** | Station Guide | Knows more about disappearances than she admits |
| **Dr. Chen** | Research Director | Running unauthorized experiments |
| **The Broker** | Information Dealer | Sells secrets to highest bidder |

---

## 🛠️ **Tech Stack**

| Component | Technology |
|---|---|
| **Runtime** | Node.js 18+ |
| **Frontend** | HTML/CSS/JS (simple chat UI) |
| **Backend** | Node.js + Express |
| **AI Dialogue** | Aliyun Qwen API |
| **State Management** | JSON files (MVP) → Supabase (later) |
| **Deployment** | Zeabur/Vercel |

---

## 🚀 **Quick Start**

### Play in Browser
```bash
# Install dependencies
npm install

# Run the game server
npm start

# Open browser
open http://localhost:3000
```

### Play on Discord
```bash
# Run Discord bot
npm run bot

# Then in Discord:
!start YourName
```

---

## 📁 **Project Structure**

```
revelation-road/
├── src/
│   ├── game.js          # Core game engine
│   ├── dialogue.js      # Dialogue system
│   ├── npc.js           # NPC AI handler
│   └── state.js         # Game state management
├── public/
│   ├── index.html       # Game UI
│   ├── style.css        # Styling
│   └── app.js           # Frontend logic
├── docs/
│   ├── story.md         # Full story outline
│   ├── characters.md    # Character profiles
│   └── api.md           # API documentation
├── tests/
│   └── game.test.js     # Test suite
├── package.json
└── README.md
```

---

## 🎯 **Current Progress**

| Phase | Status | Notes |
|---|---|---|
| Phase 1: Story & World | 🔄 In Progress | Basic outline done |
| Phase 2: Dialogue Engine | ⏳ Pending | |
| Phase 3: NPC AI | ⏳ Pending | |
| Phase 4: UI/UX | ⏳ Pending | |
| Phase 5: Testing | ⏳ Pending | |

---

## 📝 **Version History**

- **v0.1.0** (2026-03-03) - Initial MVP prototype

---

## 🎮 **How to Play**

1. Start the game server
2. Open browser to `http://localhost:3000`
3. Read dialogue and make choices
4. Your choices affect relationships and story outcome
5. Explore different paths on replay

---

## 🤖 **AI Integration**

NPCs use Aliyun Qwen API for dynamic dialogue:
- Context-aware responses
- Personality-driven conversations
- Memory of previous interactions

---

*Built with ❤️ by OpenClaw + Jarvis*
