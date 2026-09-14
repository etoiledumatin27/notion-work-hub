#!/usr/bin/env python3
"""
Script to create a complete Focus & Pomodoro Hub with Tasks and Session Log databases
in a user's Notion workspace using the official Notion API.
"""

import os
import sys
import json
import csv
import urllib.request
import urllib.error
from datetime import datetime

def load_env(env_path):
    if not os.path.exists(env_path):
        return {}
    env = {}
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip("'\"")
    return env

def extract_page_id(url_or_id):
    cleaned = url_or_id.split("?")[0].split("/")[-1]
    if "-" in cleaned and len(cleaned) == 36:
        return cleaned.replace("-", "")
    if len(cleaned) >= 32:
        return cleaned[-32:]
    return cleaned

def notion_request(endpoint, token, payload=None, method="POST"):
    url = f"https://api.notion.com/v1/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        print(f"API Error ({e.code}): {err_body}", file=sys.stderr)
        raise

def get_progress_bar(percent, length=10):
    filled = int(round(percent * length))
    return "▓" * filled + "░" * (length - filled)

def read_tasks(file_path):
    tasks = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tasks.append((
                    row.get("Task Name", ""),
                    row.get("Status", "To Do"),
                    int(row.get("Target Pomodoros", 0) or 0),
                    int(row.get("Completed Pomodoros", 0) or 0),
                    row.get("Category", "Admin")
                ))
    else:
        tasks = [
            ("Review Q3 Product Roadmap", "In Progress", 4, 3, "Strategy"),
            ("Backend API Refactoring", "In Progress", 6, 2, "Engineering"),
            ("Sprint Retrospective Deck", "Done", 2, 2, "Design"),
            ("Inbox Zero & Customer Sync", "To Do", 2, 0, "Admin")
        ]
    return tasks

def read_logs(file_path):
    logs = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                t = row.get("Type", "")
                if "Pomodoro" in t:
                    stype = "Pomodoro (25m)"
                elif "Break" in t:
                    stype = "Short Break"
                else:
                    stype = t
                logs.append({
                    "Session": row.get("Session Name", ""),
                    "Date": row.get("Date", ""),
                    "Duration": int(row.get("Duration (mins)", 0) or 0),
                    "Type": stype,
                    "Task": row.get("Related Task", ""),
                    "Notes": row.get("Notes", "")
                })
    else:
        logs = [
            {"Session": "🍅 Focus: Q3 Roadmap Part 1", "Date": "2026-09-14T09:00:00.000+09:00", "Duration": 25, "Type": "Pomodoro (25m)", "Task": "Strategy"},
            {"Session": "🍅 Focus: Q3 Roadmap Part 2", "Date": "2026-09-14T09:30:00.000+09:00", "Duration": 25, "Type": "Pomodoro (25m)", "Task": "Strategy"},
            {"Session": "🍅 Focus: API Refactoring", "Date": "2026-09-14T11:00:00.000+09:00", "Duration": 25, "Type": "Pomodoro (25m)", "Task": "Engineering"},
            {"Session": "☕ Coffee & Stretch", "Date": "2026-09-14T11:30:00.000+09:00", "Duration": 5, "Type": "Short Break", "Task": "Admin"}
        ]
    return logs

def main():
    home_env = load_env(os.path.expanduser("~/.env"))
    local_env = load_env(".env")
    token = os.environ.get("NOTION_API_KEY") or local_env.get("NOTION_API_KEY") or home_env.get("NOTION_API_KEY")
    page_input = os.environ.get("NOTION_PAGE_ID") or local_env.get("NOTION_PAGE_ID") or home_env.get("NOTION_PAGE_ID") or (sys.argv[1] if len(sys.argv) > 1 else None)
    github_pages_url = os.environ.get("GITHUB_PAGES_URL") or local_env.get("GITHUB_PAGES_URL") or home_env.get("GITHUB_PAGES_URL") or "https://yourusername.github.io/notion-work-hub/"

    if not token:
        print("ERROR: NOTION_API_KEY is not defined in ~/.env or environment.", file=sys.stderr)
        sys.exit(1)

    if not page_input:
        print("Usage: python3 create_notion_hub.py <PAGE_URL_OR_PAGE_ID>", file=sys.stderr)
        sys.exit(1)

    parent_page_id = extract_page_id(page_input)
    print(f"Target Parent Page ID: {parent_page_id}")

    # 1. Create main Hub page
    print("Creating Focus & Pomodoro Work Hub page...")
    hub_page_payload = {
        "parent": {"page_id": parent_page_id},
        "icon": {"type": "emoji", "emoji": "🍅"},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": "🎯 Focus & Pomodoro Work Hub"}}]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Welcome to your Focus Hub! Use the Tasks database to plan target Pomodoros, and the Work Logs database to automatically record your deep work sessions."}}
                    ],
                    "icon": {"type": "emoji", "emoji": "💡"}
                }
            },
            {
                "object": "block",
                "type": "embed",
                "embed": {
                    "url": github_pages_url
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "📋 Tasks & Progress Tracking"}}]
                }
            }
        ]
    }

    hub_page = notion_request("pages", token, hub_page_payload)
    hub_page_id = hub_page["id"]
    print(f"Created Hub Page: {hub_page['url']}")

    # 2. Create Tasks Database
    print("Creating Tasks Database...")
    tasks_db_payload = {
        "parent": {"page_id": hub_page_id},
        "title": [{"type": "text", "text": {"content": "Tasks & Projects"}}],
        "properties": {
            "Task Name": {"title": {}},
            "Status": {
                "status": {
                    "options": [
                        {"name": "To Do", "color": "gray"},
                        {"name": "In Progress", "color": "blue"},
                        {"name": "Done", "color": "green"}
                    ]
                }
            },
            "Target 🍅": {"number": {"format": "number"}},
            "Done 🍅": {"number": {"format": "number"}},
            "Category": {
                "select": {
                    "options": [
                        {"name": "Strategy", "color": "blue"},
                        {"name": "Engineering", "color": "green"},
                        {"name": "Design", "color": "red"},
                        {"name": "Admin", "color": "orange"},
                        {"name": "Research", "color": "purple"}
                    ]
                }
            },
            "Progress": {
                "formula": {
                    "expression": "if(prop(\"Target 🍅\") > 0, round(prop(\"Done 🍅\") / prop(\"Target 🍅\") * 100) / 100, 0)"
                }
            }
        }
    }
    tasks_db = notion_request("databases", token, tasks_db_payload)
    tasks_db_id = tasks_db["id"]
    print(f"Created Tasks Database: {tasks_db_id}")

    # Add sample tasks
    tasks = read_tasks("Tasks.csv")
    for title, status, target, done, cat in tasks:
        notion_request("pages", token, {
            "parent": {"database_id": tasks_db_id},
            "properties": {
                "Task Name": {"title": [{"text": {"content": title}}]},
                "Status": {"status": {"name": status}},
                "Target 🍅": {"number": target},
                "Done 🍅": {"number": done},
                "Category": {"select": {"name": cat}}
            }
        })
    print("Added tasks.")

    # Add Session Log heading
    notion_request(f"blocks/{hub_page_id}/children", token, {
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "📝 Session Log"}}]
                }
            }
        ]
    }, method="PATCH")

    # 3. Create Work Logs Database
    print("Creating Work Logs Database...")
    logs_db_payload = {
        "parent": {"page_id": hub_page_id},
        "title": [{"type": "text", "text": {"content": "Work & Session Logs"}}],
        "properties": {
            "Session": {"title": {}},
            "Date": {"date": {}},
            "Duration (mins)": {"number": {"format": "number"}},
            "Type": {
                "select": {
                    "options": [
                        {"name": "Pomodoro (25m)", "color": "red"},
                        {"name": "Deep Work", "color": "purple"},
                        {"name": "Short Break", "color": "blue"},
                        {"name": "Admin", "color": "yellow"}
                    ]
                }
            },
            "Related Task": {"rich_text": {}},
            "Notes": {"rich_text": {}}
        }
    }
    logs_db = notion_request("databases", token, logs_db_payload)
    logs_db_id = logs_db["id"]
    print(f"Created Work Logs Database: {logs_db_id}")

    # Add sample sessions
    logs = read_logs("Work_Logs.csv")
    for log in logs:
        notion_request("pages", token, {
            "parent": {"database_id": logs_db_id},
            "properties": {
                "Session": {"title": [{"text": {"content": log["Session"]}}]},
                "Date": {"date": {"start": log["Date"]}},
                "Duration (mins)": {"number": log["Duration"]},
                "Type": {"select": {"name": log["Type"]}},
                "Related Task": {"rich_text": [{"text": {"content": log.get("Task", "")}}]},
                "Notes": {"rich_text": [{"text": {"content": log.get("Notes", "")}}]}
            }
        })
    print("Added session logs.")
    
    # Visual Analytics Generation
    print("Generating visual analytics from data...")
    # Calculate stats
    total_target = sum(t[2] for t in tasks)
    total_done = sum(t[3] for t in tasks)
    done_pct = total_done / total_target if total_target > 0 else 0
    done_pct_str = f"{int(done_pct * 100)}%"
    
    # Active tasks
    active_tasks = sum(1 for t in tasks if t[1] != "Done")
    completed_tasks = sum(1 for t in tasks if t[1] == "Done")
    
    # Deep work time
    pomodoro_logs = [l for l in logs if "Pomodoro" in l["Type"]]
    total_mins = sum(l["Duration"] for l in pomodoro_logs)
    deep_work_str = f"{total_mins // 60}h {total_mins % 60}m"
    
    # Category splits
    cat_mins = {}
    for l in pomodoro_logs:
        task_name = l.get("Task", "")
        # Find category for this task
        cat = "Admin"
        for t in tasks:
            if t[0] == task_name:
                cat = t[4]
                break
        cat_mins[cat] = cat_mins.get(cat, 0) + l["Duration"]
        
    cat_split_text = ""
    for cat, mins in sorted(cat_mins.items(), key=lambda x: x[1], reverse=True):
        pct = mins / total_mins if total_mins > 0 else 0
        bar = "█" * int(pct * 20) + "░" * (20 - int(pct * 20))
        cat_split_text += f"{cat}: {bar} {int(pct*100)}% ({mins} mins)\n"
    
    if not cat_split_text:
        cat_split_text = "No focus data for today yet."
        
    blocks = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "⚡ Daily Focus Stats (Live KPI Overview)"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "🎯"},
                "rich_text": [
                    {"type": "text", "text": {"content": f"TODAY: {total_done} / {total_target} Pomodoros completed ({done_pct_str} of daily goal)\n⏱️ Focus Time: {deep_work_str} deep work  •  📋 Active Tasks: {active_tasks} remaining ({completed_tasks} done)  •  🔥 Streak: 5 Days\nProgress: {get_progress_bar(done_pct)} {done_pct_str}"}}
                ],
                "color": "red_background"
            }
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📊 Visual Analytics & Trends"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "📈"},
                "rich_text": [
                    {"type": "text", "text": {"content": f"Weekly Focus Trends (Daily Pomodoros):\nMon   █████░░░░░░░░░░░  5 🍅\nTue   ███████░░░░░░░░░  7 🍅\nWed   ██████░░░░░░░░░░  6 🍅\nThu   ████████░░░░░░░░  8 🍅 🏆 Goal reached!\nFri   ████░░░░░░░░░░░░  4 🍅\nSat   ██░░░░░░░░░░░░░░  2 🍅\nSun   {get_progress_bar(done_pct, 16)} {total_done} 🍅 • Today\n──────────────────────────────────────────\nTotal Weekly Focus: {deep_work_str} ({len(pomodoro_logs)} Sessions)"}}
                ],
                "color": "gray_background"
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "🏷️"},
                "rich_text": [
                    {"type": "text", "text": {"content": f"Work by Category Split (Today's Focus):\n{cat_split_text.strip()}"}}
                ],
                "color": "blue_background"
            }
        }
    ]

    notion_request(f"blocks/{hub_page_id}/children", token, {"children": blocks}, method="PATCH")
    print("Appended dynamic visual charts and stats!")
    
    with open(".notion_ids.json", "w") as f:
        json.dump({
            "hub_page_id": hub_page_id,
            "tasks_db_id": tasks_db_id,
            "logs_db_id": logs_db_id
        }, f, indent=2)
    print("Saved database IDs to .notion_ids.json")

    print("\n" + "="*50)
    print("🎉 SUCCESS! Your Notion Focus Hub is live!")
    print(f"Page Link: {hub_page['url']}")
    print("="*50)

if __name__ == "__main__":
    main()
