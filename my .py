import customtkinter as ctk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error

class AviationManagementSystem:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Jet Set Go")
        self.root.geometry("1200x800")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        self.db_config ={"host":"localhost", 
                         "user": "jetsetgo",
                         "password": "22247076", 
                         "database":"aviation",
                         "port":3306 }

        self.connection = None

        self.entity_map = {
            "dashboard":"Dashboard",
            "airline":"Airlines",
            "aircrafts":"Aircrafts",
            "airports":"Airports",
            "flights":"Flights",
            "passengers":"Passengers",
            "bookings":"Bookings"
        }

        self.form_field_to_db_column ={
        "Airlines":{
                        "Name":"airlines_Name",
                        "Country":"Country"
                    }, 
        
        "Airports":{
                        "Name":"airports_Name",
                        "City":"City",
                        "Country":"Country"
                    },
        "Aircrafts":{   
                        "Model":"Model",
                        "Airline":"airlines_ID",
                        "Capacity":"Capacity"
                    },
        "Flights":{
                        "Aircraft-ID":"aircrafts_ID",
                        "From":"departure_airports_ID",
                        "To":"arrival_airports_ID",
                        "Departure-Date":"departure_Date",
                        "Departure-Time":"departure_Time",
                        "Arrival-Date":"arrival_Date",
                        "Arrival-Time":"arrival_Time"
                    },
        "Passengers":{
                        "Name":"Name",
                        "Age":"Age",
                        "Gender":"Gender"
                    },
        "Bookings":{
                        "Passengers": "passengers_ID",
                        "Flight": "flights_ID",
                        "Date": "bookings_Date"
                    }
        }
        self.tables = {}

        self.content_frames = {}

        self.create_header("dashboard")
        
        self.create_sidebar()
        
        self.create_main_content()
        
        self.content_frames = {}
        
        self.tables = {}

        self.create_all_frames()

        self.show_frame("Dashboard")

    def get_connection(self):
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(**self.db_config)
            except Error as err :
                messagebox.showerror("Database Error",str(err))
                return None
            return self.connection

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None
    def validate_input(self,entity_name, field_values):
        validation_rules= self.get_validation_rules(entity_name)
        errors = []
        for field_name, value in field_values.items():
            rules = validation_rules.get(field_name,{})
            if rules.get('required', True) and not value:
                errors.append(f"{field_name} is required")
                continue
            if 'type' in rules:
                if rules['type']== 'int' and not str(value).isdigit():
                    errors.append(f"{field_name} must be a number")
                elif rules['type'] == 'email' and '@' not in value:
                    errors.append(f"{field_name} must be a valid email")
            
            if 'max_length' in rules and len(value) > rules ['max_length']:
                errors.append(f"{field_name} exceeds maximum length ({rules['max_length']})")
            if 'min_value' in rules and len(value) < rules['min_value']:
                errors.append(f"{field_name} must be at least { rules['min_value']}")
        return (len(errors)== 0, "\n".join(errors))
    
    def get_validation_rules(self, entity_name):
    
        rules = {
            "airlines": {
                "Name": {"required": True, "max_length": 100},
                "Country": {"required": True, "max_length": 100}
            },
            "airports": {
                "Name": {"required": True, "max_length": 100},
                "City": {"required": True, "max_length": 100},
                "Country": {"required": True, "max_length": 100}
            },
            "aircrafts": {
                "Model": {"required": True, "max_length": 100},
                "Airline": {"required": True, "type": "int"},
                "Capacity": {"required": True, "type": "int", "min_value": 1}
            },
            "flights": {
                "Aircraft-ID": {"required": True, "type": "int"},
                "From": {"required": True, "type": "int"},
                "To": {"required": True, "type": "int"},
                "Departure-Date": {"required": True},
                "Departure-Time": {"required": True},
                "Arrival-Date": {"required": True},
                "Arrival-Time": {"required": True}
            },
            "passengers": {
                "Name": {"required": True, "max_length": 100},
                "Age": {"required": True, "type": "int", "min_value": 1}
            },
            "bookings": {
                "Passenger": {"required": True, "type": "int"},
                "Flight": {"required": True, "type": "int"},
                "Date": {"required": True}
            }
        }
        return rules.get(entity_name.lower(), {})


    def get_display_name(self, name):
        return name.capitalize()

    def capitalize_entity_name(self,enitity_name):
        return enitity_name.capitalize()

    def create_header(self,entity_name):
        header = ctk.CTkFrame(self.main_container, height=60)
        header.pack(fill="x", padx=10, pady=(0, 10))
        
        title = self.entity_map[entity_name]
        title = ctk.CTkLabel(header, text="Jet Set Go", 
                            font=("Helvetica", 24, "bold"))
        title.pack(side="left", padx=20, pady=10)

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.main_container, width=200)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10))
        
        nav_buttons = [
            ("Dashboard", "📊"),
            ("Airlines", "✈️"),
            ("Airports", "🏢"),
            ("Aircrafts", "🛩️"),
            ("Flights", "🛫"),
            ("Passengers", "👥"),
            ("Bookings", "🎫")
        ]
        
        for text, icon in nav_buttons:
            btn = ctk.CTkButton(self.sidebar, text=f"{icon} {text}",
                               command=lambda t=text: self.show_frame(t))
            btn.pack(pady=5, padx=10, fill="x")

    def create_main_content(self):
        self.content_area = ctk.CTkFrame(self.main_container)
        self.content_area.pack(side="right", fill="both", expand=True)

    def create_all_frames(self):
        self.content_frames["Dashboard"] = self.create_dashboard_frame()
        entity_names= ["Airlines","Airports","Aircrafts","Flights","Passengers","Bookings"]
        for entity in entity_names:
            self.content_frames[entity] = self.create_entity_frame(entity)
    def create_dashboard_frame(self):
        frame = ctk.CTkFrame(self.content_area)
        
        title = ctk.CTkLabel(frame, text="Dashboard", font=("Helvetica", 20, "bold"))
        title.pack(pady=20)
        
        stats_frame = ctk.CTkFrame(frame)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
        stats_data =self.fetch_dashboard_stats()

        stats = [
            ("Total Airlines", stats_data.get("airlines","0")),
            ("Total Airports",stats_data.get("airports","0")),
            ("Total Flights",stats_data.get("flights","0")),
            ("Total Bookings",stats_data.get("bookings","0"))
        ]
        for index, (title, value) in enumerate(stats):
            row = index// 2
            col = index % 2
            self.create_stat_card(stats_frame, title, value ,row , col)
        return frame

    def create_stat_card(self, parent, title, value, row, col):
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
    
    def fetch_dashboard_stats(self):
        stats = {}
        
        try :
            conn = mysql.connector.connect(**self.db_config)
            cursor= conn.cursor()

            for entity in ["airlines","airports","flights","bookings"]:
                cursor.execute(f"SELECT COUNT(*) FROM {entity}")
                count =cursor.fetchone()[0]
                stats[entity]= str(count)
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            stats = {key: "0" for key in ["airlines","airports", "flights","passengers", "bookings"]}
        return stats
    def create_entity_frame(self, entity_name):
        table_name = entity_name.lower()
        frame = ctk.CTkFrame(self.content_area)
        title = ctk.CTkLabel(frame, text=entity_name, font=("Helvetica", 20, "bold"))
        title.pack(pady=20)
        
        fields = self.form_field_to_db_column[self.capitalize_entity_name(entity_name)]
        
        buttons_frame = ctk.CTkFrame(frame)
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(buttons_frame, text="Add New", 
                     command=lambda: self.show_crud_dialog(entity_name, "add")).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Edit Selected", 
                     command=lambda: self.show_crud_dialog(entity_name, "edit")).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Delete Selected", 
                     command=lambda: self.delete_selected(entity_name,entity_name.lower())).pack(side="left", padx=5)
        
        search_frame = ctk.CTkFrame(frame)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search...")
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(search_frame, text="Search", 
                     command=lambda: self.search(entity_name)).pack(side="right")
        
        table_frame = ctk.CTkFrame(frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(table_frame)
        tree.pack(fill="both", expand=True)
        
        self.setup_table_columns(tree, entity_name)
        self.tables[entity_name] = tree
        self.refresh_table(entity_name,table_name)
        
        return frame

    def get_dynamic_columns(self,entity_name, table_name):
        try:
            conn = self.get_connection()
            if conn is None:
                print(f"[DEBUG] No DB connection for {entity_name}")
                return [],[]
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = %s
             """,(self.db_config['database'],table_name.lower()))

            columns = cursor.fetchall()
            cursor.close()

            print(f"[DEBUG] Columns fetched for table '{table_name}': {[col['COLUMN_NAME'] for col in columns]}")

            filtered_columns =[
                col['COLUMN_NAME']
                for col in columns if not col['COLUMN_NAME'].endswith('_at')
            ]                    
        except mysql.connector.Error as err:
            print(f"[DEBUG] Database error in get_dynamic_columns: {err}")
            messagebox.showerror("Database Error",f"Failed to fetch columns: {str(err)}")
            return [],[]
        return filtered_columns, [col['DATA_TYPE'] for col in columns if not col['COLUMN_NAME'].endswith('_at')]


    def setup_table_columns(self, tree, entity_name):
        columns, _ = self.get_dynamic_columns(entity_name, entity_name.lower())
        if not columns :
            messagebox.showwarning("Warning", f"No columns found for {entity_name}")
            return
        
        tree["columns"] = columns
        tree["show"] = "headings"
        
        def format_column_name(col):
            return col.replace('_','').title()
        
        for col in columns:
            tree.heading(col, text=format_column_name(col))
            if col.endswith('_id'):
                tree.column(col, width=100, anchor='center')
            elif col.endswith('name'):
                tree.column(col, width=200) 
            else:
                tree.column(col, width=120)    
    
    def show_frame(self, frame_name):
        frame_key= frame_name.capitalize()
        for frame in self.content_frames.values():
            frame.pack_forget()
        
        if frame_key =="Dashboard":
            self.content_frames[frame_key].destroy()
            self.content_frames[frame_key]= self.create_dashboard_frame()
        if frame_key not in self.content_frames:
            messagebox.showerror("Error",f"Frame '{frame_key}' not found.")
            return    
        self.content_frames[frame_key].pack(fill="both", expand=True)

    def show_crud_dialog(self, entity_name, action):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(f"{action.capitalize()} {entity_name}")
        dialog.geometry("400x500")

        selected_data= None
        if action == "edit":
            frame = self.content_frames[entity_name]
            tree = self.tables[entity_name]
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warining","Select a row to edit.")
                dialog.destroy()
                return
            selected_data = tree.item(selected[0])["values"]
        self.create_entity_form(dialog, entity_name, action, selected_data)
        dialog.lift()
        dialog.focus()

    def get_db_data_from_form(self, table_name, form_entries):
        db_data = {}
        mapping = self.form_field_to_db_column.get(table_name, {})
        if not mapping :
            messagebox.showerror("Error",f"No mapping found for : {table_name}")
        for field_label, entry in form_entries.items():
            db_col = mapping.get(field_label)
            if db_col:
                db_data[db_col] = entry.get()
        return db_data
    
    def create_entity_form(self, parent, entity_name, action, selected_data=None):
        columns, _ = self.get_dynamic_columns(entity_name)
        if not columns:
            return
        form_fields = [col for col in columns 
                       if not col.lower().endswith('_id') or col.lower() == 'id']

        self.form_entries = {}

        for i, field in enumerate(form_fields):
            label =ctk.CTkLabel(parent, text=field.replace('_','').title())
            label.pack(pady=5)
            entry = ctk.CTkEntry(parent)
            if selected_data and i < len(selected_data):
                entry.insert(0,selected_data[i])

            self.form_entries[field] = entry
            entry.pack(pady=5)
        save_button = ctk.CTkButton(parent, text="Save", command= lambda: self.save_entity(entity_name, action, self.form_entries, entity_name.lower()))
        save_button.pack(pady=10)                
    
    
    def save_entity(self, entity_name, action, entries,table_name, record_id=None):
        
        field_values = {field: entry.get() for field, entry in entries.items()}
        is_valid, errors = self.validate_input(entity_name, field_values)
        if not is_valid:
            messagebox.showwarning("Validation Error", errors)
            return
        tree=self.content_frames[self.get_display_name(entity_name)].winfo_children()[-1].winfo_children()[0]
        for row in tree.get_children():
            tree.delete(row)
        
        mapping = self.form_field_to_db_column.get(entity_name)
        if not mapping:
            messagebox.showerror("Error", f"No form-field mapping found for entity '{entity_name}'.")
            return
        
        data ={}
        mapping = self.form_field_to_db_column.get(entity_name.capitalize())
        for field,entry in entries.items():
                value = entry.get().strip()
                if not value:
                    messagebox.showwarning("Input Error",f"{field} cannot be empty.")
                    return                                          
                db_column =mapping.get(field)
                if db_column :
                    data[db_column]= value
                else:
                       messagebox.showerror("Error", f"No DB column found for form field '{field}'.")
                       return 
                
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if action == "add":
                columns = ", ".join(data.keys())
                placeholders =", ".join(["%s"]* len(data))
                values = list(data.values())

                query = f"INSERT INTO {table_name.lower()} ({columns}) VALUES ({placeholders})"
                print(f"[DEBUG] Executing INSERT: {query} with values {values}")
                cursor.execute(query, values)
                
            elif action == "edit":
                tree = self.tables.get(entity_name)
                selected = tree.selection()

                if not selected:
                    messagebox.showerror("Error","No row selected for editing.")
                    cursor.close()
                    return
                record = tree.item(selected[0])["values"]
                pk = self.entities[entity_name]['primary_key']

                record_id = record[0]

                set_clause= ", ".join([f"{col}=%s" for col in data.keys()])
                values = list(data.values())
                values.append(record_id)

                query = f"UPDATE {table_name.lower()} SET {set_clause} WHERE {pk}= %s"
            
                cursor.execute(query,values)
            else:
                messagebox.showerror("Error", "Unknown entity!") 
                cursor.close()
                return   
                
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success",f"{entity_name} {action}ed successfully!")
            self.refresh_table(entity_name,entity_name.lower())
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error",f"Error while saving{entity_name}:{str(err)}")
    
    def refresh_table(self, entity_name,table_name):
        tree = self.tables[entity_name]
        for row in tree.get_children():
            tree.delete(row)
        try:
            conn = self.get_connection()
            if conn is None:
                print(f"[DEBUG] No DB connection when refreshing table {entity_name}")
                return
            cursor = conn.cursor(dictionary=True)

            columns,_ = self.get_dynamic_columns(entity_name,entity_name.lower())
            if not columns:
                print(f"[DEBUG] No columns found for entity {entity_name} in refresh_table")
                return
            columns_str =",".join(columns)
            query=f"SELECT {columns_str} FROM {table_name}"
            print(f"[DEBUG] Executing query in refresh_table: {query}")

            cursor.execute(query)
            rows= cursor.fetchall()
            cursor.close()

            for row in rows:
                tree.insert("","end", values=[row[col] for col in columns])
        except mysql.connector.Error as err:
            print(f"[DEBUG] Database error in refresh_table: {err}")
            messagebox.showerror("Database Error", f"Refresh failed: {str(err)}")        

    

    def delete_selected(self, entity_name, table_name):
        frame = self.content_frames[entity_name]
        tree= frame.winfo_children()[-1].winfo_children()[0]
        selected=tree.selection()
        if not selected:
            messagebox.showwarning("Warining","Please select a row to delete.")
            return
        item = tree.item(selected)["values"][0]
        

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this {entity_name}?")
        if not confirm:
            return
        try:
            conn = conn = self.get_connection()
            cursor = conn.cursor()
            primary_keys={
                "airlines":"airlines_ID",
                "airports":"airports_ID",
                "aircrafts":"aircrafts_ID",
                "flights":"flights_ID",
                "passengers":"passengers_ID",
                "bookings":"bookings_ID"
            }
            cursor.execute(f"DELETE FROM {table_name.lower()} WHERE {primary_keys[self.capitalize_entity_name(entity_name.lower())]} = %s", (item,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Deleted", "Record deleted successfully!")
            self.refresh_table(entity_name, entity_name.lower())
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error while refreshing {entity_name} table: {str(err)}")

        

    def search(self, entity_name):
                
        
        if entity_name not in self.content_frames:
            messagebox.showerror("Error", f"Entity {entity_name} not found")
            return
                
        search_dialog = ctk.CTkToplevel(self.root)
        search_dialog.title(f"Search {entity_name}")
        search_dialog.geometry("500x400")            
        entity_display = self.capitalize_entity_name(entity_name)
        display_fields = list(self.form_field_to_db_column[entity_display].keys())
        ctk.CTkLabel(search_dialog, text="Search Field:").pack(pady=5)
        field_combo = ctk.CTkComboBox(search_dialog, values=display_fields)
        field_combo.pack(pady=5)
        ctk.CTkLabel(search_dialog, text="Search Term:").pack(pady=5)
        search_entry = ctk.CTkEntry(search_dialog)
        search_entry.pack(pady=5)
        results_frame = ctk.CTkFrame(search_dialog)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
                
        ctk.CTkButton(search_dialog, text="Search",command=lambda: self.execute_search(entity_name, field_combo.get(), search_entry.get(), results_frame)).pack(pady=10)
        search_dialog.grab_set()  
                        

    def execute_search(self, entity_name, field_name, search_term, results_frame):
        
        cursor = None

        try:
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            if not field_name or not search_term.strip():
                messagebox.showwarning("Input Error", "Both field and term are required")
                return
                
            db_column = self.form_field_to_db_column[self.capitalize_entity_name(entity_name)].get(field_name)
            
            if not db_column:
                messagebox.showerror("Error", "Invalid search field")
                return
            
            conn = self.get_connection()
            if not conn:
                return
                
            cursor = conn.cursor(dictionary=True)
            
            if "ID" in field_name or field_name.endswith("Id"):
                try:
                    cursor.execute(
                        f"SELECT * FROM {entity_name.lower()} WHERE {db_column} = %s",
                        (int(search_term),)
                    )
                except ValueError:
                    messagebox.showerror("Error", "Search term must be a number.")
                    return
                except ValueError:
                    messagebox.showerror("Error", f"Search failed: {str(err)}")
                    return
            else:
                cursor.execute(
                    f"SELECT * FROM {entity_name.lower()} WHERE {db_column} LIKE %s",
                    (f"%{search_term}%",)
                )
                
            results = cursor.fetchall()
            cursor.close()
            
            if not results:
                ctk.CTkLabel(results_frame, text="No results found").pack()
                return
                
            tree = ttk.Treeview(results_frame)
            scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            if results:
                columns = list(results[0].keys())
                tree["columns"] = columns
                for col in columns:
                    tree.heading(col, text=col.replace('_', ' ').title())
                    tree.column(col, width=120)
                
                for row in results:
                    tree.insert("", "end", values=list(row.values()))
            
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as err:
            messagebox.showerror("Error", f"Search failed: {str(err)}")
        finally:
            if cursor:
                cursor.close()

          
    def close(self):
        self.close_connection()
        self.root.destroy()
    def run(self):
        self.root.mainloop()
        self.close()

def launch_app():
    app = AviationManagementSystem()
    app.run()
