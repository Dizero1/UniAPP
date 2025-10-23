import os
import json
import random

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
        if not subid.isdigit() or len(subid)!=3 or subid=='000':
            raise ValueError("Subject ID invalid")
        if len(self.subjects)>=Student.MAX_SUB:
            raise ValueError("Max subjects reached")
        if subid in self.subjects:
            raise ValueError("Subject already enrolled")
        mark = int(min(100, max(25, random.gauss(62.5, 15))))
        self.subjects[subid]=(Subject(subid,mark))
    def drop(self, subid):  # check if in subjects
        if not subid.isdigit() or len(subid)!=3 or subid=='000':
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
    def check_password(self,password)->bool:
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

class Database():
    PATH = 'students.data'
    data = {}# {id: {name,email,password,subjects:{subid:{id,mark,grade}}}}
    def __init__(self) -> None:
        if os.path.exists(self.PATH):
            self.load()
        else:
            with open(self.PATH,'w') as f:
                json.dump({},f) 
            self.load()
    def load(self):
        with open(self.PATH,'r') as f:
            self.data = json.load(f)
    def save(self):
        with open(self.PATH,'w') as f:
            json.dump(self.data,f)
    def datasave(self,student: Student):
        if Student:
            self.data[student.id]={
                'name':student.name,
                'email':student.email,
                'password':student.password,
                'subjects':{subid:{
                    'mark':subject.mark
                } for subid,subject in student.subjects.items()}
            }
        self.save()
    def clear(self):
        self.data = {}
        self.save()
    def login(self,email:str,password:str)->Student:
        for id,info in self.data.items():
            if info['email']==email and info['password']==password:
                student = Student(id,info['name'],info['email'],info['password'])
                for subid,subinfo in info.get('subjects',{}).items():
                    subject = Subject(subid,subinfo['mark'])
                    student.subjects[subid]=subject
                return student
        raise ValueError("Email or password not correct")
    def register(self,name:str,email:str,password:str)->Student: # return Student
        if self.check_student_exists(email):
            raise ValueError("Email already registered")
        id = self.ruid()
        self.data[id]={'name':name,'email':email,'password':password,'subjects':{}}
        self.save()
        return Student(id,name,email,password)
    def check_student_exists(self,email:str)-> bool:
        return any(info['email']==email for info in self.data.values())
    def ruid(self):
        counter = 0
        while True:
            num = random.randint(1, 999999)
            uid = str(num).zfill(6)
            counter += 1
            if counter > 100000:
                raise RuntimeError("Failed to generate unique ID")
            if uid not in self.data:
                return uid