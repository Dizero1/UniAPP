import json
from typing import Dict, List, Tuple

# ANSI color codes for CLI output
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
    # 成绩区间（如作业有特别要求可在此调整）
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

    # -------------- 主菜单（与样例提示一致的小写顺序） --------------
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

    # -------------- 持久化 --------------
    def _persist(self):
        if hasattr(self.db, "save"):
            self.db.save()
        else:
            path = getattr(self.db, "PATH", "students.data")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.db.data, f, indent=2)

    # -------------- 清空数据库 --------------
    def _clear_database(self):
        confirm = input(f"{C.WARNING}Are you sure you want to clear all students? (y/n): {C.ENDC}").strip().lower()
        if confirm == "y":
            self.db.data = {}
            self._persist()
            print(f"{C.FAIL}All students removed. Database cleared.{C.ENDC}")
        else:
            print(f"{C.OKBLUE}Cancelled. No changes made.{C.ENDC}")

    # -------------- 学生列表（与样例格式一致） --------------
    def _show_students(self):
        if not self.db.data:
            print(f"{C.WARNING}No students found.{C.ENDC}")
            return
        # 标题颜色
        print(f"{C.OKGREEN}Student List{C.ENDC}")
        # 稳定排序：先 name 再 id
        for sid, info in sorted(self.db.data.items(), key=lambda kv: (kv[1].get("name",""), kv[0])):
            name = info.get("name", "")
            email = info.get("email", "")
            # John Smith :: 673358 --> Email: john.smith@university.com
            print(f"{name} :: {sid} --> Email: {email}")

    # -------------- 成绩分组（与样例的 Grade Grouping 一致） --------------
    def _group_students(self):
        if not self.db.data:
            print(f"{C.WARNING}No students to group.{C.ENDC}")
            return

        print(f"{C.OKGREEN}Grade Grouping{C.ENDC}")

        buckets: Dict[str, List[str]] = {"HD": [], "D": [], "C": [], "P": [], "F": []}
        for sid, info in self.db.data.items():
            name = info.get("name", "")
            avg, grade = _avg_and_grade(info)
            # John Smith :: 673358 --> GRADE:  C  -  MARK:  68.25
            item = f"{name} :: {sid} --> GRADE:  {grade}  -  MARK:  {avg:.2f}"
            if grade in buckets:
                buckets[grade].append(item)

        # 只打印非空分组，顺序：HD, D, C, P, F
        for g in ["HD", "D", "C", "P", "F"]:
            if not buckets[g]:
                continue
            inside = ", ".join(buckets[g])
            # P  --> [ ... ]
            print(f"{g}  --> [{inside}]")

    # -------------- PASS/FAIL 分区（与样例 PASS/FAIL Partition 一致） --------------
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

        # 与样例一样先 FAIL 再 PASS，空集显示 []
        print(f"FAIL --> [{', '.join(fail_list)}]" if fail_list else "FAIL --> []")
        print(f"PASS --> [{', '.join(pass_list)}]" if pass_list else "PASS --> []")

    # -------------- 删除学生 --------------
    def _remove_student(self):
        sid = input("Enter the student ID to remove: ").strip()
        if sid in self.db.data:
            del self.db.data[sid]
            self._persist()
            print(f"{C.OKGREEN}Student {sid} removed.{C.ENDC}")
        else:
            print(f"{C.FAIL}Student ID not found.{C.ENDC}")
