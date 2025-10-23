import random
import re
from data import Database, Student, Subject

PASSWORD_REGEX = r'^[A-Z][A-Za-z]{4,}[0-9]{3,}$'
EMAIL_REGEX = r'^[A-Za-z0-9._-]+@university.com$'
def cprint(text,color:str='default'):
    colors = {
        'default':'\033[0m',
        'r':'\033[91m',
        'g':'\033[92m',
        'y':'\033[93m',
        'b':'\033[94m',
        'c':'\033[96m',
        'w':'\033[97m',
    }
    print(f"{colors.get(color,'\033[0m')}{text}{colors['default']}")

class StudentController():# login/register
    def __init__(self,db:Database) -> None:
        self.db = db
    def menu(self):
        while True:
            input_ = input('\033[96mStudent System (l/r/x):\033[0m')
            if input_.lower() == 'l':
                self.login()
            elif input_.lower() == 'r':
                self.register()
            elif input_.lower() == 'x':
                break
            else:
                cprint("Invalid input",'r')

    def login(self):
        cprint("Student Login",'g')
        while True:
            email = input("Email: ")
            password = input("Password: ")
            if email == '' or password == '':
                cprint("Login cancelled",'y')
                break
            email_ok = re.fullmatch(EMAIL_REGEX, email)
            pwd_ok = re.fullmatch(PASSWORD_REGEX, password)
            if not email_ok or not pwd_ok:
                cprint("Format of email or password invalid",'r')
                continue
            try:
                student = self.db.login(email,password)
            except ValueError as ve:
                cprint(ve,'r')
            else:
                cprint(f"Login successful, welcome {student}",'y')
                SubjectController(self.db, student).menu()  

            break
    def register(self):
        cprint("Student Sign Up",'g')
        while True:
            email = input("Email: ")
            password = input("Password: ")
            if email == '' or password == '':
                cprint("Registration cancelled",'y')
                break
            # validate email and password formats
            email_ok = re.fullmatch(EMAIL_REGEX, email)
            pwd_ok = re.fullmatch(PASSWORD_REGEX, password)
            if not email_ok or not pwd_ok:
                cprint("Format of email or password invalid",'r')
                continue
            if self.db.check_student_exists(email):
                cprint("Email already registered",'r')
                return
            try:
                username = input("Name: ")
                cprint(f"Registering Student {username}",'y')
                student = self.db.register(username, email, password)
            except ValueError as ve:
                cprint(str(ve),'r')
                continue
            else:
                SubjectController(self.db, student).menu()

            break

class SubjectController():# enrol/drop/show/change password
    def __init__(self,db:Database,student:Student) -> None:
        self.db = db
        self.student = student
    def menu(self):
        while True:
            input_ = input('\033[96mStudent Course System (c/e/r/s/x):\033[0m')
            if input_.lower() == 'c': # change password
                self.change_password()
            elif input_.lower() == 'e':# enrol
                self.enrol()
            elif input_.lower() == 'r':# remove
                self.remove()
            elif input_.lower() == 's':# show
                self.show_subjects()
            elif input_.lower() == 'x':
                self.db.datasave(self.student)
                break
            else:
                cprint("Invalid input",'r')

    def enrol(self):
        subid = input("Subject ID: ")
        if subid == '':
            cprint("Enrol cancelled",'y')
            return
        if subid == 'r':
            subid = str(random.randint(1,999))
        subid = subid.zfill(3)
        try:
            self.student.enrol(subid)
        except ValueError as ve:
            cprint(ve,'r')
        else:
            self.db.datasave(self.student)
            cprint(f"Enrolled in {subid} successfully, {len(self.student.subjects)} of 4",'y')
    def remove(self):
        subid = input("Subject ID: ")
        if subid == '':
            cprint("Remove cancelled",'y')
            return
        if not subid.isdigit():
            cprint("Subject ID invalid",'r')
            return
        subid = subid.zfill(3)
        if len(subid) != 3:
            cprint("Subject ID invalid",'r')
            return
        try:
            self.student.drop(subid)
        except ValueError as ve:
            cprint(ve,'r')
        else:
            self.db.datasave(self.student)
    def show_subjects(self):
        cprint(f'showing {len(self.student.subjects)} subjects','y')
        for subject in self.student.subjects.values():
            cprint(f"[{subject.id:<5} | mark={subject.mark:<3} | grade={subject.grade:<2}]")
    def change_password(self):
        old = input("Old password: ")
        if old == '':
            cprint("Password change cancelled",'y')
            return
        new = input("New password: ")
        confirm = input("Confirm new password: ")
        if new != confirm:
            cprint("Passwords do not match",'r')
            return
        if not re.fullmatch(PASSWORD_REGEX, new):
            cprint('Format of password invalid','r')
            return
        try:
            self.student.change_password(old,new)
        except ValueError as ve:
            cprint(ve,'r')
        else:
            self.db.datasave(self.student)
            cprint("Password changed successfully",'y')
    
if __name__ == "__main__":
    from data import Database
    cprint("!!!Student Module Runable Test!!!")
    db = Database()
    sc = StudentController(db)
    sc.menu()