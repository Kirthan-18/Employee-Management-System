import sqlite3

conn = sqlite3.connect('employee.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS employee (
    emp_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL NOT NULL
)
''')
conn.commit()


def add_employee():
    print("\n--- Add Employee ---")
    emp_id = int(input("Enter Employee ID: "))
    name = input("Enter Employee Name: ")
    dept = input("Enter Department: ")
    salary = float(input("Enter Salary: "))

    try:
        cursor.execute("INSERT INTO employee (emp_id, name, department, salary) VALUES (?, ?, ?, ?)",
                       (emp_id, name, dept, salary))
        conn.commit()
        print("✅ Employee added successfully!\n")
    except sqlite3.IntegrityError:
        print("❌ Employee ID already exists. Please try again.\n")


def view_all_employees():
    print("\n--- All Employee Records ---")
    cursor.execute("SELECT * FROM employee")
    rows = cursor.fetchall()

    if not rows:
        print("No records found.\n")
    else:
        print("ID\tName\t\tDepartment\tSalary")
        print("-" * 40)
        for row in rows:
            print(f"{row[0]}\t{row[1]:<15}{row[2]:<15}{row[3]:.2f}")
        print()


def search_employee():
    emp_id = int(input("\nEnter Employee ID to search: "))
    cursor.execute("SELECT * FROM employee WHERE emp_id = ?", (emp_id,))
    row = cursor.fetchone()

    if row:
        print("\nEmployee Found:")
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Department: {row[2]}")
        print(f"Salary: {row[3]:.2f}\n")
    else:
        print("❌ Employee not found.\n")


def update_employee():
    emp_id = int(input("\nEnter Employee ID to update: "))
    cursor.execute("SELECT * FROM employee WHERE emp_id = ?", (emp_id,))
    if cursor.fetchone() is None:
        print("❌ Employee not found.\n")
        return

    print("1. Update Department")
    print("2. Update Salary")
    choice = input("Enter choice: ")

    if choice == "1":
        new_dept = input("Enter new Department: ")
        cursor.execute("UPDATE employee SET department = ? WHERE emp_id = ?", (new_dept, emp_id))
    elif choice == "2":
        new_salary = float(input("Enter new Salary: "))
        cursor.execute("UPDATE employee SET salary = ? WHERE emp_id = ?", (new_salary, emp_id))
    else:
        print("Invalid choice.\n")
        return

    conn.commit()
    print("✅ Employee record updated successfully!\n")


def delete_employee():
    emp_id = int(input("\nEnter Employee ID to delete: "))
    cursor.execute("DELETE FROM employee WHERE emp_id = ?", (emp_id,))
    conn.commit()
    print("🗑️ Employee deleted successfully!\n")


def menu():
    while True:
        print("===== Employee Management System =====")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_employee()
        elif choice == "2":
            view_all_employees()
        elif choice == "3":
            search_employee()
        elif choice == "4":
            update_employee()
        elif choice == "5":
            delete_employee()
        elif choice == "6":
            print("Exiting program... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.\n")


menu()


conn.close()
