import json
import os

FILE_NAME = "contacts.json"

def loadContact(filename: str) -> list[dict[str, str]]:
    """Load contacts from JSON; return an empty list if missing or broken."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []

def saveContacts(filename: str, contacts: list[dict[str, str]]) -> None:
    """Save the list of contact dictionaries to a JSON file."""
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(contacts, file, indent=2)

def displayContacts(contacts: list[dict[str, str]], indices: list[int] | None = None) -> None:
    """Display contacts with their 1-based record numbers."""
    if not contacts:
        print("\nNo contacts found.\n")
        return
    if indices is None:
        indices = list(range(len(contacts)))
    if not indices:
        print("\nNo matching contacts found.\n")
        return

    print("\n-- Contacts --")
    for index in indices:
        c = contacts[index]
        emailPart = f" | Email: {c['email']}" if c.get('email') else ''
        print(f"{index + 1}. {c['name']} | Phone: {c['phone']}{emailPart}")
    print()

def findMatchingIndices(contacts: list[dict[str, str]], query: str) -> list[int]:
    """Return indices of contacts whose name contains the search query (case-insensitive)."""
    term = query.strip().lower()
    return [i for i, c in enumerate(contacts) if term in c.get('name', '').lower()]

def addContact(contacts: list[dict[str, str]]) -> None:
    """Prompt for contact details and add a new entry."""
    while True:
        name = input("Enter name: ").strip()
        if name:
            break
        print("Name cannot be empty.")
    while True:
        phone = input("Enter phone number: ").strip()
        if phone:
            break
        print("Phone number cannot be empty.")
    email = input("Enter email (optional, press Enter to skip): ").strip()
    contacts.append({
        "name": name,
        "phone": phone,
        "email": email,
    })
    saveContacts(FILE_NAME, contacts)
    print(f"Contact '{name}' added.\n")

def searchContacts(contacts: list[dict[str, str]]) -> None:
    """Search contacts by partial name match."""
    if not contacts:
        print("\nContact book is empty.\n")
        return
    query = input("Enter name (or part of a name) to search: ").strip()
    if not query:
        print("Search query cannot be empty.\n")
        return

    matches = findMatchingIndices(contacts, query)
    displayContacts(contacts, matches)

def selectContactIndex(contacts: list[dict[str, str]], action: str) -> int | None:
    """Display contacts and let the user choose one by number."""
    if not contacts:
        print("\nContact book is empty.\n")
        return None

    displayContacts(contacts)
    choice = input(f"Enter the contact number to {action} (or press Enter to cancel): ").strip()
    if not choice:
        return None
    if not choice.isdigit():
        print("Invalid input. Please enter a number.\n")
        return None

    index = int(choice) - 1
    if 0 <= index < len(contacts):
        return index
    print("Contact number out of range.\n")
    return None

def editContact(contacts: list[dict[str, str]]) -> None:
    """Edit an existing contact while keeping current values if left blank."""
    index = selectContactIndex(contacts, "edit")
    if index is None:
        return
    contact = contacts[index]
    print("Press Enter to keep the current value.")
    new_name = input(f"Name [{contact['name']}]: ").strip()
    new_phone = input(f"Phone [{contact['phone']}]: ").strip()
    new_email = input(f"Email [{contact.get('email', '')}]: ").strip()
    if new_name:
        contact["name"] = new_name
    if new_phone:
        contact["phone"] = new_phone
    if new_email:
        contact["email"] = new_email

    saveContacts(FILE_NAME, contacts)
    print("Contact updated.\n")

def deleteContact(contacts: list[dict[str, str]]) -> None:
    """Delete an existing contact after confirmation."""
    index = selectContactIndex(contacts, "delete")
    if index is None:
        return
    contact = contacts[index]
    confirm = input(f"Delete '{contact['name']}'? (y/n): ").strip().lower()
    if confirm == 'y':
        removed = contacts.pop(index)
        saveContacts(FILE_NAME, contacts)
        print(f"Deleted '{removed['name']}'.\n")
    else:
        print("Deletion cancelled.\n")

def main() -> None:
    contacts = loadContact(FILE_NAME)
    while True:
        print("== Contact Book ==")
        print("1. Add contact")
        print("2. List all contacts")
        print("3. Search contacts")
        print("4. Edit contact")
        print("5. Delete contact")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            addContact(contacts)
        elif choice == "2":
            displayContacts(contacts)
        elif choice == "3":
            searchContacts(contacts)
        elif choice == "4":
            editContact(contacts)
        elif choice == "5":
            deleteContact(contacts)
        elif choice == "6":
            saveContacts(FILE_NAME, contacts)
            print("Contacts saved.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.\n")

if __name__ == "__main__":
    main()