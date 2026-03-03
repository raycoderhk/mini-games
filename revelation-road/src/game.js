/**
 * 启示路 (Revelation Road) - Core Game Engine
 * Dialogue-based sci-fi interactive story
 */

const fs = require('fs');
const path = require('path');

class GameEngine {
  constructor() {
    this.state = {
      currentPlayer: null,
      currentScene: 'arrival',
      relationships: {},
      choices: [],
      inventory: [],
      flags: {}
    };
    
    this.scenes = this.loadScenes();
    this.npcs = this.loadNPCs();
  }

  loadScenes() {
    // MVP: Single arrival scene with branching dialogues
    return {
      arrival: {
        id: 'arrival',
        title: '抵達启示路',
        description: '你剛從冷凍艙醒來，透過舷窗看到启示路空間站 - 人類文明最遙遠的前哨站。',
        npcs: ['lina'],
        dialogues: [
          {
            id: 'welcome',
            speaker: 'lina',
            text: '歡迎來到启示路，Seeker。我是林娜，你的接待員。旅途還順利嗎？',
            choices: [
              {
                text: '還算順利，只是有點頭暈',
                next: 'headache',
                relationship: { lina: 1 }
              },
              {
                text: '比我預期的要好',
                next: 'good_trip',
                relationship: { lina: 2 }
              },
              {
                text: '我不想談這個',
                next: 'cold_response',
                relationship: { lina: -1 }
              }
            ]
          },
          {
            id: 'headache',
            speaker: 'lina',
            text: '正常反應。冷凍睡眠後需要 2-3 小時適應。來，先喝點水。(遞給你一杯溫水) 說說吧，你來启示路是為了什麼？',
            choices: [
              {
                text: '尋找答案',
                next: 'seeking_answers',
                relationship: { lina: 1 }
              },
              {
                text: '重新开始',
                next: 'fresh_start',
                relationship: { lina: 1 }
              },
              {
                text: '這與你無關',
                next: 'cold_shoulder',
                relationship: { lina: -2 }
              }
            ]
          },
          {
            id: 'good_trip',
            speaker: 'lina',
            text: '(微笑) 那就好。很多人第一次長途冷凍都會吐。說正事，你來启示路是為了什麼？',
            choices: [
              {
                text: '尋找答案',
                next: 'seeking_answers',
                relationship: { lina: 2 }
              },
              {
                text: '工作機會',
                next: 'job_opportunity',
                relationship: { lina: 1 }
              },
              {
                text: '逃避過去',
                next: 'escaping_past',
                relationship: { lina: 3 }
              }
            ]
          },
          {
            id: 'cold_response',
            speaker: 'lina',
            text: '(挑眉) 好吧，保持神秘。不過在启示路，秘密通常會自己找上門。',
            choices: [
              {
                text: '什麼意思？',
                next: 'mysterious_warning',
                relationship: { lina: 1 }
              },
              {
                text: '我不怕秘密',
                next: 'brave_response',
                relationship: { lina: 2 }
              }
            ]
          },
          {
            id: 'seeking_answers',
            speaker: 'lina',
            text: '(眼神閃爍) 答案... 启示路確實有很多答案。但有些問題，可能不該問。',
            choices: [
              {
                text: '你在暗示什麼？',
                next: 'hint_drop',
                relationship: { lina: 2 }
              },
              {
                text: '我會自己找出來',
                next: 'determined',
                relationship: { lina: 1 }
              }
            ]
          },
          {
            id: 'fresh_start',
            speaker: 'lina',
            text: '很多人都是這麼來的。启示路不問過去，只看未來。歡迎加入。',
            choices: [
              {
                text: '謝謝，我需要去哪裡報到？',
                next: 'orientation',
                relationship: { lina: 2 }
              },
              {
                text: '這裡安全嗎？',
                next: 'safety_question',
                relationship: { lina: 1 }
              }
            ]
          },
          {
            id: 'orientation',
            speaker: 'lina',
            text: '明天早上 9 點，C 區報到大廳。這是你的臨時通行證。(遞給你一張卡片) 今晚好好休息，別去禁止區域。',
            choices: [
              {
                text: '禁止區域？',
                next: 'restricted_area',
                relationship: { lina: 1 }
              },
              {
                text: '明白了，謝謝',
                next: 'scene_end',
                relationship: { lina: 2 }
              }
            ]
          },
          {
            id: 'restricted_area',
            speaker: 'lina',
            text: '(壓低聲音) 第 7-9 區，科研專用。沒有許可證進去... 會消失。不是開玩笑。',
            choices: [
              {
                text: '消失？什麼意思？',
                next: 'disappear_hint',
                relationship: { lina: 2 }
              },
              {
                text: '我會記住的',
                next: 'scene_end',
                relationship: { lina: 1 }
              }
            ]
          },
          {
            id: 'disappear_hint',
            speaker: 'lina',
            text: '(環顧四周) 過去三個月，已經有 12 個人... 官方說法是意外或自願離開。但你知道的，启示路只有一個出口。',
            choices: [
              {
                text: '你在調查嗎？',
                next: 'investigation',
                relationship: { lina: 3 }
              },
              {
                text: '為什麼告訴我這些？',
                next: 'why_tell',
                relationship: { lina: 2 }
              }
            ]
          },
          {
            id: 'scene_end',
            speaker: 'lina',
            text: '好了，你的艙房在 B 區 407。好好休息，明天開始新生活。(轉身離開，又回頭) 對了... 如果聽到奇怪的聲音，別理會。這站... 有它的脾氣。',
            choices: [
              {
                text: '【結束對話，前往艙房】',
                next: null,
                endScene: true
              }
            ]
          }
        ]
      }
    };
  }

  loadNPCs() {
    return {
      lina: {
        id: 'lina',
        name: '林娜 (Lina)',
        role: 'Station Guide',
        personality: '友好但神秘，似乎知道內情',
        relationship: 0,
        avatar: '👩‍💼'
      }
    };
  }

  startGame(playerName) {
    this.state.currentPlayer = playerName;
    this.state.currentScene = 'arrival';
    this.state.relationships = { lina: 0 };
    this.state.choices = [];
    
    return {
      success: true,
      scene: this.scenes.arrival,
      message: `歡迎來到启示路，${playerName}。你的旅程開始了...`
    };
  }

  getCurrentScene() {
    return this.scenes[this.state.currentScene];
  }

  makeChoice(choiceId) {
    const scene = this.getCurrentScene();
    if (!scene) return { error: 'No active scene' };

    // Find current dialogue
    let currentDialogue = scene.dialogues[0];
    
    // In MVP, we'll track dialogue progress simply
    // For full version, need proper dialogue tree traversal
    
    const choice = currentDialogue.choices.find(c => c.next === choiceId || c.text === choiceId);
    if (!choice) return { error: 'Invalid choice' };

    // Update relationships
    if (choice.relationship) {
      Object.entries(choice.relationship).forEach(([npc, delta]) => {
        this.state.relationships[npc] = (this.state.relationships[npc] || 0) + delta;
      });
    }

    // Record choice
    this.state.choices.push({
      scene: this.state.currentScene,
      dialogue: currentDialogue.id,
      choice: choice.text,
      timestamp: new Date().toISOString()
    });

    // Find next dialogue
    const nextDialogue = scene.dialogues.find(d => d.id === choice.next);
    
    return {
      success: true,
      dialogue: nextDialogue,
      relationships: { ...this.state.relationships },
      endScene: choice.endScene || false
    };
  }

  getState() {
    return { ...this.state };
  }

  saveGame(slot = 1) {
    const savePath = path.join(__dirname, `../saves/save_${slot}.json`);
    fs.mkdirSync(path.dirname(savePath), { recursive: true });
    fs.writeFileSync(savePath, JSON.stringify(this.state, null, 2));
    return { success: true, path: savePath };
  }

  loadGame(slot = 1) {
    const savePath = path.join(__dirname, `../saves/save_${slot}.json`);
    if (!fs.existsSync(savePath)) {
      return { error: 'Save not found' };
    }
    this.state = JSON.parse(fs.readFileSync(savePath, 'utf8'));
    return { success: true, state: this.state };
  }
}

module.exports = GameEngine;
