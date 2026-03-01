# Reddit Post #2: Photo Hunt Tutorial

**Subreddit:** r/OpenClawUseCases  
**Post Type:** [Tutorial]  
**Estimated Time:** 10-15 minutes to post  

---

## 📝 Post Title

```
[Tutorial] How I built a "Find the Differences" game with Canvas + persistent markers
```

---

## 📄 Post Content

```markdown
Following up on my GameWorld showcase post, several people asked about the Photo Hunt game. Here's a breakdown of how I built it! 🎨

## 🎯 What Is Photo Hunt?

Classic "find the differences" puzzle game:
- Two side-by-side images
- 5 hidden differences
- Click to find them
- Markers stay on BOTH images when found (key UX feature!)

**Play it here:** https://gameworld.zeabur.app/photohunt/

---

## 🛠️ Core Technologies

| Technology | Purpose |
|------------|---------|
| **HTML5 Canvas** | Drawing the scene programmatically |
| **JavaScript** | Game logic, click detection, state management |
| **CSS Animations** | Visual feedback (pulsing markers) |
| **No external libraries** | Pure vanilla JS |

---

## 📐 Architecture Overview

```
┌─────────────────────────────────────────┐
│           Game Container                │
├─────────────────────────────────────────┤
│  Header (Title + Stats: Found/Time)    │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐      │
│  │  Canvas 1   │  │  Canvas 2   │      │
│  │  (Original) │  │ (Modified)  │      │
│  └─────────────┘  └─────────────┘      │
├─────────────────────────────────────────┤
│  Controls (Start/Back) + Instructions  │
└─────────────────────────────────────────┤
```

---

## 💻 Key Code Sections

### 1. Defining Differences

```javascript
// Each difference has: position, hit radius, description
const differences = [
    { x: 100, y: 100, radius: 30, description: "太陽顏色" },
    { x: 250, y: 200, radius: 25, description: "樹木高度" },
    { x: 400, y: 150, radius: 35, description: "雲朵形狀" },
    { x: 150, y: 300, radius: 30, description: "花朵顏色" },
    { x: 350, y: 350, radius: 28, description: "石頭位置" }
];
```

### 2. Drawing the Scene

```javascript
function drawScene(ctx, isModified = false) {
    // Sky gradient
    const skyGradient = ctx.createLinearGradient(0, 0, 0, 200);
    skyGradient.addColorStop(0, '#87CEEB');
    skyGradient.addColorStop(1, '#E0F6FF');
    ctx.fillStyle = skyGradient;
    ctx.fillRect(0, 0, 500, 200);
    
    // Draw elements with modifications based on isModified flag
    drawSun(ctx, 100, 100, isModified); // Color differs
    drawTree(ctx, 250, 200, isModified); // Height differs
    // ... more elements
}
```

### 3. Click Detection (The Tricky Part)

```javascript
function handleClick(e, isCanvas2) {
    if (!gameState.started || !isCanvas2) return;
    
    // Get click coordinates relative to canvas
    const rect = canvas2.getBoundingClientRect();
    const scaleX = canvas2.width / rect.width;
    const scaleY = canvas2.height / rect.height;
    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;
    
    // Check distance to each difference
    differences.forEach((diff, index) => {
        if (gameState.found.includes(index)) return;
        
        const distance = Math.sqrt(
            Math.pow(x - diff.x, 2) + 
            Math.pow(y - diff.y, 2)
        );
        
        if (distance < diff.radius + 20) { // +20 for forgiveness
            // Found it!
            gameState.found.push(index);
            showFoundMarker(x, y, index);
            updateStats();
        }
    });
}
```

### 4. Persistent Markers (Key UX Feature)

```javascript
function showFoundMarker(x, y, index) {
    // Show on BOTH images
    createMarker(document.getElementById('image1Wrapper'), x, y, index);
    createMarker(document.getElementById('image2Wrapper'), x, y, index);
}

function createMarker(wrapper, x, y, index) {
    // Check if marker already exists
    const existing = wrapper.querySelector(`.found-marker[data-index="${index}"]`);
    if (existing) return; // Don't duplicate
    
    const marker = document.createElement('div');
    marker.className = 'found-marker';
    marker.setAttribute('data-index', index); // Track which difference
    marker.textContent = '✓';
    marker.style.left = (x / 500 * 100) + '%';
    marker.style.top = (y / 400 * 100) + '%';
    wrapper.appendChild(marker);
    // NO timeout - marker stays permanently!
}
```

### 5. CSS for Visual Feedback

```css
.found-marker {
    position: absolute;
    width: 40px;
    height: 40px;
    background: rgba(46, 213, 115, 0.9);
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 1.5em;
    font-weight: bold;
    animation: pop 0.3s ease-out;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    z-index: 10;
}

/* Pulsing ring effect */
.found-marker::after {
    content: '';
    position: absolute;
    width: 50px;
    height: 50px;
    border: 2px solid rgba(46, 213, 115, 0.5);
    border-radius: 50%;
    animation: pulse-ring 1.5s ease-out infinite;
}

@keyframes pulse-ring {
    0% { transform: scale(0.8); opacity: 1; }
    100% { transform: scale(1.5); opacity: 0; }
}
```

---

## 🎨 Drawing Functions (Sample)

```javascript
function drawTree(ctx, x, y, isModified) {
    // Trunk
    ctx.fillStyle = '#8B4513';
    const height = isModified ? 80 : 100; // DIFFERENCE!
    ctx.fillRect(x - 15, y - height, 30, height);
    
    // Leaves (3 circles)
    ctx.fillStyle = '#228B22';
    ctx.beginPath();
    ctx.arc(x, y - height - 30, 50, 0, Math.PI * 2);
    ctx.fill();
    // ... more circles
}
```

---

## 🧠 Game State Management

```javascript
let gameState = {
    started: false,
    found: [],           // Array of found difference indices
    mistakes: 0,         // Wrong clicks
    startTime: null,     // For timer
    timerInterval: null, // setInterval reference
    totalDifferences: 5
};

function startGame() {
    gameState = {
        started: true,
        found: [],
        mistakes: 0,
        startTime: Date.now(),
        timerInterval: null,
        totalDifferences: 5
    };
    
    // Clear markers from previous game
    document.querySelectorAll('.found-marker').forEach(m => m.remove());
    
    // Redraw scenes
    drawScene(ctx1, false);
    drawScene(ctx2, true);
    
    startTimer();
}
```

---

## 🏆 Win Condition & Scoring

```javascript
function endGame() {
    stopTimer();
    
    const elapsed = Math.floor((Date.now() - gameState.startTime) / 1000);
    const baseScore = 1000;
    const timePenalty = elapsed * 2;
    const mistakePenalty = gameState.mistakes * 50;
    const score = Math.max(0, baseScore - timePenalty - mistakePenalty);
    
    // Show modal with stats
    document.getElementById('modalTime').textContent = formatTime(elapsed);
    document.getElementById('modalMistakes').textContent = gameState.mistakes;
    document.getElementById('modalScore').textContent = score;
    document.getElementById('gameOverModal').classList.add('show');
}
```

---

## 💡 Lessons Learned

### What Worked Well
✅ **Canvas for procedural graphics** - No image assets needed  
✅ **Percentage-based positioning** - Responsive by default  
✅ **Persistent markers** - Users love knowing what they found  
✅ **Forgiving hit detection** - +20px radius prevents frustration  

### What I'd Improve
🔄 **More differences** - 5 is easy, could add difficulty levels  
🔄 **Hint system** - Button to highlight remaining differences  
🔄 **Level editor** - Let users create their own puzzles  
🔄 **Sound effects** - Feedback on click/find/win  

---

## 📦 Full Source Code

The complete game is open source:

**GitHub:** https://github.com/raycoderhk/2048-game/tree/main/photohunt

**File:** `photohunt/index.html` (single file, ~600 lines)

---

## 🚀 Try It Yourself!

Want to build something similar? Here's a starter challenge:

1. Fork my repo
2. Modify the `drawScene()` function to create a new scene
3. Define 3-5 new differences
4. Adjust colors, shapes, or theme

Tag me if you build something cool - would love to see it! 🎮

---

## ❓ Questions?

Drop a comment if you have questions about:
- Canvas drawing techniques
- Click detection logic
- State management
- Deployment to Zeabur

Happy coding! 🚀
```

---

## 🖼️ Media to Include

### Screenshots
1. **Game in progress** - Show 2-3 found differences with markers
2. **Win modal** - Display final score/stats
3. **Code snippet** - Screenshot of the click detection logic

### Optional: GIF Demo
- 10-second loop showing:
  - Click on a difference
  - Marker appears on both images
  - Counter updates
  - Win screen

---

## 📅 When to Post

**Timing:** 3-5 days after Post #1 (let first post breathe)  
**Best Day:** Tuesday or Wednesday  
**Best Time:** 9-11 AM UTC

---

## 💬 Engagement Strategy

### Expected Questions & Answers

**Q: "Why Canvas instead of images?"**
```
Great question! Canvas lets me:
1. Draw everything programmatically (no asset management)
2. Easily create variations (isModified flag)
3. Scale to any resolution
4. Animate elements if needed

For a simple game, images would work too - but Canvas is more flexible!
```

**Q: "How do you handle mobile touch?"**
```
The click handler works for both mouse and touch! 
Canvas click events fire on tap. 
The responsive CSS ensures it fits any screen.

Could add touch-specific optimizations, but vanilla events work well.
```

**Q: "Can I use this for my project?"**
```
Absolutely! The code is open source (MIT license).
Just credit the repo if you use it publicly.
Would love to see what you build! 🚀
```

---

*Document created: 2026-02-28*
*Ready to post after Post #1 gains traction*
