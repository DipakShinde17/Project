
import getpass
from colorama import Fore,Style
from Stu_functions import StuManage 

class Admin1:
    def __init__(self):
        user_name = input('Enter Username: ')
        passw = getpass.getpass('Enter Password: ')
        print("---------------------------------------------------------------------")
        if(user_name == 'admin' and passw == '12345'):
            print(Fore.GREEN+"✅ Login sucessfully...."+Style.RESET_ALL)
        

            ch = ' '
            while(ch != "10"):
                print("=======================================================================")
                print('''Please select choice: 
                    1.Add Students
                    2.Update Students
                    3.Delete Students
                    4.Show Students
                    5.Mark Students 
                    6.View Attendance By Date
                    7.View Attendance By Name
                    8.Add Notice
                    9.Add Exam Mark
                    10.Exite''')
                ch = input('Enter choice: ')
                if(ch == '1'):
                    e = StuManage()
                    # e.AddStu()
                    e.AddStu() 

                if(ch == '2'):
                    e = StuManage()
                    e.UpdStu()
                    
                if(ch == '3'):
                    e = StuManage()
                    e.DelStu()

                if(ch == '4'):
                    e = StuManage()
                    e.ShowAllStu()

                if(ch == '5'):
                    e = StuManage()
                    e.markAt()

                if(ch == '6'):
                    e = StuManage()
                    e.viewDate()

                if(ch == '7'):
                    e = StuManage()
                    e.viewName()
                    
                if(ch == '8'):
                    e = StuManage()
                    e.Add_notice()
                
                if(ch == '9'):
                    e = StuManage()
                    e.add_exam_marks()
                
        
        else:
                print('Please enter correct details...')
            