import random
import re
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

class Student():
    MAX_SUB=4

    def __init__(self,id:str,name:str,email:str,password:str):
        self.id=id
        self.name=name
        self.email=email
        self.password=password
        self.subjects:dict[str,Subject]={}# {subid: Subject}

    def __str__(self):
        return self.name
    def enrol(self, subid):# max 4 subj
        if not subid.isdigit() or len(subid)!=3:
            raise ValueError("Subject ID invalid")
        if len(self.subjects)>=Student.MAX_SUB:
            raise ValueError("Max subjects reached")
        if subid in self.subjects:
            raise ValueError("Subject already enrolled")
        mark = int(min(100, max(25, random.gauss(62.5, 15))))
        self.subjects[subid]=(Subject(subid,mark))
    def drop(self, subid):  # check if in subjects
        if not subid.isdigit() or len(subid)!=3:
            raise ValueError("Subject ID invalid")
        try:
            del self.subjects[subid]
        except KeyError:
            raise ValueError("Subject not enrolled")
    def get_avg(self)-> float:
        if len(self.subjects)<Student.MAX_SUB:
            raise ValueError("Not enrolled in all subjects")
        return sum(subject.mark for subject in self.subjects.values())/Student.MAX_SUB
    def check_pass(self)-> bool:
        avg= self.get_avg()
        if avg>= 50:
            return False
        else:
            return True
    def change_password(self,old,new):
        if self.check_password(old)==False:
            raise ValueError("Old password incorrect")
        self.password=new
    def change_name(self,newname):
        self.name=newname
    def check_password(self,password):
        return self.password==password
            
class Subject():
    def __init__(self,id:str,mark:int):
        self.id=id
        self.mark=mark
        self.grade=self.get_grade()
    def get_grade(self)-> str:
        if self.mark>=85:
            return 'HD'
        elif self.mark>=75:
            return 'D'
        elif self.mark>=65:
            return 'C'
        elif self.mark>=50:
            return 'P'
        else:
            return 'F'

class StudentController():# login/register
    def __init__(self,db) -> None:
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
        while True:
            email = input("Email: ")
            password = input("Password: ")
            if email == '' or password == '':
                break
            if re.fullmatch(r'^[A-Za-z0-9._-]+@university.com$',email):
                if re.fullmatch(r'^[A-Z][A-Za-z0-9._-]+[0-9]{3}$',password) and len(password)>=5:
                    try:
                        student = self.db.login(email,password)
                        SubjectController(self.db,student).menu()
                    except ValueError as ve:
                        cprint(ve,'r')
                    break
            cprint("Format of email or password invalid",'r')
    def register(self):
        cprint("Student Sign Up",'g')
        while True:
            email = input("Email: ")
            password = input("Password: ")
            if email == '' or password == '':
                break
            if re.fullmatch(r'^[A-Za-z0-9._-]+@university.com$',email):
                if re.fullmatch(r'^[A-Z][A-Za-z0-9._-]+[0-9]{3}$',password) and len(password)>=5:
                    try:
                        student = self.db.register(email.split('@')[0],email,password)
                        cprint(f"Enrolling Student {student}",'y')
                    except ValueError as ve:
                        cprint(ve,'r')
                        continue
                    SubjectController(self.db,student).menu()
                    break
            cprint("Format of email or password invalid",'r')

class SubjectController():# enrol/drop/show/change password
    def __init__(self,db,student:Student) -> None:
        self.db = db
        self.student = student
    def menu(self):
        while True:
            input_ = input('\033[96mStudent Course System (c/e/r/s/x):\033[0m')
            if input_.lower() == 'c': # change
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
            cprint("Drop cancelled",'y')
            return
        subid = subid.zfill(3)
        if not subid.isdigit() or len(subid)!=3:
            cprint("Subject ID invalid",'r')
            return
        try:
            self.student.drop(subid)
        except ValueError as ve:
            cprint(ve,'r')
        else:
            self.db.datasave(self.student)
            cprint(f"Dropped {subid} successfully",'y')
    def show_subjects(self):
        cprint(f'showing {len(self.student.subjects)} subjects','y')
        for subject in self.student.subjects.values():
            cprint(f"[{subject.id}: mark={subject.mark}, grade={subject.grade}]")
    def change_password(self):
        old = input("Old password: ")
        new = input("New password: ")
        confirm = input("Confirm new password: ")
        if old == '' or new == '':
            cprint("Password change cancelled",'y')
            return
        if new != confirm:
            cprint("Passwords do not match",'r')
            return
        if re.fullmatch(r'^[A-Z][A-Za-z0-9._-]+[0-9]{3}$',new) and len(new)>=5:
            if re.fullmatch(r'^[A-Z][A-Za-z0-9._-]+[0-9]{3}$',new) and len(new)>=5:
                try:
                    self.student.change_password(old,new)
                except ValueError as ve:
                    cprint(ve,'r')
                else:
                    self.db.datasave(self.student)
                    cprint("Password changed successfully",'y')
                return
        cprint('Format of password invalid','r')
    
if __name__ == "__main__":
    from data_manager import Database
    cprint("!!!Student Module Runable Test!!!")
    db = Database()
    sc = StudentController(db)
    email = 'abc@university.com'
    password = 'Pass123'
    try:
            student = db.login(email,password)
            SubjectController(db,student).menu()
    except ValueError as ve:
            cprint(ve)
    sc.menu()