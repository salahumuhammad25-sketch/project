import sqlite3

conn = sqlite3.connect("student.db")
cursor = conn.cursor()

# Admin Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Admin(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
''')

# teacher table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Teacher(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT,
       username TEXT UNIQUE,
       password TEXT
    )
''')

# Student Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Student(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        username TEXT UNIQUE, 
        password TEXT,
        course TEXT,
        FOREIGN KEY(course) REFERENCES Courses(course_name)
    )
''')
# Grades Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Grades(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject TEXT,
        grade TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_name TEXT
     )
''' )

cursor.execute('DROP TABLE IF EXISTS Courses')
conn.commit()

cursor.execute('INSERT OR IGNORE INTO Admin (username, password) VALUES (?, ?)', ('admin', 'admin123'))


conn.commit()
conn.close()

def Admin_login():
     try:
        print("\n-- Admin Login --")
        username = input("enter admin username: ")
        password = getpass.getpass("enter admin password: ")
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Admin WHERE username = ? AND password = ?', (username, password))
        data = cursor.fetchone()
        conn.close()

        if data:
          print("\n Admin login success\n")
          Admin_menu()
        else:
          print("\n Invalid credentials\n")

     except Exception as e:
       print("An error occurred:", e)


def Teacher_login():
     try:
        username = input("enter teacher username: ")
        password = getpass.getpass("enter teacher password: ")
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Teacher WHERE username = ? AND password = ?', (username, password))
        data = cursor.fetchone()
        conn.close() 

        if data:
         print("\n Teacher login success\n")
         Teacher_menu(data[0], data[1])
        else:
         print("\n Invalid credentials\n")
     except Exception as e:
        print("An error occurred:", e)   


def Student_login():
    try:
        username = input("enter student username: ")
        password = getpass.getpass("enter student password: ")
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Student WHERE username = ? AND password = ?', (username, password))
        data = cursor.fetchone()
        conn.close()

        if data:
         print("\n Student login success\n")
         Student_menu(data[0], data[1])
        else:
         print("\n Invalid credentials\n")
    except Exception as e:
       print("An error occurred:", e)


def register_Teacher():
    try:
        name = input("Enter teacher name: ")
        username = input("Enter teacher username: ")
        password = getpass.getpass("Enter teacher password: ")
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Teacher (name, username, password) VALUES (?, ?, ?)', (name, username, password))
        conn.commit()
        conn.close()
        print("\n Teacher registered successfully\n")
    except sqlite3.IntegrityError:
        print("\n Username already exists. Please choose a different username.\n")
    except Exception as e:
        print("An error occurred:", e)   

def register_Student():
    try:
        name = input("Enter student name: ")
        username = input("Enter student username: ")
        password = getpass.getpass("Enter student password: ")
        # course = input("Enter course enrolled: ")
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Student (name, username, password) VALUES (?, ?, ?)', (name, username, password))
        # student_id = cursor.lastrowid
        # cursor.execute('INSERT INTO Courses (course_name, student_id) VALUES (?, ?)', (student_id, course))
        conn.commit()
        conn.close()
        print("\n Student registered successfully\n")
    except sqlite3.IntegrityError:
        print("\n Username already exists. Please choose a different username.\n")
    except Exception as e:
        print("An error occurred:", e)


def Admin_menu():
    while True:
        print("1. View Teacher")
        print("2. View Student")
        print("3.View Grades")
        print("4. Logout")
        choice = input("Enter your choice: ")
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        if choice == '1':
            cursor.execute('SELECT id , name , username FROM Teacher')
            rows = cursor.fetchall()
            print("\n--- Teacher List---:")
            print(" ID | Name    | Username ")
            print("---------------------------")
            for row in rows:
                teacher_id, name, username = row
                print(f" {teacher_id:<2} | {name:<8} | {username} ")
                print("---------------------------")

        elif choice == '2':
            cursor.execute('SELECT id , name , username FROM Student')
            rows = cursor.fetchall()
            print("\n--- Student List---:")
            print(" ID | Name    | Username ")
            print("---------------------------")
            for row in rows:
                student_id, name, username = row
                print(f" {student_id:<2} | {name:<8} | {username} ")
                print("---------------------------")

        elif choice == '3':
            cursor.execute('SELECT * FROM Grades')
            rows = cursor.fetchall()
            print("\n--- Grades List---:")
            print(" ID | Student ID | Subject | Grade ")
            print("-------------------------------------")
            for row in rows:
                grade_id, student_id, subject, grade = row
                print(f" {grade_id:<2} | {student_id:<10} | {subject:<7} | {grade} ")
                print("-------------------------------------")

        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

        conn.close()



def Teacher_menu(teacher_id, teacher_name):
    while True:
        print("1. View Students")
        print("2. Assign Grades")
        print("3. Logout")
        choice = input("Enter your choice: ")
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        if choice == '1':
            cursor.execute('SELECT id , name , username FROM Student')
            rows = cursor.fetchall()
            print("\n--- Student List---:")
            print(" ID | Name    | Username ")
            print("---------------------------")
            for row in rows:
                student_id, name, username = row
                print(f" {student_id:<2} | {name:<8} | {username} ")
            print("---------------------------")

        elif choice == '2':
            student_id = input("Enter Student ID: ")
            subject = input("Enter Subject: ")
            grade = input("Enter Grade: ")
            cursor.execute('INSERT INTO Grades (student_id, subject, grade) VALUES (?, ?, ?)', (student_id, subject, grade))
            conn.commit()
            print("\n Grade assigned successfully\n")

        elif choice == '3':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

        conn.close()

           

def Student_menu(student_id, student_name):
    while True:
        print("1. View Grades")
        print("2. Logout")
        choice = input("Enter your choice: ")
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        if choice == '1':
            cursor.execute('SELECT subject, grade FROM Grades WHERE student_id = ?', (student_id,))
            rows = cursor.fetchall()
            print("\n Your Grades:")
            for row in rows:
                print(row)

        elif choice == '2':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

        conn.close()


import getpass
def main_menu():
    while True:
        print("1. Admin Login")
        print("2. Teacher Login")
        print("3. Student Login")
        print("4. Register Teacher")
        print("5. Register Student")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            Admin_login()
        elif choice == '2':
            Teacher_login()
        elif choice == '3':
            Student_login()
        elif choice == '4':
            register_Teacher()
        elif choice == '5':
            register_Student()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")  


main_menu()


                              