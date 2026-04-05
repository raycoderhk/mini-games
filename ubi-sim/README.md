# 🦦 UBI Simulator — Can Universal Basic Income Work?

**Part of the [GameWorld](../README.md) mini-game collection.**

An interactive browser-based economic simulation exploring whether Universal Basic Income (UBI) could succeed — runs 10,000 simulated citizens through 30 years of economic life.

Built on Dr. Jay L. Zagorsky's (Boston University) agent-based UBI methodology. Used for classroom demos, YouTube explainers, and think tank policy exploration.

---

## 🎮 Features

### Interactive Controls
- **UBI Amount** — $0 to $30,000/year per adult
- **Phase-Out Range** — EITC-style clawback window
- **Labor Elasticity** — Low / Medium / High (how much UBI reduces work incentive)
- **Time Horizon** — 5 to 50 years

### Real-Time Visualization
- **Gini Index** — Net vs. earned income inequality over time
- **Poverty Rate** — with US benchmark (11.5%)
- **Employment Rate** — behavioral response to UBI
- **Fiscal Sustainability** — UBI cost vs. tax revenue
- **Top 1% vs. Bottom 50%** — income share divergence
- **Quintile Distribution Table** — who gets what share

### Scenario Presets
| Scenario | Description |
|---|---|
| **Baseline (No UBI)** | Current welfare system, no UBI |
| **UBI $12k/yr** | Andrew Yang-style universal $1k/month |
| **UBI $20k/yr** | High UBI scenario — near poverty elimination |
| **UBI + NIT Style** | Strict phase-out — targets lower incomes |

### Playback Controls
- **Run Simulation** — full run with all years
- **Step +1yr** — advance one year at a time
- **Auto-Play** — animated playback at 5yr/sec
- **Year Scrubber** — drag to any point in time

### Evidence-Grade Metrics
- Progressive income tax (US 2024 brackets)
- EITC-style UBI phase-out
- Reservation wage model for employment choice
- Permanent income smoothing (prevents gaming)
- Poverty rate (US: $15,000/yr threshold)
- Gini coefficient, quintile shares, top 1% share

---

## 🎓 Educational Use

**For students:**
- See how Gini, poverty rate, and income distribution actually change under different UBI designs
- Understand the fiscal tradeoff: UBI cost vs. tax revenue
- Explore the behavioral question: does UBI make people stop working?

**For think tanks:**
- Compare 4 pre-built UBI scenarios instantly
- Adjust parameters to model your own proposal
- Export the CSV data for further analysis
- Based on a published academic methodology (Zagorsky/BU)

---

## 📁 Files

```
ubi-sim/
├── index.html   ← Open in any browser — fully self-contained (no server needed!)
└── README.md
```

**Just open `index.html` in Chrome/Firefox/Safari — no install, no server, no dependencies.**

---

## 🔬 Methodology

**Model:** Agent-Based Micro-Simulation
**Population:** 10,000 agents
**Time:** 30 years (configurable)
**Agents:** Individual citizens with:
- Education → skill → wage → employment probability
- Progressive income tax (US 2024 federal brackets)
- EITC-style UBI phase-out based on *permanent income*
- Reservation wage model for voluntary employment
- Savings, consumption, wealth accumulation

**Limitations (be honest about these):**
- Partial equilibrium (no price/macro feedback loops)
- Simplified labor market matching
- No geographic mobility or industry shocks
- For full budget scoring, see the [OSPC UBI Tax Simulator](https://www.ospc.org)

---

## 🦦 About GameWorld

Part of the **GameWorld** collection — interactive simulations and games built for education and policy exploration. All games are single HTML files, no server required.
