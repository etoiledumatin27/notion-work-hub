#!/usr/bin/env python3
import os
import sys
import json
import csv
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

def load_env(env_path):
    env = {}
    try:
        if not os.path.exists(env_path):
            return {}
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip("'\"")
    except Exception:
        pass
    return env

def notion_request(endpoint, token, payload=None, method="POST"):
    url = f"https://api.notion.com/v1/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    if method == "GET" and payload:
        url += "?" + urllib.parse.urlencode(payload)
        data = None
    else:
        data = json.dumps(payload).encode("utf-8") if payload else None
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        print(f"API Error ({e.code}): {err_body}", file=sys.stderr)
        raise

def get_db_entries(db_id, token):
    entries = []
    has_more = True
    next_cursor = None
    
    while has_more:
        payload = {}
        if next_cursor:
            payload["start_cursor"] = next_cursor
        
        resp = notion_request(f"databases/{db_id}/query", token, payload, method="POST")
        entries.extend(resp["results"])
        has_more = resp["has_more"]
        next_cursor = resp.get("next_cursor")
        
    return entries

def main():
    home_env = load_env(os.path.expanduser("~/.env"))
    local_env = load_env(".env")
    token = os.environ.get("NOTION_API_KEY") or local_env.get("NOTION_API_KEY") or home_env.get("NOTION_API_KEY")
    
    if not token:
        print("ERROR: NOTION_API_KEY is not defined.", file=sys.stderr)
        sys.exit(1)
        
    if not os.path.exists(".notion_ids.json"):
        print("ERROR: .notion_ids.json not found. Run create_notion_hub.py first.", file=sys.stderr)
        sys.exit(1)
        
    with open(".notion_ids.json", "r") as f:
        ids = json.load(f)
        
    tasks_db_id = ids["tasks_db_id"]
    logs_db_id = ids["logs_db_id"]
    
    # Default to CSVs
    tasks_source = "Tasks.csv"
    logs_source = "Work_Logs.csv"
    
    tasks_data = []
    logs_data = []
    
    import glob
    json_path = None
    if len(sys.argv) > 1 and sys.argv[1].endswith(".json"):
        candidate = os.path.expanduser(sys.argv[1])
        if os.path.exists(candidate):
            json_path = candidate
        else:
            print(f"❌ Error: File not found: {candidate}", file=sys.stderr)
            sys.exit(1)
    elif len(sys.argv) == 1:
        # Auto-detect latest export in ~/Downloads or current folder
        downloads_exports = glob.glob(os.path.expanduser("~/Downloads/focus-hub-export-*.json"))
        local_exports = glob.glob("focus-hub-export-*.json")
        all_exports = sorted(downloads_exports + local_exports, key=os.path.getmtime, reverse=True)
        if all_exports:
            json_path = all_exports[0]
            print(f"💡 Auto-detected latest export from Downloads: {json_path}")

    if json_path:
        print(f"Reading from JSON: {json_path}")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Widget exports tasks as {id, name, target, completed, done(bool), category}
            for t in data.get("tasks", []):
                if isinstance(t.get("done"), bool):
                    # Widget JSON format
                    status = "Done" if t["done"] else ("In Progress" if t.get("completed", 0) > 0 else "To Do")
                    tasks_data.append({
                        "name": t.get("name", ""),
                        "status": status,
                        "target": t.get("target", 0),
                        "done": t.get("completed", 0),
                        "category": t.get("category", "Admin")
                    })
                else:
                    # Already in sync format
                    tasks_data.append(t)
            # Widget exports logs as {id, time, type, task, category, duration}
            export_date = data.get("exportedAt", "")[:10] or datetime.now().strftime("%Y-%m-%d")
            for l in data.get("logs", []):
                if "session" in l:
                    # Already in sync format
                    logs_data.append(l)
                else:
                    # Widget JSON format
                    time_str = l.get("time", "00:00")
                    logs_data.append({
                        "session": f"🍅 {l.get('task', 'Focus Session')}",
                        "date": f"{export_date}T{time_str}:00.000+09:00",
                        "duration": l.get("duration", 25),
                        "type": "Pomodoro (25m)" if l.get("type") == "Pomodoro" else l.get("type", "Pomodoro (25m)"),
                        "task": l.get("task", ""),
                        "notes": ""
                    })
    else:
        print(f"Reading from CSVs: {tasks_source}, {logs_source}")
        if os.path.exists(tasks_source):
            with open(tasks_source, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tasks_data.append({
                        "name": row.get("Task Name", ""),
                        "status": row.get("Status", "To Do"),
                        "target": int(row.get("Target Pomodoros", 0) or 0),
                        "done": int(row.get("Completed Pomodoros", 0) or 0),
                        "category": row.get("Category", "Admin")
                    })
        if os.path.exists(logs_source):
            with open(logs_source, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    t = row.get("Type", "")
                    stype = "Pomodoro (25m)" if "Pomodoro" in t else ("Short Break" if "Break" in t else t)
                    logs_data.append({
                        "session": row.get("Session Name", ""),
                        "date": row.get("Date", ""),
                        "duration": int(row.get("Duration (mins)", 0) or 0),
                        "type": stype,
                        "task": row.get("Related Task", ""),
                        "notes": row.get("Notes", "")
                    })
                    
    print("Fetching existing tasks from Notion...")
    existing_tasks = get_db_entries(tasks_db_id, token)
    task_map = {}
    for task in existing_tasks:
        props = task["properties"]
        title_objs = props.get("Task Name", {}).get("title", [])
        if title_objs:
            title = title_objs[0].get("text", {}).get("content", "")
            task_map[title] = task["id"]
            
    synced_tasks = 0
    created_tasks = 0
    for t in tasks_data:
        title = t["name"]
        props = {
            "Task Name": {"title": [{"text": {"content": title}}]},
            "Status": {"status": {"name": t["status"]}},
            "Target 🍅": {"number": t["target"]},
            "Done 🍅": {"number": t["done"]},
            "Category": {"select": {"name": t["category"]}}
        }
        if title in task_map:
            notion_request(f"pages/{task_map[title]}", token, {"properties": props}, method="PATCH")
            synced_tasks += 1
        else:
            notion_request("pages", token, {
                "parent": {"database_id": tasks_db_id},
                "properties": props
            })
            created_tasks += 1

    print("Fetching existing logs from Notion...")
    existing_logs = get_db_entries(logs_db_id, token)
    log_map = set()
    for log in existing_logs:
        props = log["properties"]
        title_objs = props.get("Session", {}).get("title", [])
        date_obj = props.get("Date", {}).get("date", {})
        if title_objs and date_obj:
            title = title_objs[0].get("text", {}).get("content", "")
            date_str = date_obj.get("start", "")
            log_map.add(f"{title}_{date_str}")

    synced_logs = 0
    created_logs = 0
    for l in logs_data:
        session = l["session"]
        dt = l["date"]
        # Basic parsing/normalization could go here, relying on exact match for simplicity
        if f"{session}_{dt}" in log_map:
            synced_logs += 1
            continue
            
        props = {
            "Session": {"title": [{"text": {"content": session}}]},
            "Date": {"date": {"start": dt}},
            "Duration (mins)": {"number": l["duration"]},
            "Type": {"select": {"name": l["type"]}},
            "Related Task": {"rich_text": [{"text": {"content": l.get("task", "")}}]},
            "Notes": {"rich_text": [{"text": {"content": l.get("notes", "")}}]}
        }
        notion_request("pages", token, {
            "parent": {"database_id": logs_db_id},
            "properties": props
        })
        created_logs += 1

    print("\n" + "="*50)
    print("✅ Sync Summary:")
    print(f"Tasks: {synced_tasks} updated, {created_tasks} created")
    print(f"Logs: {synced_logs} skipped (already exists), {created_logs} created")
    print("="*50)

if __name__ == "__main__":
    main()
