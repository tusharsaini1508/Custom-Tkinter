import customtkinter as ctk
from tkinter import messagebox

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x600")
        
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.frame, text="Student Management System", font=("Arial", 24))
        self.title_label.pack(pady=12, padx=10)

        self.students = {}

        self.create_widgets()

    def create_widgets(self):
        self.add_student_button = ctk.CTkButton(self.frame, text="Add Student", command=self.add_student)
        self.add_student_button.pack(pady=5)

        self.manage_attendance_button = ctk.CTkButton(self.frame, text="Manage Attendance", command=self.manage_attendance)
        self.manage_attendance_button.pack(pady=5)

        self.add_subject_marks_button = ctk.CTkButton(self.frame, text="Add Subject and Marks", command=self.add_subject_and_marks)
        self.add_subject_marks_button.pack(pady=5)

        self.view_students_button = ctk.CTkButton(self.frame, text="View Students", command=self.view_students)
        self.view_students_button.pack(pady=5)

    def add_student(self):
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("Add Student")

        self.student_name_label = ctk.CTkLabel(self.new_window, text="Student Name")
        self.student_name_label.pack(pady=5)
        self.student_name_entry = ctk.CTkEntry(self.new_window)
        self.student_name_entry.pack(pady=5)

        self.roll_number_label = ctk.CTkLabel(self.new_window, text="Roll Number")
        self.roll_number_label.pack(pady=5)
        self.roll_number_entry = ctk.CTkEntry(self.new_window)
        self.roll_number_entry.pack(pady=5)

        self.add_student_button = ctk.CTkButton(self.new_window, text="Add", command=self.save_student)
        self.add_student_button.pack(pady=5)

    def save_student(self):
        student_name = self.student_name_entry.get()
        roll_number = self.roll_number_entry.get()
        if roll_number in self.students:
            messagebox.showerror("Error", "Roll Number already exists")
        else:
            self.students[roll_number] = {"name": student_name, "attendance": {}, "marks": {}}
            messagebox.showinfo("Success", "Student Added Successfully!")
        self.new_window.destroy()

    def manage_attendance(self):
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("Manage Attendance")

        self.roll_number_label = ctk.CTkLabel(self.new_window, text="Roll Number")
        self.roll_number_label.pack(pady=5)
        self.roll_number_entry = ctk.CTkEntry(self.new_window)
        self.roll_number_entry.pack(pady=5)

        self.date_label = ctk.CTkLabel(self.new_window, text="Date (YYYY-MM-DD)")
        self.date_label.pack(pady=5)
        self.date_entry = ctk.CTkEntry(self.new_window)
        self.date_entry.pack(pady=5)

        self.present_button = ctk.CTkButton(self.new_window, text="Present", command=lambda: self.mark_attendance("Present"))
        self.present_button.pack(pady=5)

        self.absent_button = ctk.CTkButton(self.new_window, text="Absent", command=lambda: self.mark_attendance("Absent"))
        self.absent_button.pack(pady=5)

    def mark_attendance(self, status):
        roll_number = self.roll_number_entry.get()
        date = self.date_entry.get()
        if roll_number in self.students:
            self.students[roll_number]["attendance"][date] = status
            messagebox.showinfo("Success", f"Attendance marked as {status} for {date}")
        else:
            messagebox.showerror("Error", "Invalid Roll Number")
        self.new_window.destroy()

    def add_subject_and_marks(self):
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("Add Subject and Marks")

        self.roll_number_label = ctk.CTkLabel(self.new_window, text="Roll Number")
        self.roll_number_label.pack(pady=5)
        self.roll_number_entry = ctk.CTkEntry(self.new_window)
        self.roll_number_entry.pack(pady=5)

        self.subject_label = ctk.CTkLabel(self.new_window, text="Subject")
        self.subject_label.pack(pady=5)
        self.subject_entry = ctk.CTkEntry(self.new_window)
        self.subject_entry.pack (pady=5)

        self.marks_label = ctk.CTkLabel(self.new_window, text="Marks")
        self.marks_label.pack(pady=5)
        self.marks_entry = ctk.CTkEntry(self.new_window)
        self.marks_entry.pack(pady=5)

        self.add_marks_button = ctk.CTkButton(self.new_window, text="Add", command=self.save_subject_and_marks)
        self.add_marks_button.pack(pady=5)

    def save_subject_and_marks(self):
        roll_number = self.roll_number_entry.get()
        subject = self.subject_entry.get()
        marks = self.marks_entry.get()
        
        if roll_number in self.students:
            if subject not in self.students[roll_number]["marks"]:
                self.students[roll_number]["marks"][subject] = marks
                messagebox.showinfo("Success", "Marks Added Successfully!")
            else:
                messagebox.showerror("Error", "Marks for this subject already exist")
        else:
            messagebox.showerror("Error", "Invalid Roll Number")
        self.new_window.destroy()

    def view_students(self):
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("All Students")

        for roll_number, details in self.students.items():
            student_info = f"Roll Number: {roll_number}, Name: {details['name']}"
            student_label = ctk.CTkLabel(self.new_window, text=student_info)
            student_label.pack(pady=5)
            
            attendance_info = f"Attendance: {details['attendance']}"
            attendance_label = ctk.CTkLabel(self.new_window, text=attendance_info)
            attendance_label.pack(pady=5)
            
            marks_info = f"Marks: {details['marks']}"
            marks_label = ctk.CTkLabel(self.new_window, text=marks_info)
            marks_label.pack(pady=5)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = StudentManagementSystem(root)
    root.mainloop()

