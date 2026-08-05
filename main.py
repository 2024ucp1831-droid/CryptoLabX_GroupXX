from logger import log_activity
from file_analysis import analyze_file

while True:
    print("\n========== CryptoLabX ==========")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Attack")
    print("4. Analyze")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        log_activity("Encrypt")
        print("Coming Soon")

    elif choice == "2":
        log_activity("Decrypt")
        print("Coming Soon")

    elif choice == "3":
        log_activity("Attack")
        print("Coming Soon")

    elif choice == "4":
        log_activity("Analyze")
        file = input("Enter file name: ")
        analyze_file("datasets/" + file)

    elif choice == "5":
        log_activity("Exit")
        print("Bye")
        break

    else:
        print("Invalid choice")
