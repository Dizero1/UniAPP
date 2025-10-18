import os
import json
import random
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
    def clear(self):
        self.data = {}
        self.save()
    def login(self,email:str,password:str):
        for id,info in self.data.items():
            if info['email']==email and info['password']==password:
                from student import Student, Subject
                student = Student(id,info['name'],info['email'],info['password'])
                for subid,subinfo in info.get('subjects',{}).items():
                    subject = Subject(subid,subinfo['mark'])
                    student.subjects[subid]=subject
                return student
        raise ValueError("Email or password not correct")
    def register(self,name,email,password): # return Student
        if any(info['email']==email for info in self.data.values()):
            raise ValueError("Email already registered")
        id = self.ruid()
        self.data[id]={'name':name,'email':email,'password':password,'subjects':{}}
        self.save()
        from student import Student
        return Student(id,name,email,password)
    def ruid(self):
        while True:
            num = random.randint(1, 999999)
            uid = str(num).zfill(6)
            if uid not in self.data:
                return uid