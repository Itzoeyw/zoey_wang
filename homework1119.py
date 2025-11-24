# ---------------------------------------------------------
# DATA STORAGE (Our simple database)
# ---------------------------------------------------------
students = {}
teachers = {}
homeroom_teachers = {}


# ---------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------

def create_users():
    """Handles the creation of new users."""
    while True:
        print("\n--- CREATION MENU ---")
        print("Options: student, teacher, homeroom teacher, end")
        user_type = input("Which user to create? ")

        if user_type == "end":
            break  # Go back to main menu

        elif user_type == "student":
            name = input("Enter student first and last name: ")
            class_name = input("Enter class name (e.g., 3C): ")
            # Save to dictionary
            students[name] = class_name
            print(f"Student {name} added to class {class_name}.")

        elif user_type == "teacher":
            name = input("Enter teacher first and last name: ")
            subject = input("Enter subject: ")

            taught_classes = []
            print("Enter classes one by one. Press Enter (empty line) to finish.")
            while True:
                c = input("Class name: ")
                if c == "":
                    break
                taught_classes.append(c)

            teachers[name] = {
                "subject": subject,
                "classes": taught_classes
            }
            print(f"Teacher {name} added.")

        elif user_type == "homeroom teacher":
            name = input("Enter homeroom teacher name: ")
            class_name = input("Enter the class they lead: ")

            homeroom_teachers[name] = class_name
            print(f"Homeroom teacher {name} assigned to {class_name}.")

        else:
            print("Invalid option. Please try again.")


def manage_users():
    """Handles the management/viewing of users."""
    while True:
        print("\n--- MANAGEMENT MENU ---")
        print("Options: class, student, teacher, homeroom teacher, end")
        option = input("What to manage? ")

        if option == "end":
            break  # Go back to main menu

        elif option == "class":
            search_class = input("Enter class name to display (e.g. 3C): ")

            print(f"\n--- Data for Class: {search_class} ---")

            print("Students:")
            found_student = False
            for name in students:
                if students[name] == search_class:
                    print(f"- {name}")
                    found_student = True
            if not found_student:
                print("- No students found.")

            print("Homeroom Teacher:")
            found_ht = False
            for name in homeroom_teachers:
                if homeroom_teachers[name] == search_class:
                    print(f"- {name}")
                    found_ht = True
            if not found_ht:
                print("- No homeroom teacher assigned.")

        elif option == "student":
            name = input("Enter student name: ")

            if name in students:
                student_class = students[name]
                print(f"\nStudent {name} attends class: {student_class}")

                print(f"Teachers for class {student_class}:")
                for t_name in teachers:
                    if student_class in teachers[t_name]['classes']:
                        subject = teachers[t_name]['subject']
                        print(f"- {t_name} ({subject})")
            else:
                print("Error: Student not found.")

        elif option == "teacher":
            name = input("Enter teacher name: ")

            if name in teachers:
                classes = teachers[name]['classes']
                subject = teachers[name]['subject']
                print(f"\nTeacher {name} teaches {subject}.")
                print("Classes taught:")
                for c in classes:
                    print(f"- {c}")
            else:
                print("Error: Teacher not found.")

        elif option == "homeroom teacher":
            name = input("Enter homeroom teacher name: ")

            if name in homeroom_teachers:
                led_class = homeroom_teachers[name]
                print(f"\n{name} leads class {led_class}.")
                print("Students in this class:")

                for s_name in students:
                    if students[s_name] == led_class:
                        print(f"- {s_name}")
            else:
                print("Error: Homeroom teacher not found.")

        else:
            print("Invalid option.")


# ---------------------------------------------------------
# MAIN PROGRAM LOOP
# ---------------------------------------------------------
print("Welcome to the School Database.")

while True:
    print("\n=== MAIN MENU ===")
    command = input("Command (create, manage, end): ")

    if command == "create":
        create_users()
    elif command == "manage":
        manage_users()
    elif command == "end":
        print("Terminating program. Goodbye!")
        break
    else:
        print("Invalid command. Please type create, manage, or end.")