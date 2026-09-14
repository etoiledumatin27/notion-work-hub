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
> **How to embed your custom interactive timer here:**
> 1. Type `/embed` right below this line.
> 2. Paste `https://etoiledumatin27.github.io/notion-work-hub/`.
> 3. Drag the borders to adjust the height and width.

---

## 📋 Task & Progress Board

| Task Name | Status | Target 🍅 | Done 🍅 | Progress | Time Spent | Category |
| :--- | :---: | :---: | :---: | :--- | :---: | :--- |
| **Literature Review: Foundation Models** | `In Progress` | 4 | 2 | ▓▓▓▓▓░░░░░ 50% | 50m | Reading Papers |
| **Statistical Learning Theory Ch. 4** | `To Do` | 4 | 0 | ░░░░░░░░░░ 0% | 0m | Textbooks |
| **Draft Methodology Section** | `In Progress` | 6 | 2 | ▓▓▓░░░░░░░ 33% | 50m | Writing |
| **Baseline Benchmarking & Ablation** | `Done` | 3 | 3 | ▓▓▓▓▓▓▓▓▓▓ 100% | 75m | Data Analysis |
| **Implement Custom Attention Layer** | `In Progress` | 4 | 1 | ▓▓░░░░░░░░ 25% | 25m | Coding |
| **Weekly Advisor Meeting Prep** | `To Do` | 2 | 0 | ░░░░░░░░░░ 0% | 0m | Admin |

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
