import getpass
from Stu_functions import StuManage
from extra import Extra
from attendance import AttendanceManage
from colorama import Fore, Style

user_file = 'zProject/users.txt'
class User:
    def __init__(self,user_name):
        try:
            username = input("Enter Username: ")
            password = input("Enter Password: ")

            found = False

            with open(user_file, "r") as f:
                for line in f:
            # Skip blank or invalid lines safely
                    try:
                        user, pw = line.strip().split(',')
                    except ValueError:
                # Raised when a line doesn’t have both username,password
                        continue  

            # Compare credentials
                    if username.strip() == user.strip() and password.strip() == pw.strip():
                        found = True
                        break

            if found:
                print("✅ Login successful!")
            else:
                print("❌ Invalid username or password!")  # Custom error message
                return
            
        except FileNotFoundError:
            print("⚠️ User data file not found! Please create 'users.txt' first.")

        except ValueError as e:
            print(e)  # prints custom message from raise ValueError

        except Exception as e:
            print("⚠️ Unexpected error:", e)

    # ------------- User Dashboard -------------
    # def user_menu(self, user_name):
        ch = ''
        while ch != '6':
            print(f"\n🎓 Welcome, {user_name} 🎓")
            print('''Please select choice:
                  1. View Attendance By Date
                  2. View Attendance By Name
                  3. Show Notice
                  4. View Marks
                  5. Exit
                  ''')

            ch = input('Enter choice: ')

            if ch == '1':
                a = AttendanceManage()
                a.ViewAttendanceByDate()

            elif ch == '2':
                a = AttendanceManage()
                a.ViewAttendanceByName()

            elif ch == '3':
                e = Extra()
                e.view_notices()

            elif ch == '4':
                e = Extra()
                e.show_marks()

            elif ch == '5':
                print(Fore.CYAN + "👋 Thank you! Logging out..." + Style.RESET_ALL)
                break

            else:
                print(Fore.RED + "❌ Invalid choice! Please try again." + Style.RESET_ALL)
# u = User('Student')
