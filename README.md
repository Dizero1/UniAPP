# UniAPP
## Assignment for 32555
Created by
- 25040433 Cheng Chi 
- 25940608 Leyang Cheng 
- 25661113 Qi Li 
- 13820182 Zhaofeng He 

## Project Abstract
A local university wants to develop a new interactive system – CLIUniApp - that offers access totwo interactive subsystems for students and admins separately. CLIUniApp stores students’ data intoa local file students.data, with all CRUD operations interacting with this file.Students accessing the student subsystem have the choice to login (if they are previously registered)or register. A registered student can enrol in a maximum of four (4) subjects, remove a subject,change password, and view enrolment.Admins already exist in the system and do not need to register. An admin using the admin subsystemcan remove a student from the students.data, partition students to PASS/FAIL categories, groupstudents by grade, view all students, and clear all student data.

## System Requirement
- Python 3.8 or higher.
- Requirements are standard libraries: *os, json, random, re, etc.* GUI requires *tkinter*.

## How to Run
First, clone or copy repository to local directory.
  ```sh
  git clone https://github.com/Dizero1/UniAPP
  ```
- CLI:
  ```sh
  python main.py
  ```
  This shows the main menu where you can choose Admin (A), Student (S), or Exit (X).

- GUI:
  ```sh
  python gui.py
  ```
  Opens a tkinter login window. Use registered email and password to log in and manage courses.

## Configurations
- Data file path: controlled by a constant PATH = 'students.data' in data.py — edit to change storage location.
- Validation rules: email and password regexes are defined in controller.py and gui.py:
  - EMAIL_REGEX
  - PASSWORD_REGEX

## Notes and Security
- students.data contains sensitive information (plain-text passwords). For production or real-world use, store passwords securely (salted hashing).
- Some behaviors (e.g., admin without authentication, plain-text password storage) are for learning/assignment purposes only. Add proper authentication and security for real use.