import pytest 
from task_manager import (
    addTask,
    completeTask,
    deleteTask,
    listTasks,
    main,
)

def test_add_and_list_tasks(tmp_path):
    db = str(tmp_path / "tasks.json")
    t1 = addTask("Write unit tests", due="2026-12-20", db_path=db)
    t2 = addTask("Push repo to GitHub", db_path=db)
    assert t1['id'] == 1
    assert t2['id'] == 2

    all_tasks = listTasks(db_path=db)
    assert len(all_tasks) == 2
    assert all_tasks[0]['title'] == "Write unit tests"
    assert all_tasks[0]['status'] == "pending"

def test_filter_by_status(tmp_path):
    db = str(tmp_path / "tasks.json")
    addTask("Task A", db_path=db)
    addTask("Task B", db_path=db)
    completeTask(1, db_path=db)

    done_tasks = listTasks(status = "done", db_path=db)
    pending_tasks = listTasks(status="pending", db_path=db)

    assert len(done_tasks) == 1
    assert done_tasks[0]['title'] == "Task A"
    assert len(pending_tasks) == 1
    assert pending_tasks[0]['status'] == "Task B"

def test_filter_by_due_date(tmp_path):
    db = str(tmp_path / "tasks.json")
    addTask("Submit internship capstone", due="2026-12-22", db_path=db)
    addTask("Prepare notes", due="2026-12-25", db_path=db)
    filtered = listTasks(due='2026-12-22', db_path=db)
    assert len(filtered) == 1
    assert filtered[0]['title'] == "Submit internship capstone"

def test_delete_task_and_invalid_date(tmp_path):
    db = str(tmp_path / "tasks.json")
    addTask("Temporary task", db_path=db)
    removed = deleteTask(1, db_path=db)

    assert removed['title'] == 'Temporary task'
    assert listTasks(db_path=db) == []

    with pytest.raises(ValueError):
        addTask("Bad date task", due='22-12-2026', db_path=db)

def test_cli_subcommands_end_to_end(tmp_path, capsys):
    db = str(tmp_path / "tasks.json")
    assert main(["--db", db, "add", "Review PR", "--due", "2026-12-21"]) == 0
    assert main(["--db", db, "done", "1"]) == 0
    assert main(["--db", db, "list", "--status", "done"]) == 0

    output = capsys.readouterr().out()
    assert "[x] #1 Review PR (done | due: 2026-12-21)" in output