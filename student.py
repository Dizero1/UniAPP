import random

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
    def show_subjects(self):
        for subject in self.subjects.values():
            print(f"[{subject.id}: mark={subject.mark}, grade={subject.grade}]")
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
    def check_pass(self):
        if len(self.subjects)<Student.MAX_SUB:
            print("Not enrolled in all subjects")
            return False
        total=0
        for subject in self.subjects.values():
            total += subject.mark
        if total>= 50*Student.MAX_SUB:
            print(f"passed wtih average mark {total/Student.MAX_SUB:.2f}")
            return True
        else:
            print(f"failed wtih average mark {total/Student.MAX_SUB:.2f}")
            return False
    def change_password(self,old,new):
        if self.password!=old:
            raise ValueError("Old password incorrect")
        self.password=new

class Subject():
    def __init__(self,id,mark:int):
        self.id=id
        self.mark=mark
        self.grade=self.get_grade()
    def get_grade(self):
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