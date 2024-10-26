import csv
import os

LIBRARY_FILE = "Library.csv"

class Book:
    def __init__(self, title, author, status="Available"):
        self.title = title
        self.author = author
        self.status = status

class Library:
    def __init__(self):
        self.books = []

    def load_library(self):
        if os.path.exists(LIBRARY_FILE):
            with open(LIBRARY_FILE, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book = Book(row['Title'], row['Author'], row['Status'])
                    self.books.append(book)

    def save_library(self):
        with open(LIBRARY_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Title', 'Author', 'Status'])
            writer.writeheader()
            for book in self.books:
                writer.writerow({'Title': book.title, 'Author': book.author, 'Status': book.status})

    def display_books(self, status=None):
        if not self.books:
            print("Library is empty.")
            return

        if status:
            filtered_books = [book for book in self.books if book.status.lower() == status.lower()]
            if not filtered_books:
                print(f"No books with status '{status}' found.")
            else:
                print(f"Books with status '{status}':")
                for book in filtered_books:
                    print(f"{book.title} by {book.author}")
        else:
            print("Books in the library:")
            for book in self.books:
                print(f"{book.title} by {book.author}")

    def search_book(self, title):
        found_books = [book for book in self.books if book.title.lower() == title.lower()]
        if not found_books:
            print("Book not found in the library.")
        else:
            print("Book found:")
            for book in found_books:
                print(f"{book.title} by {book.author} - Status: {book.status}")

    def update_book_status(self, title, new_status):
        found_books = [book for book in self.books if book.title.lower() == title.lower()]
        if not found_books:
            print("Book not found in the library.")
        else:
            for book in found_books:
                book.status = new_status
            self.save_library()
            print(f"Book '{title}' status updated successfully.")

    def add_book(self, title, author):
        if any(book.title.lower() == title.lower() and book.author.lower() == author.lower() for book in self.books):
            print("Book already exists in the library.")
        else:
            new_book = Book(title, author)
            self.books.append(new_book)
            self.save_library()
            print("Book added successfully.")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPress Enter to continue..")

def prompt_continue():
    choice = input("Do you want to choose another option? (yes/no): ").strip().lower()
    return choice == 'yes'

def admin_menu(library):
    ADMIN_PASSWORD = "adminjaiswal"  # Set your admin password here
    for attempt in range(3):  # Allow up to 3 attempts
        password = input("Enter admin password: ")
        if password == ADMIN_PASSWORD:
            print("Login successful. Welcome to the Admin Menu.")
            break
        else:
            print("Incorrect password. Please try again.")
    else:
        print("Too many failed attempts. Exiting.")
        return  # Exit if password attempts exceed limit

    while True:
        print("\nAdmin Menu:")
        print("1. Display All Books")
        print("2. Display Issued Books")
        print("3. Display Available Books")
        print("4. Search for a Book")
        print("5. Issue a Book")
        print("6. Return a Book")
        print("7. Add a Book")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            library.display_books()
        elif choice == '2':
            library.display_books("Issued")
        elif choice == '3':
            library.display_books("Available")
        elif choice == '4':
            title = input("Enter the title of the book you want to search for: ")
            library.search_book(title)
        elif choice == '5':
            title = input("Enter the title of the book you want to issue: ")
            library.update_book_status(title, "Issued")
        elif choice == '6':
            title = input("Enter the title of the book you want to return: ")
            library.update_book_status(title, "Available")
        elif choice == '7':
            title = input("Enter the title of the book: ")
            author = input("Enter the author's name: ")
            library.add_book(title, author)
        elif choice == '8':
            print("Exiting Admin Menu.")
            break
        else:
            print("Invalid choice. Please try again.")

        if not prompt_continue():
            break

def user_menu(library):
    while True:
        print("\nUser Menu:")
        print("1. Display All Books")
        print("2. Display Issued Books")
        print("3. Display Available Books")
        print("4. Search for a Book")
        print("5. Return a Book")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            library.display_books()
        elif choice == '2':
            library.display_books("Issued")
        elif choice == '3':
            library.display_books("Available")
        elif choice == '4':
            title = input("Enter the title of the book you want to search for: ")
            library.search_book(title)
        elif choice == '5':
            title = input("Enter the title of the book you want to return: ")
            library.update_book_status(title, "Available")
        elif choice == '6':
            print("Exiting User Menu.")
            break
        else:
            print("Invalid choice. Please try again.")

        if not prompt_continue():
            break

def main():
    clear_screen()
    print("Welcome to Library Management System")

    library = Library()
    library.load_library()

    print("\nLogin:")
    role = input("Enter your role (admin/user): ").strip().lower()

    if role not in ["admin", "user"]:
        print("Invalid role. Please enter 'admin' or 'user'.")
        return

    if role == "admin":
        admin_menu(library)
    else:
        print("You are now logged in as User.")
        user_menu(library)

    print("Exiting")

if __name__ == "__main__":
    main()
