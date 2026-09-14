import os, json, urllib.request

home_env = {}
with open(os.path.expanduser("~/.env")) as f:
    for line in f:
        if "=" in line:
            k, v = line.strip().split("=", 1)
            home_env[k.strip()] = v.strip().strip("\"'\''")

token = home_env.get("NOTION_API_KEY")
hub_id = "3db8b54903c881039d99c669e3d9af08"

# 1. Delete test embed
headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

try:
    del_req = urllib.request.Request("https://api.notion.com/v1/blocks/3db8b549-03c8-81d5-bfc9-df0b916a2398", headers=headers, method="DELETE")
    urllib.request.urlopen(del_req)
    print("Deleted test block.")
except Exception as e:
    print("Delete test block note:", e)

# 2. Append rich visual blocks matching index.html
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
                {"type": "text", "text": {"content": "TODAY: 6 / 8 Pomodoros completed (75% of daily goal)\n", "annotations": {"bold": True}}},
                {"type": "text", "text": {"content": "⏱️ Focus Time: 2h 30m deep work  •  📋 Active Tasks: 3 remaining (1 done)  •  🔥 Streak: 5 Days\nProgress: ▓▓▓▓▓▓▓▓░░ 75%"}}
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
                {"type": "text", "text": {"content": "Weekly Focus Trends (Daily Pomodoros):\n", "annotations": {"bold": True}}},
                {"type": "text", "text": {"content": "Mon   █████░░░░░░░░░░░  5 🍅  (2h 05m)\nTue   ███████░░░░░░░░░  7 🍅  (2h 55m)\nWed   ██████░░░░░░░░░░  6 🍅  (2h 30m)\nThu   ████████░░░░░░░░  8 🍅  (3h 20m) 🏆 Goal reached!\nFri   ████░░░░░░░░░░░░  4 🍅  (1h 40m)\nSat   ██░░░░░░░░░░░░░░  2 🍅  (0h 50m)\nSun   ██████░░░░░░░░░░  6 🍅  (2h 30m) • Today\n──────────────────────────────────────────\nTotal Weekly Focus: 15h 50m (38 Sessions)"}}
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
                {"type": "text", "text": {"content": "Work by Category Split (Today's Focus):\n", "annotations": {"bold": True}}},
                {"type": "text", "text": {"content": "🔵 Strategy:     ████████████░░░░░░░░  50%  (75 mins)\n🟢 Engineering:  ████████░░░░░░░░░░░░  33%  (50 mins)\n🟠 Admin:        ████░░░░░░░░░░░░░░░░  17%  (25 mins)\n🔴 Design:       ░░░░░░░░░░░░░░░░░░░░   0%  (0 mins)"}}
            ],
            "color": "blue_background"
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
            "rich_text": [{"type": "text", "text": {"content": "🧠 Daily Reflection & Wrap-up"}}]
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": "Completed highest priority task (Review Q3 Roadmap)"}}],
            "checked": True
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": "Wrapped up backend PR review"}}],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": "Set 3 top priorities for tomorrow"}}],
            "checked": False
        }
    }
]

url = f"https://api.notion.com/v1/blocks/{hub_id}/children"
req = urllib.request.Request(url, data=json.dumps({"children": blocks}).encode("utf-8"), headers=headers, method="PATCH")
with urllib.request.urlopen(req) as resp:
    print("Appended all visual charts, stats, and sections!")
