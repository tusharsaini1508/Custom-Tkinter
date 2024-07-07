import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import datetime

# Database initialization and functions
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('banking_system.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                username TEXT PRIMARY KEY, 
                                password TEXT,
                                email TEXT,
                                phone TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                                username TEXT, 
                                balance REAL, 
                                transaction_history TEXT)''')
        self.conn.commit()

    def add_user(self, username, password, email, phone):
        self.cursor.execute('INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)', 
                            (username, password, email, phone))
        self.cursor.execute('INSERT INTO accounts (username, balance, transaction_history) VALUES (?, ?, ?)', 
                            (username, 1000.0, ""))
        self.conn.commit()

    def get_user(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        return self.cursor.fetchone()

    def user_exists(self, username):
        return self.get_user(username) is not None

    def update_account(self, username, balance, transaction_history):
        self.cursor.execute('UPDATE accounts SET balance=?, transaction_history=? WHERE username=?', 
                            (balance, transaction_history, username))
        self.conn.commit()

    def get_account(self, username):
        self.cursor.execute('SELECT * FROM accounts WHERE username=?', (username,))
        return self.cursor.fetchone()

db = Database()

# Authentication functions
class Authentication:
    def register(self, username, password, email, phone):
        if db.user_exists(username):
            return False
        hashed_password = self.hash_password(password)
        db.add_user(username, hashed_password, email, phone)
        return True

    def login(self, username, password):
        user = db.get_user(username)
        if user and user[1] == self.hash_password(password):
            return True
        return False

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

auth = Authentication()

# Account management functions
class Account:
    def __init__(self, username):
        self.username = username
        account_data = db.get_account(username)
        self.balance = account_data[1]
        self.transaction_history = account_data[2].splitlines() if account_data[2] else []

    def check_balance(self):
        return self.balance

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"Deposit: ${amount} - {datetime.datetime.now()}")
        self.update_account()

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        self.transaction_history.append(f"Withdrawal: ${amount} - {datetime.datetime.now()}")
        self.update_account()
        return True

    def update_account(self):
        db.update_account(self.username, self.balance, "\n".join(self.transaction_history))

    def get_transaction_history(self):
        return self.transaction_history

# Notification functions
class Notifications:
    def __init__(self):
        self.twilio_client = Client('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN')

    def send_email(self, to_email, subject, body):
        from_email = 'gmail'
        password = 'aaaa aaaa aaaa aaaa '  # Use the app password generated

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)

    def send_sms(self, to_phone, body):
        self.twilio_client.messages.create(
            body=body,
            from_='+1234567890',
            to=to_phone
        )

    def send_deposit_notification(self, email, phone, amount):
        subject = "Deposit Notification"
        body = f"${amount} has been deposited into your account."
        self.send_email(email, subject, body)
        self.send_sms(phone, body)

    def send_withdrawal_notification(self, email, phone, amount):
        subject = "Withdrawal Notification"
        body = f"${amount} has been withdrawn from your account."
        self.send_email(email, subject, body)
        self.send_sms(phone, body)

    def send_transaction_history(self, email, transaction_history):
        subject = "Transaction History"
        body = "Your transaction history:\n" + "\n".join(transaction_history)
        self.send_email(email, subject, body)

notifications = Notifications()

# UI functions
class BankingApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Banking System")
        self.geometry("400x500")
        self.current_user = None
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        self.label = ctk.CTkLabel(self, text="Login")
        self.label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show='*')
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = ctk.CTkButton(self, text="Register", command=self.show_register_screen)
        self.register_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if auth.login(username, password):
            self.current_user = username
            self.account = Account(username)
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Incorrect username or password")

    def show_register_screen(self):
        self.clear_screen()
        self.label = ctk.CTkLabel(self, text="Register")
        self.label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show='*')
        self.password_entry.pack(pady=10)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=10)

        self.phone_entry = ctk.CTkEntry(self, placeholder_text="Phone")
        self.phone_entry.pack(pady=10)

        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.create_login_screen)
        self.back_button.pack(pady=10)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        if auth.register(username, password, email, phone):
            messagebox.showinfo("Success", "Registration successful")
            self.create_login_screen()
        else:
            messagebox.showerror("Error", "Username already exists")

    def show_main_menu(self):
        self.clear_screen()
        self.label = ctk.CTkLabel(self, text="Main Menu")
        self.label.pack(pady=10)

        self.balance_button = ctk.CTkButton(self, text="Check Balance", command=self.check_balance)
        self.balance_button.pack(pady=10)

        self.deposit_button = ctk.CTkButton(self, text="Deposit Cash", command=self.deposit_cash)
        self.deposit_button.pack(pady=10)

        self.withdraw_button = ctk.CTkButton(self, text="Withdraw Cash", command=self.withdraw_cash)
        self.withdraw_button.pack(pady=10)

        self.history_button = ctk.CTkButton(self, text="Transaction History", command=self.show_transaction_history)
        self.history_button.pack(pady=10)

        self.logout_button = ctk.CTkButton(self, text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)

    def check_balance(self):
        balance = self.account.check_balance()
        messagebox.showinfo("Balance", f"Your balance is: ${balance}")

    def deposit_cash(self):
        self.clear_screen()
        self.label = ctk.CTkLabel(self, text="Enter amount to deposit:")
        self.label.pack(pady=10)

        self.amount_entry = ctk.CTkEntry(self)
        self.amount_entry.pack(pady=10)

        self.confirm_button = ctk.CTkButton(self, text="Deposit", command=self.perform_deposit)
        self.confirm_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.show_main_menu)
        self.back_button.pack(pady=10)

    def perform_deposit(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            self.account.deposit(amount)
            user = db.get_user(self.current_user)
            notifications.send_deposit_notification(user[2], user[3], amount)
            messagebox.showinfo("Deposit", f"${amount} deposited successfully")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid amount: {e}")
        self.show_main_menu()

    def withdraw_cash(self):
        self.clear_screen()
        self.label = ctk.CTkLabel(self, text="Enter amount to withdraw:")
        self.label.pack(pady=10)

        self.amount_entry = ctk.CTkEntry(self)
        self.amount_entry.pack(pady=10)

        self.confirm_button = ctk.CTkButton(self, text="Withdraw", command=self.perform_withdraw)
        self.confirm_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.show_main_menu)
        self.back_button.pack(pady=10)

    def perform_withdraw(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            if self.account.withdraw(amount):
                user = db.get_user(self.current_user)
                notifications.send_withdrawal_notification(user[2], user[3], amount)
                messagebox.showinfo("Withdrawal", f"${amount} withdrawn successfully")
            else:
                messagebox.showerror("Error", "Insufficient balance")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid amount: {e}")
        self.show_main_menu()

    def show_transaction_history(self):
        history = self.account.get_transaction_history()
        user = db.get_user(self.current_user)
        notifications.send_transaction_history(user[2], history)
        history_str = "\n".join(history)
        messagebox.showinfo("Transaction History", history_str)
        self.show_main_menu()

    def logout(self):
        self.current_user = None
        self.account = None
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = BankingApp()
    app.mainloop()
