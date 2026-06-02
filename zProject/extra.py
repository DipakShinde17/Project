from prettytable import PrettyTable
from colorama import Style,Fore
MARKS_FILE = "marks.txt"
NOTICE_FILE = "notices.txt"
OTHER_ACTIVITI = "other_activity.txt"


        
class Extra:
    
    def add_exam_marks(self):
        print("============================ 📄 ADD MARKS ============================")
        roll = input("Enter Roll Number                 : ")
        name = input("Enter Student Name                : ")
        subjects = ["Math", "Science", "English", "History", "Computer"]
        marks = {}
        for sub in subjects:
            mark = input(f"{sub} Marks                        : ")
            if mark.strip():
                marks[sub] = float(mark)

        if not marks:
            print("⚠️ No marks entered.")
            return

        total = sum(marks.values())
        percent = total / len(marks)

        line = f"Roll: {roll}, Name: {name}"
        for sub, m in marks.items():
            line += f", {sub}: {m}"
        line += f", Total: {total}, Percentage: {percent:.2f}%\n"

        with open(MARKS_FILE, "a") as f:
            f.write(line)
        print("----------------------------------------------------")
        print("✅ Marks added successfully!")
     # ---------- SHOW MARKS ----------
        # def show_marks():
        #     roll = input("Enter Roll Number to View Marks: ")

        #     if not MARKS_FILE:
        #         print("⚠️ No marks file found.")
        #         return

        #     found = False
        #     with open(MARKS_FILE, "r") as f:
        #         for line in f:
        #             if f"Roll: {roll}" in line:
        #                 print("\n📘 Student Marks Record:")
        #                 print(line.strip())
        #                 found = True
        #                 break

        #     if not found:
        #         print("⚠️ Student not found!")
    @staticmethod
    def show_marks():
            
            roll = input("Enter Roll Number to View Marks: ")

            if not MARKS_FILE:
                print("⚠️ No marks file found.")
                return

            found = False
            with open(MARKS_FILE, "r") as f:
                for line in f:
                    if f"Roll: {roll}" in line:
                        found = True

                        # Split the line into fields
                        data_parts = [part.strip() for part in line.strip().split(",")]

                        # Extract Data into Dictionaries
                        # student_info stores roll, name, total, and percentage.
                        # subjects stores subject names and marks
                        
                        student_info = {}
                        subjects = {}

                        # Extract fields
                        for part in data_parts:
                            if part.startswith("Roll:"):
                                student_info["roll"] = part.split(":")[1].strip()
                            elif part.startswith("Name:"):
                                student_info["name"] = part.split(":")[1].strip()
                            elif part.startswith("Total:"):
                                student_info["total"] = part.split(":")[1].strip()
                            elif part.startswith("Percentage:"):
                                student_info["percent"] = part.split(":")[1].strip().replace("%", "")
                            elif ":" in part:
                                key, value = part.split(":")
                                key = key.strip()
                                value = value.strip()
                                if key not in ["Roll", "Name", "Total", "Percentage"]:
                                    subjects[key] = value

                        # Convert percentage for grade calculation
                        try:
                            percent_value = float(student_info.get("percent", 0))
                        except ValueError:
                            percent_value = 0.0

                        # Grade logic
                        if percent_value >= 90:
                            grade = "A+"
                        elif percent_value >= 80:
                            grade = "A"
                        elif percent_value >= 70:
                            grade = "B"
                        elif percent_value >= 60:
                            grade = "C"
                        elif percent_value >= 50:
                            grade = "D"
                        else:
                            grade = "F"

                        
                        # Create the table
                        table = PrettyTable()
                        table.field_names = ["Subject", "Marks"]
                        
                        for sub, mark in subjects.items():
                            table.add_row([sub, mark])

                        # Add summary row
                        table.add_row(["-" * 10, "-" * 10])
                        table.add_row(["Total", student_info.get("total", "N/A")])
                        table.add_row(["Percentage", f"{student_info.get('percent', '0')}%"])
                        table.add_row(["Grade", grade])

                        
                        # Display student info and table
                        print("===========📘 Student Marks Record ===========")

                        print(Fore.GREEN+"")
                        print(f"Roll Number : {student_info.get('roll', '')}")
                        print(f"Name        : {student_info.get('name', '')}\n")
                        print(table)
                        print(""+Style.RESET_ALL)
                        break

            if not found:
                print("⚠️ Student not found!")


    @staticmethod
    def add_notice():
        try:
            print("============================ 🔎 ADD NOTICE =============================")
            title = input("Enter Notice Title: ")
            Discription = input("Enter Notice Description: ")
            with open(NOTICE_FILE, "a") as f:
                f.write(f"Title: {title}\nBody: {Discription}\n")
            print("------------------------------------------------------------------")
            print(Fore.GREEN+"☑️ Notice added successfully!"+Style.RESET_ALL)
        except FileNotFoundError:
             print("⚠️ No notices found.")

    @staticmethod
    def view_notices():
        try:
            print("=========================== 📢Important Notice===============================")
            with open(NOTICE_FILE, "r") as f:
                print(f.read())
        except FileNotFoundError:
            print("⚠️ No notices found.")
            print("-----------------------------------------------------------------------")
    

if __name__ == "__main__":
    e = Extra
    # e.add_notice()
    # e.view_notices()
    # e.add_exam_marks(0)
    e.show_marks()
    
    