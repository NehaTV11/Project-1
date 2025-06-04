import sqlite3
import csv
import datetime

# Database Setup
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create Tables
cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
    BookID INTEGER PRIMARY KEY,
    Title TEXT NOT NULL,
    Author TEXT NOT NULL,
    Year INTEGER,
    Available INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Members (
    MemberID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    JoinDate TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Issues (
    IssueID INTEGER PRIMARY KEY,
    BookID INTEGER,
    MemberID INTEGER,
    IssueDate TEXT,
    ReturnDate TEXT,
    FOREIGN KEY(BookID) REFERENCES Books(BookID),
    FOREIGN KEY(MemberID) REFERENCES Members(MemberID)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Staff (
    StaffID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Position TEXT NOT NULL,
    JoinDate TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Logs (
    LogID INTEGER PRIMARY KEY,
    Action TEXT NOT NULL,
    Timestamp TEXT
)''')

conn.commit()

# Book Management Functions
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author: ")
    year = int(input("Enter year: "))
    available = 1
    cursor.execute("INSERT INTO Books (Title, Author, Year, Available) VALUES (?, ?, ?, ?)", (title, author, year, available))
    conn.commit()
    print("Book added successfully!\n")

def view_books():
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    for book in books:
        print(book)

def search_books_by_author():
    author = input("Enter author to search: ")
    cursor.execute("SELECT * FROM Books WHERE Author LIKE ?", ('%' + author + '%',))
    books = cursor.fetchall()
    for book in books:
        print(book)

def update_book():
    book_id = int(input("Enter Book ID to update: "))
    title = input("New Title: ")
    author = input("New Author: ")
    year = int(input("New Year: "))
    cursor.execute("UPDATE Books SET Title=?, Author=?, Year=? WHERE BookID=?", (title, author, year, book_id))
    conn.commit()
    print("Book updated successfully!\n")

def delete_book():
    book_id = int(input("Enter Book ID to delete: "))
    cursor.execute("DELETE FROM Books WHERE BookID=?", (book_id,))
    conn.commit()
    print("Book deleted successfully!\n")

# Member Management Functions
def add_member():
    name = input("Enter member name: ")
    join_date = datetime.date.today().isoformat()
    cursor.execute("INSERT INTO Members (Name, JoinDate) VALUES (?, ?)", (name, join_date))
    conn.commit()
    print("Member added successfully!\n")

def view_members():
    cursor.execute("SELECT * FROM Members")
    members = cursor.fetchall()
    for member in members:
        print(member)

def search_member_by_name():
    name = input("Enter member name to search: ")
    cursor.execute("SELECT * FROM Members WHERE Name LIKE ?", ('%' + name + '%',))
    members = cursor.fetchall()
    for member in members:
        print(member)

# Issue and Return Functions
def issue_book():
    book_id = int(input("Enter Book ID: "))
    member_id = int(input("Enter Member ID: "))
    issue_date = datetime.date.today().isoformat()
    return_date = input("Enter return date (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO Issues (BookID, MemberID, IssueDate, ReturnDate) VALUES (?, ?, ?, ?)", (book_id, member_id, issue_date, return_date))
    cursor.execute("UPDATE Books SET Available=0 WHERE BookID=?", (book_id,))
    conn.commit()
    print("Book issued successfully!\n")

def return_book():
    issue_id = int(input("Enter Issue ID: "))
    cursor.execute("SELECT BookID FROM Issues WHERE IssueID=?", (issue_id,))
    book = cursor.fetchone()
    if book:
        book_id = book[0]
        cursor.execute("UPDATE Books SET Available=1 WHERE BookID=?", (book_id,))
        cursor.execute("DELETE FROM Issues WHERE IssueID=?", (issue_id,))
        conn.commit()
        print("Book returned successfully!\n")
    else:
        print("Issue record not found!\n")

# Staff Management Functions
def add_staff():
    name = input("Enter staff name: ")
    position = input("Enter position: ")
    join_date = datetime.date.today().isoformat()
    cursor.execute("INSERT INTO Staff (Name, Position, JoinDate) VALUES (?, ?, ?)", (name, position, join_date))
    conn.commit()
    print("Staff added successfully!\n")

def view_staff():
    cursor.execute("SELECT * FROM Staff")
    staff = cursor.fetchall()
    for s in staff:
        print(s)

# Log Function
def log_action(action):
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute("INSERT INTO Logs (Action, Timestamp) VALUES (?, ?)", (action, timestamp))
    conn.commit()

# CSV Export Function
def export_books_to_csv():
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    with open('books_export.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['BookID', 'Title', 'Author', 'Year', 'Available'])
        writer.writerows(books)
    print("Books exported to books_export.csv successfully!\n")

# Menu System
def main_menu():
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. View Books")
        print("3. Search Books by Author")
        print("4. Update Book")
        print("5. Delete Book")
        print("6. Add Member")
        print("7. View Members")
        print("8. Search Member by Name")
        print("9. Issue Book")
        print("10. Return Book")
        print("11. Add Staff")
        print("12. View Staff")
        print("13. Export Books to CSV")
        print("14. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_book()
            log_action("Added Book")
        elif choice == '2':
            view_books()
            log_action("Viewed Books")
        elif choice == '3':
            search_books_by_author()
            log_action("Searched Books by Author")
        elif choice == '4':
            update_book()
            log_action("Updated Book")
        elif choice == '5':
            delete_book()
            log_action("Deleted Book")
        elif choice == '6':
            add_member()
             log_action("Added Member")
        elif choice == '7':
            view_members()
            log_action("Viewed Members")
        elif choice == '8':
            search_member_by_name()
            log_action("Searched Member by Name")
        elif choice == '9':
            issue_book()
            log_action("Issued Book")

        else:
            print("Invalid choice. Please try again.")

print("Library Management System loaded successfully. Run main_menu() to start.")

