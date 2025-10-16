import random
import re
class Student():
    MAX_SUB=4

    def __init__(self,id,name,email,password):
        self.id=id
        self.name=name
        self.email=email
        self.password=password
        self.subjects={}

    def __str__(self):
        return self.name
    def enrol(self,subid):# max 4 subj
        if len(self.subjects)>=Student.MAX_SUB:
            raise ValueError("Max subjects reached")
        if subid in self.subjects:
            raise ValueError("Subject already enrolled")
        mark = int(min(100, max(25, random.gauss(62.5, 15))))
        self.subjects[subid]=(Subject(subid,mark))
    def drop(self, subid):  # check if in subjects
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
        if self.password!=old:
            raise ValueError("Old password incorrect")
        self.password=new
    def check_password(self,password):
        return self.password==password
            
class Subject():
    def __init__(self,id,mark:int):
        self.id=id
        self.mark=mark
        self.grade=self.get_grade()
    def get_grade(self)-> str:
        if self.mark>=90:
            return 'A'
        elif self.mark>=80:
            return 'B'
        elif self.mark>=70:
            return 'C'
        elif self.mark>=60:
            return 'D'
        else:
            return 'F'

class StudentController():
    def __init__(self) -> None:
        pass
    def menu(self):
        while True:
            input = input('\tStudent System (l/r/x):')
            if input.lower() == 'l':
                self.login()
            elif input.lower() == 'r':
                self.register()
            elif input.lower() == 'x':
                break
            else:
                print("Invalid input")

    def login(self):
        while True:
            email = input("Email: ")
            password = input("Password: ")
            if email == '' or password == '':
                break
            if re.fullmatch(r'^[A-Za-z0-9._-]+@university.com$',email):
                if re.fullmatch(r'^[A-Z][A-Za-z0-9._-]+[0-9]{3}$',password) and len(password)>=5:
                    # if database.check(email,password):
                    #   return student
                    # SubjectController(student).menu()
                    # else:
                    print('Student does not exist')
                    break
            print("Email or password invalid")
    def register(self):
        while True:
            email = input("Email: ")
            password = input("Password: ")
            if email == '' or password == '':
                break
            if re.fullmatch(r'^[A-Za-z0-9._-]+@university.com$',email):
                if re.fullmatch(r'^[A-Z][A-Za-z0-9._-]+[0-9]{3}$',password) and len(password)>=5:
                    # database.register(email,password)
                    break
            print("Email or password invalid")

class SubjectController():
    def __init__(self,student:Student) -> None:
        self.student = student
    def menu(self):
        while True:
            input = input('\t\tStudent Course System (c/e/r/s/x):')
            if input.lower() == 'c': # change
                old = input("Old password: ")
                new = input("New password: ")
                if old == '' or new == '':
                    print("Password change cancelled")
                    continue
                if re.fullmatch(r'^[A-Z][A-Za-z0-9._-]+[0-9]{3}$',new) and len(new)>=5:
                    if re.fullmatch(r'^[A-Z][A-Za-z0-9._-]+[0-9]{3}$',new) and len(new)>=5:
                        print('password valid')
                        continue
                self.change_password(old,new)
            elif input.lower() == 'e':# enrol
                pass
            elif input.lower() == 'r':# remove
                pass
            elif input.lower() == 's':# show
                self.show_subjects()
            elif input.lower() == 'x':
                # save student data
                break
            else:
                print("Invalid input")
                
    def show_subjects(self):
        print(f'showing {len(self.student.subjects)} subjects')
        for subject in self.student.subjects.values():
            print(f"[{subject.id}: mark={subject.mark}, grade={subject.grade}]")
    def change_password(self,old,new):
        try:
            self.student.change_password(old,new)
        except ValueError as ve:
            print(ve)
        else:
            print("Password changed successfully")
    
