# 🎯 Daily Work & Pomodoro Focus Hub

> 💡 **Tip**: Pin this page to your Notion favorites. Use the embedded timer or quick buttons to track your deep work sessions automatically!

---

## ⚡ Quick Dashboard

| 🍅 Daily Pomodoro Target | ⏱️ Deep Work Goal | 📋 Active Tasks | 🔥 Focus Streak |
| :---: | :---: | :---: | :---: |
| **6 / 8 Sessions** | **2h 30m / 3h 20m** | **3 Remaining** | **4 Days** |

---

## ⏱️ Pomodoro Timer

> [!NOTE]
> **How to embed an interactive timer here:**
> 1. Type `/embed` right below this line.
> 2. Paste `https://pomofocus.io/app` (or `https://flocus.com/minimalist-pomodoro-timer/`).
> 3. Drag the borders to adjust the height and width to your liking.

---

## 📋 Task & Progress Board

| Task Name | Status | Target 🍅 | Done 🍅 | Progress | Time Spent | Category |
| :--- | :---: | :---: | :---: | :--- | :---: | :--- |
| **Review Q3 Product Roadmap** | `In Progress` | 4 | 2 | ▓▓▓▓▓░░░░░ 50% | 50m | Strategy |
| **Client Presentation Deck** | `To Do` | 6 | 0 | ░░░░░░░░░░ 0% | 0m | Design |
| **Code Review & PR Triage** | `Done` | 2 | 2 | ▓▓▓▓▓▓▓▓▓▓ 100% | 50m | Engineering |
| **Weekly Report & Inbox Zero** | `In Progress` | 2 | 1 | ▓▓▓▓▓░░░░░ 50% | 25m | Admin |
| **Research Competitor Benchmarks** | `To Do` | 3 | 0 | ░░░░░░░░░░ 0% | 0m | Research |

### 🛠️ Formulas for Automatic Progress & Time Tracking:

- **Formula for Progress Bar (`Progress`)**:
  ```javascript
  let(
    target, prop("Target 🍅"),
    done, prop("Done 🍅"),
    if(target > 0,
      round((done / target) * 100) / 100,
      0
    )
  )
  ```
  *(In property settings, set **Show as**: `Bar` or `Ring` and choose your favorite color).*

- **Formula for Total Time (`Time Spent`)**:
  ```javascript
  let(
    mins, prop("Done 🍅") * 25,
    if(mins >= 60,
      floor(mins / 60) + "h " + (mins % 60) + "m",
      mins + "m"
    )
  )
  ```

---

## 🕒 Today's Work & Session Log

| Session | Time | Duration | Type | Linked Task | Notes |
| :--- | :---: | :---: | :--- | :--- | :--- |
| 🍅 Session 1 | 09:00 - 09:25 | 25 mins | Pomodoro | Review Q3 Product Roadmap | Reviewed intro & key milestones |
| 🍅 Session 2 | 09:30 - 09:55 | 25 mins | Pomodoro | Review Q3 Product Roadmap | Added feedback on Q3 roadmap |
| ☕ Coffee Break | 09:55 - 10:05 | 10 mins | Short Break | *None* | Coffee & stretch |
| 🍅 Session 3 | 10:15 - 10:40 | 25 mins | Pomodoro | Weekly Report & Inbox Zero | Responded to high-priority emails |
| 🍅 Session 4 | 11:00 - 11:25 | 25 mins | Pomodoro | Code Review & PR Triage | Tested and approved PR #142 |

---

## 🧠 Daily Reflection & Wrap-up

- [ ] **What was my main win today?**
- [ ] **What caused distractions or friction?**
- [ ] **Top 3 priorities for tomorrow:**
  1. 
  2. 
  3. 
