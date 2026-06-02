from colorama import Fore, Style
from admin1 import Admin1
from user import User


while True:
    print("\n#####...🎉 WELCOME TO STUDENT RECORD MANAGEMENT SYSTEM 🎓...#####")
    print("=======================================================================")
    print('''Please Select Choice: 
          1. Admin Log In
          2. Student Log In
          3. Student New Register 
          4. Exit''')
    print("************************************************************************")
    
    ch = input('Enter choice: ')

    # -------------------- Admin Section --------------------
    if ch == '1':
        a = Admin1()   # create an Admin object

    # -------------------- User Login --------------------
    elif ch == '2':
        u = User('WelCome Student...🎓')     # login handled inside User class
        
    # -------------------- New Register --------------------
    elif ch == '3':
        print(Fore.YELLOW + "\n--- 🆕 New User Registration ---" + Style.RESET_ALL)
        username = input("Enter new username: ")
        password = input("Enter new password: ")

        
        if not "zProject/users.txt":
            open("zProject/users.txt", "w").close()


        # check if username already exists
        exists = False
        with open("zProject/users.txt", "r") as f:
            for line in f:
                line = line

            # Skip empty or invalid lines
                if not line or "," not in line:
                    continue

                user, pw = line.split(",") # split only on first comma
                if user == username:
                    exists = True
                    break

        if exists:
            print(Fore.RED + "⚠️ Username already exists. Please try another one." + Style.RESET_ALL)
        else:
            # hide_pw = "*" * len(password)  # Replace actual password with asterisks
            hide_pw = password
            with open("zProject/users.txt", "a") as f:
                f.write(f"{username},{hide_pw}\n")
            print(Fore.GREEN + f"✅ Registration successful! Welcome, {username}." + Style.RESET_ALL)
            print(Fore.CYAN + "You can now log in from the main menu using option 2 (User)." + Style.RESET_ALL)
           
    elif ch == '4':
        print(Fore.RED + "Exiting system... Goodbye!" + Style.RESET_ALL)
        break

    # -------------------- Invalid Input --------------------
    else:
        print(Fore.RED + "Invalid choice! Please try again." + Style.RESET_ALL)
