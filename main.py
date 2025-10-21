import student
from data_manager import Database
import admin
import admin
print("Loaded admin from:", getattr(admin, "__file__", "?"))
print("has AdminController:", hasattr(admin, "AdminController"))

def menu():
    while True:
        input_ = input("University System:(A)dmin, (S)tudent, or X:")
        if input_.lower() == 'a':
            db = Database()
            admin.AdminController(db).menu()
        elif input_.lower() == 's':
            db = Database()
            student.StudentController(db).menu()
        elif input_.lower() == 'x':
            print("Thank you")
            break
        else:
            print("Invalid input")

if __name__ == "__main__":
    menu()