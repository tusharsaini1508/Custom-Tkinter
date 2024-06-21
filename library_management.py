import customtkinter as ctk
from tkinter import messagebox
import datetime

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.frame, text="Library Management System", font=("Arial", 24))
        self.title_label.pack(pady=12, padx=10)

        self.books = {}
        self.students = {}

        self.admin_credentials = {"admin": "admin123"}

        self.create_widgets()

    def create_widgets(self):
        # Create buttons
        self.add_book_button = ctk.CTkButton(self.frame, text="Add Book", command=self.add_book)
        self.add_book_button.pack(pady=5)

        self.add_student_button = ctk.CTkButton(self.frame, text="Add Student", command=self.add_student)
        self.add_student_button.pack(pady=5)

        self.issue_book_button = ctk.CTkButton(self.frame, text="Issue Book", command=self.issue_book)
        self.issue_book_button.pack(pady=5)

        self.return_book_button = ctk.CTkButton(self.frame, text="Return Book", command=self.return_book)
        self.return_book_button.pack(pady=5)

        self.check_availability_button = ctk.CTkButton(self.frame, text="Check Book Availability", command=self.check_availability)
        self.check_availability_button.pack(pady=5)

        self.admin_login_button = ctk.CTkButton(self.frame, text="Admin Login", command=self.admin_login)
        self.admin_login_button.pack(pady=5)

        self.admin_signup_button = ctk.CTkButton(self.frame, text="Admin Signup", command=self.admin_signup)
        self.admin_signup_button.pack(pady=5)

        self.student_signup_button = ctk.CTkButton(self.frame, text="Student Signup", command=self.student_signup)
        self.student_signup_button.pack(pady=5)

    def add_book(self):
        # Function to add a book
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("Add Book")

        self.book_id_label = ctk.CTkLabel(self.new_window, text="Book ID")
        self.book_id_label.pack(pady=5)
        self.book_id_entry = ctk.CTkEntry(self.new_window)
        self.book_id_entry.pack(pady=5)

        self.book_name_label = ctk.CTkLabel(self.new_window, text="Book Name")
        self.book_name_label.pack(pady=5)
        self.book_name_entry = ctk.CTkEntry(self.new_window)
        self.book_name_entry.pack(pady=5)

        self.add_book_button = ctk.CTkButton(self.new_window, text="Add", command=self.save_book)
        self.add_book_button.pack(pady=5)

    def save_book(self):
        book_id = self.book_id_entry.get()
        book_name = self.book_name_entry.get()
        self.books[book_id] = {"name": book_name, "issued_to": None}
        messagebox.showinfo("Success", "Book Added Successfully!")
        self.new_window.destroy()

    def add_student(self):
        # Function to add a student
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("Add Student")

        self.student_id_label = ctk.CTkLabel(self.new_window, text="Student ID")
        self.student_id_label.pack(pady=5)
        self.student_id_entry = ctk.CTkEntry(self.new_window)
        self.student_id_entry.pack(pady=5)

        self.student_name_label = ctk.CTkLabel(self.new_window, text="Student Name")
        self.student_name_label.pack(pady=5)
        self.student_name_entry = ctk.CTkEntry(self.new_window)
        self.student_name_entry.pack(pady=5)

        self.add_student_button = ctk.CTkButton(self.new_window, text="Add", command=self.save_student)
        self.add_student_button.pack(pady=5)

    def save_student(self):
        student_id = self.student_id_entry.get()
        student_name = self.student_name_entry.get()
        self.students[student_id] = {"name": student_name, "books_issued": []}
        messagebox.showinfo("Success", "Student Added Successfully!")
        self.new_window.destroy()

    def issue_book(self):
        # Function to issue a book
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("Issue Book")

        self.book_id_label = ctk.CTkLabel(self.new_window, text="Book ID")
        self.book_id_label.pack(pady=5)
        self.book_id_entry = ctk.CTkEntry(self.new_window)
        self.book_id_entry.pack(pady=5)

        self.student_id_label = ctk.CTkLabel(self.new_window, text="Student ID")
        self.student_id_label.pack(pady=5)
        self.student_id_entry = ctk.CTkEntry(self.new_window)
        self.student_id_entry.pack(pady=5)

        self.issue_book_button = ctk.CTkButton(self.new_window, text="Issue", command=self.save_issue_book)
        self.issue_book_button.pack(pady=5)

    def save_issue_book(self):
        book_id = self.book_id_entry.get()
        student_id = self.student_id_entry.get()

        if book_id in self.books and student_id in self.students:
            if self.books[book_id]["issued_to"] is None:
                self.books[book_id]["issued_to"] = student_id
                self.students[student_id]["books_issued"].append(book_id)
                messagebox.showinfo("Success", "Book Issued Successfully!")
            else:
                messagebox.showerror("Error", "Book already issued")
        else:
            messagebox.showerror("Error", "Invalid Book ID or Student ID")
        self.new_window.destroy()

    def return_book(self):
        # Function to return a book
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("Return Book")

        self.book_id_label = ctk.CTkLabel(self.new_window, text="Book ID")
        self.book_id_label.pack(pady=5)
        self.book_id_entry = ctk.CTkEntry(self.new_window)
        self.book_id_entry.pack(pady=5)

        self.student_id_label = ctk.CTkLabel(self.new_window, text="Student ID")
        self.student_id_label.pack(pady=5)
        self.student_id_entry = ctk.CTkEntry(self.new_window)
        self.student_id_entry.pack(pady=5)

        self.return_book_button = ctk.CTkButton(self.new_window, text="Return", command=self.save_return_book)
        self.return_book_button.pack(pady=5)

    def save_return_book(self):
        book_id = self.book_id_entry.get()
        student_id = self.student_id_entry.get()

        if book_id in self.books and student_id in self.students:
            if self.books[book_id]["issued_to"] == student_id:
                self.books[book_id]["issued_to"] = None
                self.students[student_id]["books_issued"].remove(book_id)
                messagebox.showinfo("Success", "Book Returned Successfully!")
            else:
                messagebox.showerror("Error", "Book not issued to this student")
        else:
            messagebox.showerror("Error", "Invalid Book ID or Student ID")
        self.new_window.destroy()

    def check_availability(self):
        # Function to check book availability
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("Check Book Availability")

        self.book_id_label = ctk.CTkLabel(self.new_window, text="Book ID")
        self.book_id_label.pack(pady=5)
        self.book_id_entry = ctk.CTkEntry(self.new_window)
        self.book_id_entry.pack(pady=5)

        self.check_button = ctk.CTkButton(self.new_window, text="Check", command=self.check_book_status)
        self.check_button.pack(pady=5)

    def check_book_status(self):
        book_id = self.book_id_entry.get()
        if book_id in self.books:
            if self.books[book_id]["issued_to"] is None:
                messagebox.showinfo("Availability", "Book is available")
            else:
                messagebox.showinfo("Availability", f"Book is issued to {self.books[book_id]['issued_to']}")
        else:
            messagebox.showerror("Error", "Invalid Book ID")
        self.new_window.destroy()

    def admin_login(self):
        # Function for admin login
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("Admin Login")

        self.username_label = ctk.CTkLabel(self.new_window, text="Username")
        self.username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(self.new_window)
        self.username_entry.pack(pady=5)

        self.password_label = ctk.CTkLabel(self.new_window, text="Password")
        self.password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.new_window, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(self.new_window, text="Login", command=self.verify_admin)
        self.login_button.pack(pady=5)

    def verify_admin(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.admin_credentials and self.admin_credentials[username] == password:
            messagebox.showinfo("Success", "Login Successful!")
            self.new_window.destroy()
            self.admin_panel()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")
            self.new_window.destroy()

    def admin_signup(self):
        # Function for admin signup
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("Admin Signup")

        self.username_label = ctk.CTkLabel(self.new_window, text="Username")
        self.username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(self.new_window)
        self.username_entry.pack(pady=5)

        self.password_label = ctk.CTkLabel(self.new_window, text="Password")
        self.password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.new_window, show="*")
        self.password_entry.pack(pady=5)

        self.signup_button = ctk.CTkButton(self.new_window, text="Signup", command=self.save_admin)
        self.signup_button.pack(pady=5)

    def save_admin(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.admin_credentials:
            messagebox.showerror("Error", "Username already exists")
        else:
            self.admin_credentials[username] = password
            messagebox.showinfo("Success", "Admin Signup Successful!")
        self.new_window.destroy()

    def student_signup(self):
        # Function for student signup
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("Student Signup")

        self.student_id_label = ctk.CTkLabel(self.new_window, text="Student ID")
        self.student_id_label.pack(pady=5)
        self.student_id_entry = ctk.CTkEntry(self.new_window)
        self.student_id_entry.pack(pady=5)

        self.student_name_label = ctk.CTkLabel(self.new_window, text="Student Name")
        self.student_name_label.pack(pady=5)
        self.student_name_entry = ctk.CTkEntry(self.new_window)
        self.student_name_entry.pack(pady=5)

        self.signup_button = ctk.CTkButton(self.new_window, text="Signup", command=self.save_student_signup)
        self.signup_button.pack(pady=5)

    def save_student_signup(self):
        student_id = self.student_id_entry.get()
        student_name = self.student_name_entry.get()
        if student_id in self.students:
            messagebox.showerror("Error", "Student ID already exists")
        else:
            self.students[student_id] = {"name": student_name, "books_issued": []}
            messagebox.showinfo("Success", "Student Signup Successful!")
        self.new_window.destroy()

    def admin_panel(self):
        # Admin panel functionality
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("Admin Panel")

        self.info_label = ctk.CTkLabel(self.new_window, text="Admin Panel", font=("Arial", 20))
        self.info_label.pack(pady=5)

        self.view_books_button = ctk.CTkButton(self.new_window, text="View All Books", command=self.view_books)
        self.view_books_button.pack(pady=5)

        self.view_students_button = ctk.CTkButton(self.new_window, text="View All Students", command=self.view_students)
        self.view_students_button.pack(pady=5)

    def view_books(self):
        # View all books
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("All Books")

        for book_id, details in self.books.items():
            book_info = f"ID: {book_id}, Name: {details['name']}, Issued To: {details['issued_to']}"
            book_label = ctk.CTkLabel(self.new_window, text=book_info)
            book_label.pack(pady=5)

    def view_students(self):
        # View all students
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.title("All Students")

        for student_id, details in self.students.items():
            student_info = f"ID: {student_id}, Name: {details['name']}, Books Issued: {details['books_issued']}"
            student_label = ctk.CTkLabel(self.new_window, text=student_info)
            student_label.pack(pady=5)

# Running the application
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = LibraryManagementSystem(root)
    root.mainloop()
