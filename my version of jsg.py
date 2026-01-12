import customtkinter
import mysql.connector
from jetsetgogui import launch_app
from tkinter import messagebox
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


# Login window

def login_gui():
    login_window = customtkinter.CTk()
    login_window.geometry("400x300")
    login_window.title("Login")

    frame = customtkinter.CTkFrame(master=login_window)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="Login System", font=("Roboto", 24))
    label.pack(pady=12, padx=10)

    username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
    username_entry.pack(pady=12, padx=10)

    password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
    password_entry.pack(pady=12, padx=10)

    def login():
        user = username_entry.get()
        pwd = password_entry.get()
        if user == "admin" and pwd == "admin":
            login_window.destroy()
            from jetsetgogui import launch_app  # import here
            launch_app()

        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    login_button = customtkinter.CTkButton(master=frame, text="Login", command=login)
    login_button.pack(pady=12, padx=10)

    checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
    checkbox.pack(pady=12, padx=10)

    login_window.mainloop()

# Start the app
login_gui()
