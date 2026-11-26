# CLI Task Manager (Task 04 – Capstone)

A command-line task manager built with Python's `argparse` subcommands, JSON file persistence, status/due-date filtering, and an automated `pytest` test suite.

## Installation

1. Make sure Python 3.10+ is installed.
2. Clone this repository and navigate into the task folder:
   ```bash
   git clone https://github.com/govindnikhil0097/upstartintern-python.git
   cd upstartintern-python/task-04-cli-task-manager
   ```
3. Install `pytest` (only required to run the test suite; the CLI itself uses only the Python standard library):
   ```bash
   pip install -r requirements.txt
   ```

## Usage Examples

Add tasks (with or without a due date):
```bash
python task_manager.py add "Finish capstone documentation" --due 2026-12-22
python task_manager.py add "Review pull requests"
```

List all tasks:
```bash
python task_manager.py list
```

Filter tasks by status (`pending` or `done`) or due date (`YYYY-MM-DD`):
```bash
python task_manager.py list --status pending
python task_manager.py list --due 2026-12-22
python task_manager.py list --status done --due 2026-12-22
```

Mark a task as done or delete it by ID:
```bash
python task_manager.py done 1
python task_manager.py delete 2
```

## Running Tests

Run the `pytest` suite from inside `task-04-cli-task-manager`:
```bash
pytest
```

## Design Decisions

- **`argparse` Subcommands Over Interactive Loops:** Designed `add`, `list`, `done`, and `delete` as subcommands so the CLI behaves like a standard Unix/POSIX command-line utility and can be scripted cleanly.
- **Standard Library Runtime:** The core tool relies solely on `argparse`, `json`, `datetime`, `os`, and `sys`, requiring zero external dependencies to run.
- **Isolated Testing via `--db` & `tmp_path`:** Exposed `--db` on the CLI and `db_path` on core functions so `pytest` tests execute against temporary files without modifying user data.