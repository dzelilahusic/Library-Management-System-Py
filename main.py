import json
from datetime import datetime, timedelta

class LibrarySystem:
    def __init__(self):
        self.books = []
        self.members = []
        self.rentals = []
    
    def add_book(self):
        title = input("Enter book title: ").strip()
        author = input("Enter book author: ").strip()
        serial_num = input("Enter book serial number: ").strip()
        book = {"title": title, "author": author, "serial_num": serial_num, "available": True}
        self.books.append(book)
        print(f'Book "{title}" added successfully.')
        self.save_data()

    def remove_book(self):
        serial_num = input("Enter the serial number of the book to remove: ").strip()
        book = next((b for b in self.books if b["serial_num"] == serial_num), None)
        if book:
            self.books.remove(book)
            print(f'Book "{book["title"]}" removed successfully.')
            self.save_data()
        else:
            print("Book not found.")

    def display_books(self):
        print("\n--- All Books ---")
        for book in self.books:
            print(f'ID: {book["serial_num"]}, Name: "{book["title"]}", Author: "{book["author"]}", Available: {book["available"]}')
    
    def add_member(self):
        name = input("Enter member name: ").strip()
        member_id = input("Enter member ID: ").strip()
        address = input("Enter member address: ").strip()
        phone = input("Enter member phone number: ").strip()
        email = input("Enter member email: ").strip()
        member = {"id": member_id, "name": name, "address": address, "phone": phone, "email": email, "fine": 0, "rented_books": []}
        self.members.append(member)
        print(f'Member "{name}" added successfully.')
        self.save_data()

    def remove_member(self):
        member_id = input("Enter the member ID to remove: ").strip()
        member = next((m for m in self.members if m["id"] == member_id), None)
        if member:
            self.members.remove(member)
            print(f'Member "{member["name"]}" removed successfully.')
            self.save_data()
        else:
            print("Member not found.")

    def display_members(self):
        print("\n--- All Members ---")
        for member in self.members:
            print(f'ID: {member["id"]}, Name: "{member["name"]}", Fine: {member["fine"]}')
    
    def rent_book(self):
        member_id = input("Enter your member ID: ").strip()
        book_serial = input("Enter book serial number: ").strip()
        book = next((b for b in self.books if b["serial_num"] == book_serial and b["available"]), None)
        member = next((m for m in self.members if m["id"] == member_id), None)
        
        if not book:
            print("Book is not available.")
        elif not member:
            print("Member not found.")
        else:
            book["available"] = False
            due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            member["rented_books"].append({"book": book, "due_date": due_date})
            print(f'Book "{book["title"]}" rented by member "{member["name"]}". Due date: {due_date}.')
            self.save_data()

    def return_book(self):
        member_id = input("Enter your member ID: ").strip()
        book_serial = input("Enter the serial number of the book you want to return: ").strip()
        member = next((m for m in self.members if m["id"] == member_id), None)
        if member:
            book = next((b for b in member["rented_books"] if b["book"]["serial_num"] == book_serial), None)
            if book:
                member["rented_books"].remove(book)
                book["book"]["available"] = True
                print(f'Book "{book["book"]["title"]}" returned successfully.')
                self.save_data()
            else:
                print("This book was not rented by the member.")
        else:
            print("Member not found.")

    def check_overdue(self):
        print("\n--- Overdue Rentals ---")
        today = datetime.now().strftime('%Y-%m-%d')
        overdue_found = False
        for member in self.members:
            for rented_book in member["rented_books"]:
                if rented_book["due_date"] < today:
                    print(f'Overdue: "{rented_book["book"]["title"]}" rented by {member["name"]}. Due date: {rented_book["due_date"]}')
                    overdue_found = True
        
        if not overdue_found:
            print("No overdue rentals.")

    def display_rentals(self):
        print("\n--- Rentals ---")
        for member in self.members:
            if member["rented_books"]:
                print(f'Member: "{member["name"]}"')
                for rented_book in member["rented_books"]:
                    print(f'  Book: "{rented_book["book"]["title"]}", Author: {rented_book["book"]["author"]}, Serial: {rented_book["book"]["serial_num"]}, Due date: {rented_book["due_date"]}')
            else:
                print(f'Member: "{member["name"]}" has no rented books.')

    def save_data(self):
        data = {"books": self.books, "members": self.members, "rentals": self.rentals}
        with open("library_data.json", "w") as file:
            json.dump(data, file, indent=2)
        print("Data saved to library_data.json.")
    
    def load_data(self):
        try:
            with open("library_data.json", "r") as file:
                data = json.load(file)
                self.books = data.get("books", [])
                self.members = data.get("members", [])
                self.rentals = data.get("rentals", [])
                print("Data loaded from library_data.json.")
        except FileNotFoundError:
            print("No data found. Starting with an empty library.")

library_system = LibrarySystem()

library_system.load_data()

while True:
    print("\n--- Library System Login ---")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    if username == "admin@library.com" and password == "admin16":
        print("Login successful!\n")
        break
    else:
        print("Invalid username or password. Please try again.")

while True:
    print("\n--- Library System Menu ---")
    print("1. Add Member       |  2. Remove Member")
    print("3. Add Book         |  4. Remove Book")
    print("5. Display Books    |  6. Display Members")
    print("7. Rent Book        |  8. Check Overdue Rentals")
    print("9. Return Book      | 10. Exit")
    print("11. Display Rentals |")
    
    choice = input("Please choose your option: ").strip()
    if choice == "1":
        library_system.add_member()
    elif choice == "2":
        library_system.remove_member()
    elif choice == "3":
        library_system.add_book()
    elif choice == "4":
        library_system.remove_book()
    elif choice == "5":
        library_system.display_books()
    elif choice == "6":
        library_system.display_members()
    elif choice == "7":
        library_system.rent_book()
    elif choice == "8":
        library_system.check_overdue()
    elif choice == "9":
        library_system.return_book()
    elif choice == "10":
        print("Exiting the system. Goodbye!")
        break
    elif choice == "11":
        library_system.display_rentals()
    else:
        print("Invalid option. Please try again.")