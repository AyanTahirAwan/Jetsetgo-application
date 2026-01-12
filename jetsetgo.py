import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pass123",
            database="aviation"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return None

def init_window():
    root = ctk.CTk()
    root.title("Aviation Management System")
    root.geometry("1200x800")
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    return root

def create_main_container(root):
    main_container = ctk.CTkFrame(root)
    main_container.pack(fill="both", expand=True, padx=20, pady=20)
    return main_container

def create_header(container):
    header = ctk.CTkFrame(container, height=60)
    header.pack(fill="x", padx=10, pady=(0, 10))
    
    title = ctk.CTkLabel(header, text="Aviation Management System", 
                        font=("Helvetica", 24, "bold"))
    title.pack(side="left", padx=20, pady=10)

def create_sidebar(container, content_frames, content_area):
    sidebar = ctk.CTkFrame(container, width=200)
    sidebar.pack(side="left", fill="y", padx=(0, 10))
    
    nav_buttons = [
        ("Dashboard", "📊"),
        ("Airlines", "✈️"),
        ("Airports", "🏢"),
        ("Aircraft", "🛩️"),
        ("Flights", "🛫"),
        ("Passengers", "👥"),
        ("Bookings", "🎫")
    ]
    
    for text, icon in nav_buttons:
        btn = ctk.CTkButton(
            sidebar,
            text=f"{icon} {text}",
            command=lambda t=text: show_frame(t, content_frames)
        )
        btn.pack(pady=5, padx=10, fill="x")

def show_frame(frame_name, content_frames):
    for frame in content_frames.values():
        frame.pack_forget()
    content_frames[frame_name].pack(fill="both", expand=True)

def create_stat_card(parent, title, value, row, col):
    card = ctk.CTkFrame(parent)
    card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    
    title_label = ctk.CTkLabel(card, text=title, font=("Helvetica", 14))
    title_label.pack(pady=5)
    
    value_label = ctk.CTkLabel(card, text=value, font=("Helvetica", 24, "bold"))
    value_label.pack(pady=10)
    
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_rowconfigure(1, weight=1)

def create_dashboard_frame(content_area):
    frame = ctk.CTkFrame(content_area)
    
    title = ctk.CTkLabel(frame, text="Dashboard", font=("Helvetica", 20, "bold"))
    title.pack(pady=20)
    
    stats_frame = ctk.CTkFrame(frame)
    stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Airline")
            airlines_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Airport")
            airports_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Flight")
            flights_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Booking")
            bookings_count = cursor.fetchone()[0]
            
            create_stat_card(stats_frame, "Total Airlines", str(airlines_count), 0, 0)
            create_stat_card(stats_frame, "Total Airports", str(airports_count), 0, 1)
            create_stat_card(stats_frame, "Active Flights", str(flights_count), 1, 0)
            create_stat_card(stats_frame, "Total Bookings", str(bookings_count), 1, 1)
        
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()
    
    return frame

def get_entity_columns(entity_name):
    columns = {
        "Airlines": ["Airline_ID", "Airline_Name", "Country"],
        "Airports": ["Airport_ID", "Airport_Name", "City", "Country"],
        "Aircraft": ["Aircraft_ID", "Model", "Airline_ID", "Capacity"],
        "Flights": ["Flight_ID", "Aircraft_ID", "Departure_Airport_ID", "Arrival_Airport_ID", 
                   "Departure_Date", "Departure_Time", "Arrival_Date", "Arrival_Time"],
        "Passengers": ["Passenger_ID", "Name", "Age", "Gender"],
        "Bookings": ["Booking_ID", "Passenger_ID", "Flight_ID", "Booking_Date", "Status"]
    }
    return columns.get(entity_name, [])

def refresh_table(tree, entity_name):
    for item in tree.get_children():
        tree.delete(item)
        
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            table_name = get_table_name(entity_name)
            cursor.execute(f"SELECT * FROM {table_name}")
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

def save_entity(entity_name, action, entries, dialog, tree):
    values = {field: entry.get() for field, entry in entries.items()}
    
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            if action == "add":
                fields = ", ".join(values.keys())
                placeholders = ", ".join(["%s"] * len(values))
                table_name = get_table_name(entity_name)
                query = f"INSERT INTO {table_name} ({fields}) VALUES ({placeholders})"
                cursor.execute(query, list(values.values()))
            
            conn.commit()
            messagebox.showinfo("Success", f"{entity_name[:-1]} {action}ed successfully!")
            dialog.destroy()
            refresh_table(tree, entity_name)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

def create_entity_form(parent, entity_name, action, tree):
    fields = get_entity_columns(entity_name)[1:]
    entries = {}
    
    for field in fields:
        label = ctk.CTkLabel(parent, text=field.replace("_", " "))
        label.pack(pady=5)
        entry = ctk.CTkEntry(parent)
        entry.pack(pady=5)
        entries[field] = entry
    
    save_btn = ctk.CTkButton(
        parent,
        text="Save",
        command=lambda: save_entity(entity_name, action, entries, parent, tree)
    )
    save_btn.pack(pady=20)

def show_crud_dialog(entity_name, action, tree):
    dialog = ctk.CTkToplevel()
    dialog.title(f"{action.capitalize()} {entity_name}")
    dialog.geometry("400x500")
    
    create_entity_form(dialog, entity_name, action, tree)

def delete_selected(entity_name, tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select an item to delete")
        return
        
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
        item_id = tree.item(selected_item)['values'][0]
        
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                table_name = get_table_name(entity_name)
                cursor.execute(f"DELETE FROM {table_name} WHERE {table_name}_ID = %s", (item_id,))
                conn.commit()
                messagebox.showinfo("Success", f"{entity_name[:-1]} deleted successfully!")
                refresh_table(tree, entity_name)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

def create_entity_frame(content_area, entity_name):
    frame = ctk.CTkFrame(content_area)
    
    title = ctk.CTkLabel(frame, text=entity_name, font=("Helvetica", 20, "bold"))
    title.pack(pady=20)
    
    buttons_frame = ctk.CTkFrame(frame)
    buttons_frame.pack(fill="x", padx=20, pady=10)
    
    table_frame = ctk.CTkFrame(frame)
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    style = ttk.Style()
    style.configure("Treeview", background="#2a2d2e", 
                   fieldbackground="#2a2d2e", foreground="white")
    
    columns = get_entity_columns(entity_name)
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    ctk.CTkButton(
        buttons_frame,
        text="Add New",
        command=lambda: show_crud_dialog(entity_name, "add", tree)
    ).pack(side="left", padx=5)
    
    ctk.CTkButton(
        buttons_frame,
        text="Edit Selected",
        command=lambda: show_crud_dialog(entity_name, "edit", tree)
    ).pack(side="left", padx=5)
    
    ctk.CTkButton(
        buttons_frame,
        text="Delete Selected",
        command=lambda: delete_selected(entity_name, tree)
    ).pack(side="left", padx=5)
    
    ctk.CTkButton(
        buttons_frame,
        text="Refresh",
        command=lambda: refresh_table(tree, entity_name)
    ).pack(side="right", padx=5)
    
    refresh_table(tree, entity_name)
    
    return frame

def get_table_name(entity_name):
    table_mapping = {
        "Airlines": "Airline",
        "Airports": "Airport",
        "Aircraft": "Aircraft",
        "Flights": "Flight",
        "Passengers": "Passenger",
        "Bookings": "Booking"
    }
    return table_mapping.get(entity_name, entity_name)

root = init_window()
main_container = create_main_container(root)
content_area = ctk.CTkFrame(main_container)
content_area.pack(side="right", fill="both", expand=True)

create_header(main_container)

content_frames = {
    "Dashboard": create_dashboard_frame(content_area),
    "Airlines": create_entity_frame(content_area, "Airlines"),
    "Airports": create_entity_frame(content_area, "Airports"),
    "Aircraft": create_entity_frame(content_area, "Aircraft"),
    "Flights": create_entity_frame(content_area, "Flights"),
    "Passengers": create_entity_frame(content_area, "Passengers"),
    "Bookings": create_entity_frame(content_area, "Bookings")
}

create_sidebar(main_container, content_frames, content_area)

show_frame("Dashboard", content_frames)

root.mainloop()