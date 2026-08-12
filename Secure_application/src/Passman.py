import os
import sqlite3

DATABASE = "passwords.db"


# Connect to database
def connect_db():
    return sqlite3.connect(DATABASE)


# Create database table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            website TEXT,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


# Add a password
def add_password():
    username = input("Enter username: ")
    website = input("Enter website: ")
    password = input("Enter password: ")

    conn = connect_db()
    cursor = conn.cursor()

    # INSECURE STORAGE:
    # Password is stored directly as plaintext.
    cursor.execute(
        "INSERT INTO passwords (username, website, password) VALUES (?, ?, ?)",
        (username, website, password)
    )

    conn.commit()
    conn.close()

    print("Password saved successfully.")


# View all passwords
def view_passwords():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT username, website, password FROM passwords")
    records = cursor.fetchall()

    print("\nStored Passwords:")
    print("-----------------")

    for username, website, password in records:
        # INFORMATION LEAKAGE:
        # Passwords are displayed directly on the screen.
        print("Username:", username)
        print("Website :", website)
        print("Password:", password)
        print()

    conn.close()


# Search for a website
def search_password():
    website = input("Enter website to search: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, website, password FROM passwords WHERE website = ?",
        (website,)
    )

    records = cursor.fetchall()

    for username, website, password in records:
        print("\nUsername:", username)
        print("Website :", website)
        print("Password:", password)

    conn.close()


# Main menu
def main():
    create_table()

    # MISSING AUTHENTICATION:
    # There is no login or authentication mechanism.
    # Anyone who runs this program can access all stored passwords.

    while True:
        print("\n===== PASSWORD MANAGER =====")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Search Password")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_password()

        elif choice == "2":
            view_passwords()

        elif choice == "3":
            search_password()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
