from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore,Style

class AttendanceManage:
    attendance_file = 'zProject/Attendance.txt'
    student_file = 'zProject/Stu_Details.txt'


    def MarkAttendance(self):
        try:
            
            date_today = datetime.now().strftime("%Y-%m-%d")

            # Read all student records
            print("---------------------------------------------------------------")
            with open(self.student_file, 'r') as fp:
                students = [line.strip().split(',') for line in fp if line.strip()]

            if not students:
                print("⚠️ No students found.")
                return

            print(f"\n📅   Marking attendance for {date_today}")
            attendance_data = []
            print("-----------------------------------------------------------------")
            for stu in students:
                # ✅ Ensure each student line has at least two parts (ID, Name)
                if len(stu) < 2:
                    print(f"⚠️ Skipping malformed line: {stu}")
                    continue

                sid, name = stu[0].strip(), stu[1].strip()

                # Ask user to mark presence
                print(Fore.LIGHTMAGENTA_EX+"")
                status = input(f"ID {sid} : {name} present? (P/A): ").strip().upper()
                print("_______________________________________________________________"+Style.RESET_ALL)
                if status not in ['P', 'A']:
                    status = 'A'  # default to Absent if invalid input

                attendance_data.append(f"{date_today},{sid},{name},{status}\n")

            # ✅ Write attendance line by line (no writelines)
            with open(self.attendance_file, 'a') as fp:
                for record in attendance_data:
                    fp.write(record)

            print(Fore.GREEN+"✅ Attendance marked successfully."+Style.RESET_ALL)

        except FileNotFoundError:
            print("❌ Student data file not found.")
        except Exception as e:
            print("❌ Error:", e)

    def ViewAttendanceByDate(self):
            try:
                date_to_view = input("Enter date (YYYY-MM-DD): ")
                file_name = 'zProject/Attendance.txt'
                print(Fore.LIGHTYELLOW_EX+"")
                table = PrettyTable(["Date", "ID", "Name", "Status"])
                found = False
                print(Fore.BLUE+"======================📅🎓 STUDENT ATTENDANCE =============================="+Style.RESET_ALL)
                print(Fore.LIGHTYELLOW_EX+"")
                with open(file_name, 'r') as fp:
                    for line in fp:  #  Directly iterate over each line
                        line = line.strip()
                        if not line:
                            continue

                        parts = line.split(',')
                        if len(parts) != 4:
                            print(f"⚠️ Skipping malformed line: {line}")
                            continue

                        date, sid, name, status = [p.strip() for p in parts]

                        if date == date_to_view:
                            table.add_row([date, sid, name, status])
                            found = True
                        

                if found:
                    print(table)
                    
                else:
                    print(f"⚠️ No attendance found for {date_to_view}."+Style.RESET_ALL)
            except FileNotFoundError:
                print("❌ Attendance file not found.")
            except Exception as e:
                print("❌ Error:", e)

    

    def ViewAttendanceByName(self):
        try:
            name_to_view = input("Enter Student Name: ").strip().lower()
            file_name = 'zProject/Attendance.txt'

            table = PrettyTable(["Date", "ID", "Name", "Status"])
            found = False
            print(Fore.BLUE+"======================📅🎓 STUDENT ATTENDANCE =============================="+Style.RESET_ALL)
            print(Fore.LIGHTYELLOW_EX+"")
            with open(file_name, 'r') as fp:
                for line in fp:  # ✅ Directly iterate over each line
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(',')
                    if len(parts) != 4:
                        print(f"⚠️ Skipping malformed line: {line}")
                        continue

                    date, sid, name, status = [p.strip() for p in parts]

                    if name.lower() == name_to_view:
                        table.add_row([date, sid, name, status])
                        found = True

            if found:
                print(table)
                print(""+Style.RESET_ALL)
            else:
                print(f"⚠️ No attendance found for student '{name_to_view}'.")

        except FileNotFoundError:
            print("❌ Attendance file not found.")
        except Exception as e:
            print("❌ Error:", e)
    

if __name__ == "__main__":
    A = AttendanceManage()
    # A.MarkAttendance()
    # A.ViewAttendanceByDate()
    A.ViewAttendanceByName()