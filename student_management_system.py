
#   AI STUDENT MANAGEMENT & PERFORMANCE ANALYZER SYSTEM
#   Future Vision University
#   Python 3.14 | IDLE Compatible

import os
import csv
import numpy as np
import pandas as pd

TEXT_FILE = "students.txt"
CSV_FILE  = "students.csv"

GRADE_A    = 90
GRADE_B    = 75
GRADE_C    = 50
EXCELLENT  = 85

class C:
    """Terminal color & style codes."""
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

   
    WHITE   = "\033[97m"
    CYAN    = "\033[96m"
    BLUE    = "\033[94m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"

   
    BG_BLUE  = "\033[44m"
    BG_CYAN  = "\033[46m"
    BG_BLACK = "\033[40m"



def section_header(title):
    """Prints a styled section heading."""
    width = 55
    bar   = "─" * width
    print(f"\n{C.CYAN}{bar}{C.RESET}")
    print(f"{C.BG_BLUE}{C.BOLD}{C.WHITE}  {'  ' + title:<{width-2}}{C.RESET}")
    print(f"{C.CYAN}{bar}{C.RESET}")


def success(msg):
    print(f"\n  {C.GREEN}{C.BOLD}✔  {msg}{C.RESET}")


def warn(msg):
    print(f"\n  {C.YELLOW}⚠  {msg}{C.RESET}")


def error(msg):
    print(f"\n  {C.RED}[!] {msg}{C.RESET}")


def info(msg):
    print(f"\n  {C.CYAN}ℹ  {msg}{C.RESET}")


def prompt(label):
    """Styled input prompt. Returns stripped string."""
    return input(f"  {C.BOLD}{C.WHITE}{label}{C.RESET}").strip()


def back_hint():
    """Remind the user they can go back."""
    print(f"  {C.DIM}(type 'b' at any prompt to go back to the Main Menu){C.RESET}")


def is_back(value):
    return str(value).strip().lower() == 'b'



class Student:
    """Represents a single student record."""

    total_students = 0

    def __init__(self, student_id, name, age, marks):
        self.student_id  = str(student_id)
        self.name        = str(name)
        self.age         = int(age)
        self.marks       = float(marks)
        self.grade       = self.calculate_grade()
        self.performance = self.evaluate_performance()
        Student.total_students += 1

    def calculate_grade(self):
        if self.marks >= GRADE_A:
            return "A"
        elif self.marks >= GRADE_B:
            return "B"
        elif self.marks >= GRADE_C:
            return "C"
        else:
            return "Fail"

    def evaluate_performance(self):
        if self.marks > EXCELLENT:
            return "Excellent Performance"
        else:
            return "Needs Improvement"

    def to_tuple(self):
        return (self.student_id, self.name, self.age, self.marks,
                self.grade, self.performance)

    def to_dict(self):
        return {
            "Student ID"  : self.student_id,
            "Name"        : self.name,
            "Age"         : self.age,
            "Marks"       : self.marks,
            "Grade"       : self.grade,
            "Performance" : self.performance
        }

    def __str__(self):
        grade_color = {
            "A"   : C.GREEN,
            "B"   : C.CYAN,
            "C"   : C.YELLOW,
            "Fail": C.RED
        }.get(self.grade, C.WHITE)
        return (f"{C.BOLD}ID:{C.RESET} {self.student_id}  "
                f"{C.BOLD}Name:{C.RESET} {self.name}  "
                f"{C.BOLD}Age:{C.RESET} {self.age}  "
                f"{C.BOLD}Marks:{C.RESET} {self.marks}  "
                f"{C.BOLD}Grade:{C.RESET} {grade_color}{self.grade}{C.RESET}  "
                f"{C.DIM}|{C.RESET} {self.performance}")



class StudentManager:
    """Manages all student records – add, display, save, load."""

    def __init__(self):
        self.students = []
        self.load_from_file()

    def add_student(self):
        section_header("ADD NEW STUDENT")
        back_hint()

        student_id = prompt("Enter Student ID   : ")
        if is_back(student_id):
            info("Returning to Main Menu.")
            return

        if self.find_student(student_id):
            error(f"Student with ID '{student_id}' already exists!")
            return

        name = prompt("Enter Student Name : ")
        if is_back(name):
            info("Returning to Main Menu.")
            return

        
        while True:
            raw = prompt("Enter Age          : ")
            if is_back(raw):
                info("Returning to Main Menu.")
                return
            try:
                age = int(raw)
                if age < 10 or age > 100:
                    error("Please enter a valid age (10–100).")
                    continue
                break
            except ValueError:
                error("Age must be a number. Try again.")

       
        while True:
            raw = prompt("Enter Marks (0–100): ")
            if is_back(raw):
                info("Returning to Main Menu.")
                return
            try:
                marks = float(raw)
                if marks < 0 or marks > 100:
                    error("Marks must be between 0 and 100.")
                    continue
                break
            except ValueError:
                error("Marks must be a number. Try again.")

        student = Student(student_id, name, age, marks)
        self.students.append(student)

        success("Student added successfully!")
        print(f"     {C.BOLD}Grade assigned  :{C.RESET} {student.grade}")
        print(f"     {C.BOLD}Performance     :{C.RESET} {student.performance}")

        self.save_to_file()
        self.export_to_csv()

    
    def find_student(self, student_id):
        for student in self.students:
            if student.student_id == str(student_id):
                return student
        return None

    
    def display_all_students(self):
        section_header("ALL STUDENT RECORDS")

        if not self.students:
            warn("No student records found.")
            return

        for i, student in enumerate(self.students, start=1):
            print(f"\n  {C.CYAN}[{i}]{C.RESET} {student}")

        print(f"\n  {C.BOLD}{C.BLUE}Total Students: {len(self.students)}{C.RESET}")

   
    def search_student(self):
        section_header("SEARCH STUDENT")
        back_hint()

        sid = prompt("Enter Student ID to search: ")
        if is_back(sid):
            info("Returning to Main Menu.")
            return

        student = self.find_student(sid)
        if student:
            print(f"\n  {C.GREEN}{C.BOLD}Student Found:{C.RESET}")
            print(f"  {C.CYAN}{'─'*50}{C.RESET}")
            info_dict = student.to_dict()
            for key, value in info_dict.items():
                print(f"  {C.BOLD}{key:<15}{C.RESET}: {value}")
        else:
            error(f"No student found with ID '{sid}'.")


    def performance_analysis(self):
        section_header("PERFORMANCE ANALYSIS  (NumPy)")

        if not self.students:
            warn("No student records available.")
            return

        marks_list  = [s.marks for s in self.students]
        marks_array = np.array(marks_list)

        highest = np.max(marks_array)
        lowest  = np.min(marks_array)
        average = np.mean(marks_array)
        std_dev = np.std(marks_array)

        print(f"\n  {C.BOLD}Total Students  :{C.RESET} {len(self.students)}")
        print(f"  {C.BOLD}Highest Marks   :{C.RESET} {C.GREEN}{highest:.2f}{C.RESET}")
        print(f"  {C.BOLD}Lowest Marks    :{C.RESET} {C.RED}{lowest:.2f}{C.RESET}")
        print(f"  {C.BOLD}Average Marks   :{C.RESET} {C.CYAN}{average:.2f}{C.RESET}")
        print(f"  {C.BOLD}Std Deviation   :{C.RESET} {std_dev:.2f}")

        grade_counts = {"A": 0, "B": 0, "C": 0, "Fail": 0}
        excellent_students = []
        weak_students      = []

        for student in self.students:
            grade_counts[student.grade] += 1
            if student.marks > EXCELLENT:
                excellent_students.append(student.name)
            else:
                weak_students.append(student.name)

        print(f"\n  {C.BOLD}{C.BLUE}--- Grade Distribution ---{C.RESET}")
        grade_colors = {"A": C.GREEN, "B": C.CYAN, "C": C.YELLOW, "Fail": C.RED}
        for grade, count in grade_counts.items():
            bar = "█" * count
            col = grade_colors.get(grade, C.WHITE)
            print(f"  Grade {col}{grade:<5}{C.RESET}: {count} students  {col}{bar}{C.RESET}")

        print(f"\n  {C.BOLD}{C.GREEN}--- Excellent Performers ---{C.RESET}")
        if excellent_students:
            for name in excellent_students:
                print(f"  {C.GREEN}⭐ {name}{C.RESET}")
        else:
            print("  None")

        print(f"\n  {C.BOLD}{C.YELLOW}--- Students Needing Improvement ---{C.RESET}")
        if weak_students:
            for name in weak_students:
                print(f"  {C.YELLOW}⚠  {name}{C.RESET}")
        else:
            print("  None")


    def generate_report(self):
        section_header("STUDENT REPORT  (Pandas DataFrame)")

        if not self.students:
            warn("No student records available.")
            return

        data = [s.to_dict() for s in self.students]
        df   = pd.DataFrame(data)

        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 200)
        print("\n", df.to_string(index=False))

        print(f"\n  {C.BOLD}{C.BLUE}--- Marks Summary ---{C.RESET}")
        print(df["Marks"].describe().to_string())

        print(f"\n  {C.BOLD}{C.BLUE}--- Grade Count ---{C.RESET}")
        print(df["Grade"].value_counts().to_string())

        print(f"\n  {C.BOLD}{C.BLUE}--- Performance Count ---{C.RESET}")
        print(df["Performance"].value_counts().to_string())

        report_file = "student_report.csv"
        df.to_csv(report_file, index=False)
        success(f"Report saved to '{report_file}'")

    # ── Save to Text File ────────────────────────────────────
    def save_to_file(self):
        with open(TEXT_FILE, "w") as f:
            for student in self.students:
                t    = student.to_tuple()
                line = f"{t[0]},{t[1]},{t[2]},{t[3]},{t[4]},{t[5]}\n"
                f.write(line)


    def load_from_file(self):
        self.students = []
        if not os.path.exists(TEXT_FILE):
            return
        with open(TEXT_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) >= 4:
                        try:
                            student = Student(parts[0], parts[1],
                                              int(parts[2]), float(parts[3]))
                            self.students.append(student)
                        except (ValueError, IndexError):
                            pass

    def export_to_csv(self):
        headers = ["Student ID", "Name", "Age", "Marks", "Grade", "Performance"]
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for student in self.students:
                writer.writerow(student.to_dict())
        success(f"Data exported to '{CSV_FILE}'")

    
    def load_from_csv(self):
        if not os.path.exists(CSV_FILE):
            error(f"'{CSV_FILE}' not found.")
            return
        self.students = []
        with open(CSV_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    student = Student(
                        row["Student ID"], row["Name"],
                        int(row["Age"]), float(row["Marks"])
                    )
                    self.students.append(student)
                except (ValueError, KeyError):
                    pass
        success(f"Loaded {len(self.students)} records from '{CSV_FILE}'.")


    def delete_student(self):
        section_header("DELETE STUDENT")
        back_hint()

        sid = prompt("Enter Student ID to delete: ")
        if is_back(sid):
            info("Returning to Main Menu.")
            return

        student = self.find_student(sid)
        if not student:
            error(f"No student found with ID '{sid}'.")
            return

        # Confirmation step
        confirm = prompt(f"Are you sure you want to delete '{student.name}'? (yes/b): ")
        if is_back(confirm) or confirm.lower() != "yes":
            info("Deletion cancelled. Returning to Main Menu.")
            return

        self.students.remove(student)
        Student.total_students -= 1
        self.save_to_file()
        self.export_to_csv()
        success(f"Student '{student.name}' deleted successfully.")


    def update_marks(self):
        section_header("UPDATE STUDENT MARKS")
        back_hint()

        sid = prompt("Enter Student ID to update: ")
        if is_back(sid):
            info("Returning to Main Menu.")
            return

        student = self.find_student(sid)
        if not student:
            error(f"No student found with ID '{sid}'.")
            return

        print(f"  {C.BOLD}Current Marks:{C.RESET} {C.CYAN}{student.marks}{C.RESET}")

        while True:
            raw = prompt("Enter new Marks (0–100): ")
            if is_back(raw):
                info("Returning to Main Menu.")
                return
            try:
                new_marks = float(raw)
                if new_marks < 0 or new_marks > 100:
                    error("Marks must be between 0 and 100.")
                    continue
                break
            except ValueError:
                error("Please enter a valid number.")

        student.marks       = new_marks
        student.grade       = student.calculate_grade()
        student.performance = student.evaluate_performance()

        self.save_to_file()
        self.export_to_csv()
        success("Marks updated successfully!")
        print(f"     {C.BOLD}New Grade   :{C.RESET} {student.grade}")
        print(f"     {C.BOLD}Performance :{C.RESET} {student.performance}")



def print_banner():
    """Displays the themed application banner."""
    w = 57
    print()
    print(f"{C.CYAN}{'═' * w}{C.RESET}")
    print(f"{C.BG_BLUE}{C.BOLD}{C.WHITE}{'':^{w}}{C.RESET}")
    print(f"{C.BG_BLUE}{C.BOLD}{C.WHITE}{'  🎓  AI STUDENT MANAGEMENT SYSTEM':^{w}}{C.RESET}")
    print(f"{C.BG_BLUE}{C.BOLD}{C.CYAN}{'  PERFORMANCE ANALYZER':^{w}}{C.RESET}")
    print(f"{C.BG_BLUE}{C.BOLD}{C.WHITE}{'':^{w}}{C.RESET}")
    print(f"{C.BG_BLACK}{C.DIM}{C.WHITE}{'  ⚡ Future Vision University':^{w}}{C.RESET}")
    print(f"{C.BG_BLACK}{C.DIM}{C.WHITE}{'':^{w}}{C.RESET}")
    print(f"{C.CYAN}{'═' * w}{C.RESET}")


def print_menu():
    """Displays the styled main menu."""
    w = 55
    print(f"\n{C.BLUE}{'─' * w}{C.RESET}")
    print(f"  {C.BOLD}{C.WHITE}{'MAIN MENU':^{w-4}}{C.RESET}")
    print(f"{C.BLUE}{'─' * w}{C.RESET}")
    items = [
        ("1", "Add New Student"),
        ("2", "Display All Students"),
        ("3", "Search Student by ID"),
        ("4", "Update Student Marks"),
        ("5", "Delete Student"),
        ("6", "Performance Analysis  (NumPy)"),
        ("7", "Generate Report       (Pandas)"),
        ("8", "Export to CSV"),
        ("9", "Load from CSV"),
        ("0", "Exit"),
    ]
    for key, label in items:
        color = C.RED if key == "0" else C.CYAN
        print(f"  {color}{C.BOLD}[{key}]{C.RESET}  {label}")
    print(f"{C.BLUE}{'─' * w}{C.RESET}")
    print(f"  {C.DIM}Tip: type 'b' inside any option to go back{C.RESET}")


def get_choice():
    """Gets and validates menu choice."""
    valid_choices = [str(i) for i in range(10)]
    while True:
        choice = input(f"\n  {C.BOLD}{C.WHITE}Enter your choice:{C.RESET} ").strip()
        if choice in valid_choices:
            return choice
        error("Invalid choice. Please enter 0–9.")


def show_grade_table():
    """Displays grading criteria."""
    section_header("GRADING CRITERIA")
    grade_info = (
        ("90 and above", "A",    "Excellent", C.GREEN),
        ("75 – 89",      "B",    "Good",      C.CYAN),
        ("50 – 74",      "C",    "Average",   C.YELLOW),
        ("Below 50",     "Fail", "Poor",      C.RED),
    )
    print(f"\n  {C.BOLD}{'Marks Range':<20} {'Grade':<10} Remark{C.RESET}")
    print(f"  {C.BLUE}{'─' * 40}{C.RESET}")
    for marks_range, grade, remark, col in grade_info:
        print(f"  {col}{marks_range:<20} {grade:<10} {remark}{C.RESET}")


def main():
    print_banner()

    manager = StudentManager()

    if manager.students:
        success(f"Loaded {len(manager.students)} existing record(s) from file.")
    else:
        info("No existing records found. Starting fresh.")

    while True:
        print_menu()
        choice = get_choice()

        if   choice == "1": manager.add_student()
        elif choice == "2": manager.display_all_students()
        elif choice == "3": manager.search_student()
        elif choice == "4": manager.update_marks()
        elif choice == "5": manager.delete_student()
        elif choice == "6": manager.performance_analysis()
        elif choice == "7": manager.generate_report()
        elif choice == "8": manager.export_to_csv()
        elif choice == "9": manager.load_from_csv()
        elif choice == "0":
            section_header("GOODBYE")
            print(f"\n  {C.DIM}Saving data before exit...{C.RESET}")
            manager.save_to_file()
            manager.export_to_csv()
            print(f"\n  {C.BOLD}{C.CYAN}Thank you for using FVU Student System!{C.RESET}")
            print(f"  {C.CYAN}Goodbye! 👋{C.RESET}\n")
            break



if __name__ == "__main__":
    main()
