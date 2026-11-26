import argparse
from datetime import datetime
import json
import os 
import sys 

DEFAULT_DB = "tasks.json"

def isValidDate(date_str: str) -> bool:
    """Validate that a due date string follows YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def loadTasks(db_path: str = DEFAULT_DB) -> list[dict]:
    """Load tasks from JSON; return any empty list if missing or corrupted."""
    if not os.path.exists(db_path):
        return []
    try:
        with open(db_path, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []

def saveTasks(tasks: list[dict], db_path: str = DEFAULT_DB) -> None:
    """Save tasks list to JSON."""
    with open(db_path, mode='w', encoding='utf-8') as file:
        json.dump(tasks, file, indent=2)

def addTask(title: str, due: str | None = None, db_path: str = DEFAULT_DB) -> dict:
    """Create and persist a new task."""
    cleanTitle = title.strip()
    if not cleanTitle:
        raise ValueError("Task title cannot be empty.")

    if due is not None and not isValidDate(due):
        raise ValueError("Invalid due date. Use YYYY-MM-DD format.")

    tasks = loadTasks(db_path)
    nextId = max((task.get("id", 0) for task in tasks), default=0) + 1
    newTask = {
        "id": nextId,
        "title": cleanTitle,
        "status": "pending",
        "due": due,
    }
    tasks.append(newTask)
    saveTasks(tasks, db_path)
    return newTask

def listTasks(status: str | None = None, due: str | None = None, db_path: str = DEFAULT_DB) -> list[dict]:
    """Return tasks optionally filtered by status and/or due date."""
    if due is not None and not isValidDate(due):
        raise ValueError("Invalid due date filter. Ue YYYY-MM-DD format.")
    tasks = loadTasks(db_path)
    if status:
        tasks = [t for t in tasks if t.get('status') == status]
    if due:
        tasks = [t for t in tasks if t.get("due") == due]
    return tasks

def completeTask(task_id: int, db_path: str = DEFAULT_DB) -> dict:
    """Mark a task as done by ID."""
    tasks = loadTasks(db_path)
    for task in tasks:
        if task.get("id") == task_id:
            task["status"] = "done"
            saveTasks(tasks, db_path)
            return task
    raise LookupError(f"Task with ID {task_id} not found.")

def deleteTask(task_id: int, db_path: str = DEFAULT_DB) -> dict:
    """Remove a task by ID."""
    tasks = loadTasks(db_path)
    for index, task in enumerate(tasks):
        if task.get("id") == task_id:
            removed = tasks.pop(index)
            saveTasks(tasks, db_path)
            return removed
    raise LookupError(f"Task with ID {task_id} not found.")

def buildParser() -> argparse.ArgumentParser:
    """Configure argparse subcommands."""
    parser = argparse.ArgumentParser(prog="task_manager", description="Command-line task manager with filtering and JSON persistence.")
    parser.add_argument(
        "--db",
        default=DEFAULT_DB,
        help=f"Path to tasks JSON file (default: {DEFAULT_DB})",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task description")
    add_parser.add_argument("--due", default=None, help="Optional due date (YYYY-MM-DD)")

    list_parser = subparsers.add_parser("list", help="List tasks with optional filters")
    list_parser.add_argument(
        "--status",
        choices = ['pending', 'done'],
        default=None,
        help="Filter by status (pending or done)",
    )
    list_parser.add_argument(
        "--due",
        default=None,
        help="Filter by due date (YYYY-MM-DD)",
    )

    done_parser = subparsers.add_parser("done", help="Mark a task as completed")
    done_parser.add_argument("id", type=int, help="Task ID to mark as done")

    del_parser = subparsers.add_parser("delete", help="Delete a task")
    del_parser.add_argument("id", type=int, help="Task ID to delete")

    return parser

def main(argv: list[str] | None = None) -> int:
    parser = buildParser()
    args = parser.parse_args(argv)
    try:
        if args.command == "add":
            task = addTask(args.title, due = args.due, db_path = args.db)
            due_text = f" (due {task['due']})" if task["due"] else ""
            print(f"Added #{task['id']}: {task['title']}{due_text}")

        elif args.command == "list":
            tasks = listTasks(status=args.status, due=args.due, db_path=args.db)
            if not tasks:
                print("No tasks found.")
                return 0
            for task in tasks:
                mark = "x" if task["status"] == "done" else " "
                due_text = f" | due: {task['due']}" if task.get("due") else ""
                print(f"[{mark}] #{task['id']} {task['title']} ({task['status']}{due_text})")

        elif args.command == "done":
            task = completeTask(args.id, db_path=args.db)
            print(f"Completed #{task['id']}: {task['title']}")
        elif args.command == "delete":
            task = deleteTask(args.id, db_path=args.db)
            print(f"Deleted #{task['id']}: {task['title']}")

        return 0

    except (ValueError, LookupError) as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())