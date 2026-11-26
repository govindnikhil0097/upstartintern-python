# Contact Book (Task 03)

A menu-driven command-line contact book in Python that stores contacts in a JSON file (`contacts.json`) so records persist between runs.

## How to Run

1. Make sure Python 3.10+ is installed.
2. Clone this repository and navigate into the task folder:
   ```bash
   git clone [https://github.com/govindnikhil0097/upstartintern-python.git](https://github.com/govindnikhil0097/upstartintern-python.git)
   cd upstartintern-python/task-03-contact-book
   ```
3. Run the script:
   ```bash
   python contact_book.py
   ```

## Design Decisions

- **Standard Library Only:** Built with Python's built-in `json` and `os` modules with no external dependencies.
- **Resilient JSON Loading:** Wraps file reading in `try/except (json.JSONDecodeError, OSError)` and validates the data structure so the app starts cleanly with an empty list if `contacts.json` is missing or corrupted.
- **Partial Case-Insensitive Search:** Matches any substring inside a contact's name regardless of letter case (`term in c.get('name', '').lower()`).
- **Immediate Persistence:** Writes updates to `contacts.json` right after every add, edit, or delete operation so no changes are lost between runs.