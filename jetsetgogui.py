import customtkinter as ctk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
import hashlib      
from tkinter import simpledialog

class AviationManagementSystem:
    def __init__(self,user_id, username, is_admin=False):
        self.root = ctk.CTk()
        self.root.title("Jet Set Go Aviation Management")
        self.root.geometry("1200x800")
        self.user_id = user_id
        self.current_user = username
        self.is_admin = is_admin

        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Database configuration
        self.db_config = {
            "host": "localhost",
            "user": "jetsetgo",
            "password": "22247076",
            "database": "aviation",
            "port": 3306
        }

        self.connection = None
        self.current_edit_id = None
        
        # Database entities configuration
        self.entities = {
            "Dashboard": {"fields": [], "table": None},
            "Airlines": {
                "fields": ["Name", "Country"],
                "table": "airlines",
                "primary_key": "airlines_id",
                "columns": {"Name": "airlines_name", "Country": "country"}
            },
            "Airports": {
                "fields": ["Name", "City", "Country"],
                "table": "airports",
                "primary_key": "airports_id", 
                "columns": {"Name": "airports_name", "City": "city", "Country": "country"}
            },
            "Aircrafts": {
                "fields": ["Model", "Airline", "Capacity"],
                "table": "aircrafts",
                "primary_key": "aircrafts_id",
                "columns": {"Model": "model", "Airline": "airlines_id", "Capacity": "capacity"}
            },
            "Flights": {
                "fields": ["Aircraft", "From", "To", "Departure Date", "Arrival Date"],
                "table": "flights",
                "primary_key": "flights_id",
                "columns": {
                    "Aircraft": "aircrafts_id",
                    "From": "departure_airports_id", 
                    "To": "arrival_airports_id",
                    "Departure Date": "departure_date",
                    "Arrival Date": "arrival_date"
                }
            },
            "Passengers": {
                "fields": ["Name", "Age", "Gender"],
                "table": "passengers",
                "primary_key": "passengers_id",
                "columns": {"Name": "name", "Age": "age", "Gender": "gender"}
            },
            "Bookings": {
                "fields": ["Passenger", "Flight", "Date"],
                "table": "bookings",
                "primary_key": "bookings_id",
                "columns": {"Passenger": "passengers_id", "Flight": "flights_id", "Date": "bookings_date"}
            }
        }

        # UI Components
        self.tables = {}
        self.content_frames = {}
        
        # Initialize interface
        self.create_interface()

    def get_connection(self):
        """Get database connection with error handling"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.db_config)
            return self.connection
        except Error as err:
            messagebox.showerror("Database Error", f"Connection failed: {str(err)}")
            return None

    def get_record_count(self, table_name):
        """Count records in table"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except Error as e:
            messagebox.showerror("Database Error", f"Count failed: {str(e)}")
            return 0

    def create_interface(self):
        """Create all interface components"""
        self.create_main_container()
        self.create_header(with_account_menu=True)
        self.create_sidebar()
        self.create_content_area()
        self.create_all_frames()
        self.show_frame("Dashboard")

    def create_main_container(self):
        """Main application container"""
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

    def create_header(self, with_account_menu=False):
        """Application header with user info"""
        self.header = ctk.CTkFrame(self.main_container)
        self.header.pack(fill="x", pady=5)

        # Application title
        title = ctk.CTkLabel(
            self.header,
            text=f"Jet Set Go - {self.current_user}",
            font=("Roboto", 18, "bold")
        )
        title.pack(side="left", padx=10)

        if with_account_menu:
            # Account management dropdown
            self.account_menu = ctk.CTkOptionMenu(
                self.header,
                values=["Account", "Change Password", "Logout"],
                command=self.handle_account_action,
                width=150
            )
            self.account_menu.pack(side="right", padx=10)

    def handle_account_action(self, choice):
        """Handle account-related actions"""
        if choice == "Change Password":
            self.change_password()
        elif choice == "Logout":
            self.logout()
    
    def hash_password(self, password):
        """Instance method to hash passwords"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def change_password(self):
        """Dialog for changing current user password"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Change Password")
        dialog.grab_set()

        frame = ctk.CTkFrame(dialog)
        frame.pack(pady=20, padx=20)

        ctk.CTkLabel(frame, text=f"Change Password for {self.current_user}", font=("Roboto", 16)).pack(pady=10)

        # Current password
        ctk.CTkLabel(frame, text="Current Password:").pack()
        current_entry = ctk.CTkEntry(frame, show="*")
        current_entry.pack(pady=5)

        # New password
        ctk.CTkLabel(frame, text="New Password:").pack()
        new_entry = ctk.CTkEntry(frame, show="*")
        new_entry.pack(pady=5)

        # Confirm new password
        ctk.CTkLabel(frame, text="Confirm New Password:").pack()
        confirm_entry = ctk.CTkEntry(frame, show="*")
        confirm_entry.pack(pady=5)

        def validate_and_change():
            current = current_entry.get().strip()
            new_pass = new_entry.get().strip()
            confirm = confirm_entry.get().strip()

            if not all([current, new_pass, confirm]):
                messagebox.showwarning("Error", "All fields are required")
                return

            if new_pass != confirm:
                messagebox.showerror("Error", "New passwords don't match")
                return

            if len(new_pass) < 6:
                messagebox.showwarning("Error", "Password must be at least 6 characters")
                return

            try:
                conn = self.get_connection()
                cursor = conn.cursor(dictionary=True)
                
                # Verify current password
                cursor.execute(
                    "SELECT password_hash FROM users WHERE username = %s",
                    (self.current_user,)
                )
                user = cursor.fetchone()
                
                if not user or self.hash_password(current) != user['password_hash']:
                    messagebox.showerror("Error", "Current password is incorrect")
                    return

                # Update password
                cursor.execute(
                    "UPDATE users SET password_hash = %s WHERE username = %s",
                    (self.hash_password(new_pass), self.current_user)
                )
                conn.commit()
                messagebox.showinfo("Success", "Password changed successfully")
                dialog.destroy()
                
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to change password: {str(e)}")
            finally:
                cursor.close()
                conn.close()

        ctk.CTkButton(
            frame,
            text="Change Password",
            command=validate_and_change
        ).pack(pady=20)

    def logout(self):
        """Handle logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            # Note: The login.py script should handle restarting the login process

    def create_sidebar(self):
        """Navigation sidebar"""
        self.sidebar = ctk.CTkFrame(self.main_container, width=220)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10), pady=10)
        
        nav_items = [
            ("Dashboard", "📊"),
            ("Airlines", "✈️"), 
            ("Airports", "🏢"),
            ("Aircrafts", "🛩️"),
            ("Flights", "🛫"),
            ("Passengers", "👥"),
            ("Bookings", "🎫")
        ]

        for text, icon in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{icon} {text}",
                command=lambda t=text: self.show_frame(t),
                anchor="w",
                corner_radius=0,
                fg_color="transparent"
            )
            btn.pack(fill="x", pady=2)

    def create_content_area(self):
        """Main content area for entity frames"""
        self.content_area = ctk.CTkFrame(self.main_container)
        self.content_area.pack(side="right", fill="both", expand=True)

    def create_all_frames(self):
        """Create all application frames"""
        self.content_frames["Dashboard"] = self.create_dashboard_frame()
        
        for entity in [e for e in self.entities if e != "Dashboard"]:
            try:
                self.content_frames[entity] = self.create_entity_frame(entity)
                self.refresh_table(entity)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to initialize {entity}: {str(e)}")

    def create_dashboard_frame(self):
        """Dashboard overview frame with statistics"""
        frame = ctk.CTkFrame(self.content_area)
        
        title = ctk.CTkLabel(frame, text="Dashboard Overview", font=("Roboto", 20))
        title.pack(pady=20)

        stats_frame = ctk.CTkFrame(frame)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=10)

        stats = [
            ("Airlines", "airlines"),
            ("Airports", "airports"),
            ("Flights", "flights"),
            ("Bookings", "bookings")
        ]

        for i, (title, table) in enumerate(stats):
            row = i // 2
            col = i % 2
            
            card = ctk.CTkFrame(stats_frame)
            card.grid(row=row, column=col, padx=10, pady=10)

            ctk.CTkLabel(card, text=title).pack()
            ctk.CTkLabel(
                card,
                text=str(self.get_record_count(table)),
                font=("Roboto", 24, "bold")
            ).pack(pady=5)

            stats_frame.rowconfigure(row, weight=1)
            stats_frame.columnconfigure(col, weight=1)

        return frame

    def create_entity_frame(self, entity_name):
        """Create frame for specific entity with CRUD controls"""
        frame = ctk.CTkFrame(self.content_area)

        # Title
        ctk.CTkLabel(
            frame,
            text=f"{entity_name} Management",
            font=("Roboto", 18, "bold")
        ).pack(pady=10)

        # Action buttons
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(fill="x", padx=20, pady=(5, 10))

        ctk.CTkButton(
            btn_frame,
            text="Add New",
            command=lambda: self.show_form_dialog(entity_name, "add"),
            width=100
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Edit Selected", 
            command=lambda: self.show_form_dialog(entity_name, "edit"),
            width=100
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame, 
            text="Delete",
            command=lambda: self.delete_record(entity_name),
            fg_color="red",
            hover_color="darkred",
            width=100
        ).pack(side="left", padx=5)

        # Create table with scrollbars
        table_frame = ctk.CTkFrame(frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tree = ttk.Treeview(table_frame)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y") 
        hsb.pack(side="bottom", fill="x")

        # Configure columns
        fields = self.entities[entity_name]["fields"]
        tree["columns"] = fields
        tree["show"] = "headings"

        for col in fields:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        self.tables[entity_name] = tree
        
        return frame

    def show_frame(self, frame_name):
        """Show the requested frame"""
        # Hide all frames first
        for frame in self.content_frames.values():
            frame.pack_forget()

        if frame_name in self.content_frames:
            self.content_frames[frame_name].pack(fill="both", expand=True)
            if frame_name != "Dashboard":
                self.refresh_table(frame_name)

    def refresh_table(self, entity_name):
        """Refresh data in entity table"""
        try:
            tree = self.tables[entity_name]
            tree.delete(*tree.get_children())

            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            fields = self.entities[entity_name]["fields"]
            columns = [self.entities[entity_name]["columns"][f] for f in fields]
            
            cursor.execute(f"SELECT {','.join(columns)} FROM {self.entities[entity_name]['table']}")
            
            for row in cursor:
                tree.insert("", "end", values=[str(row.get(col, "")) for col in columns])
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load data: {str(e)}")
        finally:
            cursor.close()

    def show_form_dialog(self, entity_name, action):
        """Show form dialog for add/edit operations"""
        try:
            if entity_name not in self.entities:
                raise ValueError("Invalid entity")
                
            dialog = ctk.CTkToplevel(self.root)
            dialog.title(f"{action.capitalize()} {entity_name}")
            dialog.after(100, lambda: dialog.grab_set())
            
            # Get selected record for edit
            selected_record = None
            if action == "edit":
                tree = self.tables.get(entity_name)
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Warning", "Please select a record first")
                    dialog.destroy()
                    return
                
                selected_record = tree.item(selected[0])["values"]
                self.current_edit_id = selected_record[0]  # Store ID for update
            
            self.create_form(dialog, entity_name, action, selected_record)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create form: {str(e)}")

    def create_form(self, dialog, entity_name, action, record=None):
        """Create form fields for entity CRUD operations"""
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.form_entries = {}
        fields = self.entities[entity_name]["fields"]
        
        # Skip ID field for add operations
        fields_to_show = [f for f in fields if not (action == "add" and f.lower() == "id")]
        
        for i, field in enumerate(fields_to_show):
            ctk.CTkLabel(form_frame, text=field).pack(pady=5)
            
            entry = ctk.CTkEntry(form_frame)
            
            # Pre-fill for edit
            if record and i < len(record):
                entry.insert(0, str(record[i]))
                
            entry.pack(fill="x", pady=5)
            self.form_entries[field] = entry
        
        ctk.CTkButton(
            form_frame,
            text="Save",
            command=lambda: self.save_entity(entity_name, action),
            height=40
        ).pack(pady=20)

    def save_entity(self, entity_name, action):
        """Save entity data to database"""
        try:
            if entity_name not in self.entities:
                raise ValueError("Invalid entity")
                
            # Get values from form
            values = {field: entry.get() for field, entry in self.form_entries.items()}
            
            # Validate required fields
            for field, value in values.items():
                if not value.strip():
                    messagebox.showwarning("Validation Error", f"{field} cannot be empty")
                    return
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            fields = self.entities[entity_name]["fields"]
            columns = {f: self.entities[entity_name]["columns"][f] for f in fields}
            
            if action == "add":
                # Build INSERT query
                cols = []
                vals = []
                for f in fields:
                    if f.lower() == "id":
                        continue
                    cols.append(columns[f])
                    vals.append(values[f])
                
                query = f"""
                    INSERT INTO {self.entities[entity_name]['table']} 
                    ({",".join(cols)}) VALUES ({",".join(['%s']*len(vals))})
                """
                cursor.execute(query, vals)
                
            elif action == "edit":
                # Build UPDATE query
                set_parts = []
                vals = []
                for f in fields:
                    if f.lower() == "id":
                        continue
                    db_col = columns[f]
                    set_parts.append(f"{columns[f]} = %s")
                    vals.append(values[f])
                pk_column = self.entities[entity_name]['primary_key']

                query = f"""
                    UPDATE {self.entities[entity_name]['table']}
                    SET {",".join(set_parts)}
                    WHERE {pk_column} = %s
                """
                vals.append(self.current_edit_id)
                cursor.execute(query, vals)
            
            conn.commit()
            messagebox.showinfo("Success", f"Record {action}ed successfully")
            self.refresh_table(entity_name)
            
            # Close dialog
            for child in self.root.winfo_children():
                if isinstance(child, ctk.CTkToplevel):
                    child.destroy()
                    
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to save: {str(e)}")
            conn.rollback()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
        finally:
            cursor.close()

    def delete_record(self, entity_name):
        """Delete selected record from database"""
        try:
            tree = self.tables.get(entity_name)
            if not tree:
                raise ValueError("Table not initialized")
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a record first")
                return
                
            record = tree.item(selected[0])
            record_id = record["values"][0]
            
            pk_column = self.entities[entity_name].get("primary_key", "id")

            if not messagebox.askyesno("Confirm", "Delete this record?"):
                return
                
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                f"DELETE FROM {self.entities[entity_name]['table']} WHERE {pk_column} = %s",
                (record_id,)
            )
            
            if cursor.rowcount == 1:
                conn.commit()
                messagebox.showinfo("Success", "Record deleted successfully")
                self.refresh_table(entity_name)
            else:
                messagebox.showwarning("Warning", "No record was deleted")
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to delete: {str(e)}")
            conn.rollback()
        finally:
            cursor.close()

    def run(self):
        """Run the application mainloop"""
        self.root.mainloop()

if __name__ == "__main__":
    # For testing without login
    app = AviationManagementSystem(is_admin=True, username="admin")
    app.run()
