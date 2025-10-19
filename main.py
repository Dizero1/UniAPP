import student
from data_manager import Database
import admin
def menu():
    while True:
        input_ = input("University System:(A)dmin, (S)tudent, or X:")
        if input_.lower() == 'a':
            db = Database()
            # AdminController(db).menu()
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