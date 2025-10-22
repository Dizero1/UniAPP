import json
from typing import Dict, List, Tuple


class C:
    HEADER   = "\033[95m"
    OKBLUE   = "\033[94m"
    OKCYAN   = "\033[96m"
    OKGREEN  = "\033[92m"
    WARNING  = "\033[93m"
    FAIL     = "\033[91m"
    ENDC     = "\033[0m"
    BOLD     = "\033[1m"
    UNDER    = "\033[4m"

def _grade_for_mark(mark: int) -> str:
    if mark >= 85: return "HD"
    if mark >= 75: return "D"
    if mark >= 65: return "C"
    if mark >= 50: return "P"
    return "F"

def _avg_and_grade(student_record: dict) -> Tuple[float, str]:
    subs = student_record.get("subjects", {}) or {}
    if not subs:
        return 0.0, "N/A"
    marks = [int(s.get("mark", 0)) for s in subs.values()]
    avg = sum(marks) / len(marks)
    return avg, _grade_for_mark(int(avg))

class AdminController:
    """
    Admin System
    (c) clear database
    (g) group students
    (p) partition students
    (r) remove student
    (s) show
    (x) exit
    """
    def __init__(self, db):
        self.db = db
        if hasattr(self.db, "load"):
            self.db.load()

    def menu(self):
        while True:
            print(f"{C.OKCYAN}Admin System (c/g/p/r/s/x): {C.ENDC}", end="")
            choice = input().strip().lower()
            if choice == "c":
                self._clear_database()
            elif choice == "g":
                self._group_students()
            elif choice == "p":
                self._partition_students()
            elif choice == "r":
                self._remove_student()
            elif choice == "s":
                self._show_students()
            elif choice == "x":
                print(f"{C.OKGREEN}Returning to the University System...{C.ENDC}")
                break
            else:
                print(f"{C.WARNING}Invalid input{C.ENDC}")


    def _persist(self):
        if hasattr(self.db, "save"):
            self.db.save()
        else:
            path = getattr(self.db, "PATH", "students.data")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.db.data, f, indent=2)

  
    def _clear_database(self):
        confirm = input(f"{C.WARNING}Are you sure you want to clear all students? (y/n): {C.ENDC}").strip().lower()
        if confirm == "y":
            self.db.data = {}
            self._persist()
            print(f"{C.FAIL}All students removed. Database cleared.{C.ENDC}")
        else:
            print(f"{C.OKBLUE}Cancelled. No changes made.{C.ENDC}")

    def _show_students(self):
        if not self.db.data:
            print(f"{C.WARNING}No students found.{C.ENDC}")
            return

        print(f"{C.OKGREEN}Student List{C.ENDC}")
        
        for sid, info in sorted(self.db.data.items(), key=lambda kv: (kv[1].get("name",""), kv[0])):
            name = info.get("name", "")
            email = info.get("email", "")
          
            print(f"{name} :: {sid} --> Email: {email}")

    def _group_students(self):
        if not self.db.data:
            print(f"{C.WARNING}No students to group.{C.ENDC}")
            return

        print(f"{C.OKGREEN}Grade Grouping{C.ENDC}")

        buckets: Dict[str, List[str]] = {"HD": [], "D": [], "C": [], "P": [], "F": []}
        for sid, info in self.db.data.items():
            name = info.get("name", "")
            avg, grade = _avg_and_grade(info)
            
            item = f"{name} :: {sid} --> GRADE:  {grade}  -  MARK:  {avg:.2f}"
            if grade in buckets:
                buckets[grade].append(item)

        for g in ["HD", "D", "C", "P", "F"]:
            if not buckets[g]:
                continue
            inside = ", ".join(buckets[g])
            # P  --> [ ... ]
            print(f"{g}  --> [{inside}]")

  
    def _partition_students(self):
        if not self.db.data:
            print(f"{C.WARNING}No students to partition.{C.ENDC}")
            return

        print(f"{C.OKGREEN}PASS/FAIL Partition{C.ENDC}")

        pass_list: List[str] = []
        fail_list: List[str] = []
        for sid, info in self.db.data.items():
            name = info.get("name", "")
            avg, grade = _avg_and_grade(info)
            item = f"{name} :: {sid} --> GRADE:  {grade}  -  MARK:  {avg:.2f}"
            if avg >= 50:
                pass_list.append(item)
            else:
                fail_list.append(item)

        
        print(f"FAIL --> [{', '.join(fail_list)}]" if fail_list else "FAIL --> []")
        print(f"PASS --> [{', '.join(pass_list)}]" if pass_list else "PASS --> []")

    
    def _remove_student(self):
        sid = input("Enter the student ID to remove: ").strip()
        if sid in self.db.data:
            del self.db.data[sid]
            self._persist()
            print(f"{C.OKGREEN}Student {sid} removed.{C.ENDC}")
        else:
            print(f"{C.FAIL}Student ID not found.{C.ENDC}")
