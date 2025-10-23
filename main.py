import controller
from data import Database
import admin

def menu():
    while True:
        input_ = input("\033[96mUniversity System:(A)dmin, (S)tudent, or X:\033[0m")
        if input_.lower() == 'a':
            db = Database()
            admin.AdminController(db).menu()
        elif input_.lower() == 's':
            db = Database()
            controller.StudentController(db).menu()
        elif input_.lower() == 'x':
            print("\033[93mThank you\033[0m")
            break
        else:
            print("\033[91mInvalid input\033[0m")

if __name__ == "__main__":
    menu()