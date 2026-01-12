import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import hashlib
import sys

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "jetsetgo",
    "password": "22247076",
    "database": "aviation",
    "port": 3306
}

class LoginSystem:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Jet Set Go - Login")
        self.root.geometry("400x500")
        self.setup_database()
        self.create_ui()
        
    def hash_password(self, password):
        """Static method to hash passwords consistently"""
        return hashlib.sha256(password.encode()).hexdigest()

    def setup_database(self):
        """Ensure users table exists with default admin"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    is_admin BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Add default admin if not exists
            cursor.execute("SELECT 1 FROM users WHERE username = 'admin'")
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO users (username, password_hash, is_admin) VALUES (%s, %s, TRUE)",
                    ("admin", self.hash_password("admin"))
                )
            conn.commit()
        except Error as e:
            messagebox.showerror("Database Error", f"Setup failed: {str(e)}")
            sys.exit(1)
        finally:
            cursor.close()
            conn.close()

    def create_ui(self):
        """Create login interface with account creation option"""
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=40, padx=60, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Jet Set Go Aviation", font=("Roboto", 24)).pack(pady=12)
        
        # Login Form
        self.username_entry = ctk.CTkEntry(frame, placeholder_text="Username")
        self.username_entry.pack(pady=12)

        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12)

        ctk.CTkButton(
            frame, 
            text="Login",
            command=self.attempt_login
        ).pack(pady=12)

        # Account creation option
        ctk.CTkButton(
            frame,
            text="Create New Account",
            command=self.show_create_account_dialog,
            fg_color="transparent",
            border_width=1
        ).pack(pady=12)

    def show_create_account_dialog(self):
        """Show account creation dialog"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Create Account")
        dialog.geometry("350x400")
        dialog.grab_set()

        frame = ctk.CTkFrame(dialog)
        frame.pack(pady=20, padx=20)

        ctk.CTkLabel(frame, text="Create New Account", font=("Roboto", 16)).pack(pady=10)

        username_entry = ctk.CTkEntry(frame, placeholder_text="Username")
        username_entry.pack(pady=8)

        password_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        password_entry.pack(pady=8)

        confirm_entry = ctk.CTkEntry(frame, placeholder_text="Confirm Password", show="*")
        confirm_entry.pack(pady=8)

        admin_check = ctk.CTkCheckBox(frame, text="Admin Account")
        admin_check.pack(pady=8)

        def validate_and_create():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()
            is_admin = admin_check.get()

            if not all([username, password, confirm]):
                messagebox.showwarning("Error", "All fields are required")
                return

            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return

            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                # Check if username exists
                cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Username already exists")
                    return

                # Create account
                cursor.execute(
                    "INSERT INTO users (username, password_hash, is_admin) VALUES (%s, %s, %s)",
                    (username, self.hash_password(password), bool(is_admin))
                )
                conn.commit()
                messagebox.showinfo("Success", "Account created successfully")
                dialog.destroy()
                
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to create account: {str(e)}")
            finally:
                cursor.close()
                conn.close()

        ctk.CTkButton(
            frame,
            text="Create Account",
            command=validate_and_create
        ).pack(pady=15)

    def attempt_login(self):
        """Handle login attempt"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password")
            return
            
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(cursor.execute("SELECT user_id, username, password_hash, COALESCE(is_admin, FALSE) as is_admin FROM users WHERE username = %s", (username,))
            )
            user = cursor.fetchone()
            
            if user and user['password_hash'] == self.hash_password(password):
                self.root.destroy()
                self.launch_main_app(user['user_id'], username, user.get('is_admin', False))  # Corrected this line
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")
                
        except Error as e:
            messagebox.showerror("Database Error", f"Login failed: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def launch_main_app(self, username, user_id, is_admin= False):
        """Launch the main application with proper arguments"""
        try:
            from jetsetgogui import AviationManagementSystem
            app = AviationManagementSystem(username, user_id, is_admin )
            app.run()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start application: {str(e)}")
            sys.exit(1)

    def run(self):
        """Run the login application"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root.mainloop()

if __name__ == "__main__":
    login = LoginSystem()
    login.run()
