from prettytable import PrettyTable
from colorama import Fore,Style
from attendance import AttendanceManage
from stu import Studentt
from extra import Extra


class StuManage():
    
    def is_id_unique(self, student_id):
        """Return True if student_id is NOT present in the file (unique)."""
        filepath = 'zProject/Stu_Details.txt'
        if not filepath:
            return True  # file doesn't exist -> ID is unique

        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  # skip blank lines

                # split on comma only, then strip spaces around fields
                parts = [p.strip() for p in line.split(',')]
                if not parts:
                    continue

                # parts[0] should be the ID; compare as strings
                if parts[0] == str(student_id):
                    return False  # ID found -> not unique
        return True
    
    def AddStu(self):
        try:

            while True:
                print("----------------------------------------------------------------------------")
                id = int(input(Fore.YELLOW + 'Enter Student ID: '))
                if self.is_id_unique(id):
                    # name.split(',')

                    while True:
                        name = input("Enter Student Name: ") 
                        if all(ch.isalpha() or ch.isspace() for ch in name) and name.strip() != "":
                            break
                        else:
                            print(Fore.RED + "❌ Name must contain only letters. Try again." + Style.RESET_ALL)

                    while True:
                        clas = input('Enter Student Class: ')
                        if all(ch.isalpha() or ch.isspace() for ch in clas) and clas.strip() != "": #isalpha use to letter and isspace use to 
                            break
                        else:
                            print(Fore.RED + "❌ Name must contain only letters. Try again." + Style.RESET_ALL)

                    while True:
                        dept = input('Enter Department: ')
                        print("-----------------------------------------------------------------------")
                        if all(ch.isalpha() or ch.isspace() for ch in dept) and dept.strip() != "":
                            break
                        else:
                            print(Fore.RED+ "❌ Department must contain only letter. Try again" +Style.RESET_ALL)
                        
                    e1 = Studentt(id, name, clas, dept)
                    eData = str(e1)

                    with open('zProject/Stu_Details.txt', 'a') as fp:
                        fp.write(eData + '\n' )

                    print(Fore.GREEN + '✅ Student Added Successfully!\n' + Style.RESET_ALL)
                    break
                else:
                    print(Fore.RED + '❌ Student ID already exists. Please try again.' + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + 'Error:', e)


    def UpdStu(self):
        try:
            print("-------------------------------------------------------------------")
            StuData = []
            
            id = input(Fore.YELLOW+"Enter Student Id: ")
            chkId = False

            with open('zProject/Stu_Details.txt','r') as fp:
                for eStr in fp:
                    # print(eStr)
                    eList = eStr.split(',')
                    if (id == eList[0]):
                        chkId = True
                        chk = input('Do you want to change the name: ')
                        if(chk.lower() in ['yes','y']):
                            eList[1] = input('Enter New Name: ')
                        chk = input('Do you want to change Class (y/n: )')
                        if(chk.lower() in ['y','yes']):
                            eList[2] = input('Enter new Class: ')
                        chk = input('Do you want to change department (y/n): ')
                        if(chk.lower() in ['yes','y']):
                            eList[3] = input("Enter new department: ")+ '\n'
                        eStr = f'{eList[0]},{eList[1]},{eList[2]},{eList[3]}'+Style.RESET_ALL
                    
                    StuData.append(eStr)
            if (chkId):
                with open('zProject/Stu_Details.txt','w') as fp:
                    for eStr in StuData:
                        fp.write(eStr)
                print("-------------------------------------------------------------------")
                print(Fore.GREEN+'✅ Student Update Sucessfully...'+Style.RESET_ALL)
                        
            else:
                print(f'{id} is not found')
        except ValueError:
            print("Enter valid details")

    def DelStu(self):
        
            try:
                print("------------------------------------------------------------------")
                id_to_delete = input(Fore.YELLOW+"Enter Student ID to delete: "+Style.RESET_ALL)
                found = False
                new_lines = []

                with open('zProject/Stu_Details.txt', 'r') as fp:
                    lines = fp.readlines()

                for line in lines:
                    data = line.strip().split(',')
                    if data[0] != id_to_delete:
                        new_lines.append(line)
                    else:
                        found = True

                if found:
                    with open('zProject/Stu_Details.txt', 'w') as fp:
                        fp.writelines(new_lines)
                    print('--------------------------------------------------------------')
                    print(Fore.GREEN+f'🗑️  Student with ID {id_to_delete} deleted successfully.'+Style.RESET_ALL)
                else:
                    print(f'⚠️ No student found with ID {id_to_delete}.')
            except FileNotFoundError:
                print("❌ Error: File not found. Make sure 'Stu_Datails.txt' exists.")
            except Exception as e:
                print('❌ Error:', e)
        
    def ShowAllStu(self):
        try:
            print("=============================🎓 STUDENT LIST 🎓=============================")
            print(Fore.CYAN+"")
            with open('zProject/Stu_Details.txt', 'r') as fp:
                lines = fp.read().strip().split('\n')
            if not lines:
                print("⚠️ No student data to show.")
                return
            
            # Create the table
            table = PrettyTable()
            table.field_names = ["ID", "Name", "Class", "Department"]

            # Process each student record
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) >= 4:
                    id = parts[0].strip()
                    name = parts[1].strip()
                    clas = parts[2].strip()
                    dept = parts[3].strip()
                    table.add_row([id, name, clas, dept])

            print(table)
            print(""+Style.RESET_ALL)
        except FileNotFoundError:
            print("❌ File not found. Please add a student first.")
        except Exception as e:
            print("❌ Error:", e)

    def markAt(self):
        Ab = AttendanceManage()
        Ab.MarkAttendance()

    def viewDate(self):
        Ab = AttendanceManage()
        Ab.ViewAttendanceByDate()

    def viewName(self):
        Ab = AttendanceManage()
        Ab.ViewAttendanceByName()

    def Add_notice(self):
        e = Extra()
        e.add_notice()
    def add_exam_marks(self):
        e = Extra()
        e.add_exam_marks()
    
if __name__ == '__main__':
    e = StuManage()
    e.ShowAllStu()
    # e.AddStu()
    # e.UpdStu()
    # e.DelStu()
