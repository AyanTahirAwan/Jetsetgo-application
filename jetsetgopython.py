def customtkinter():
import customtkinter as tk
from tkinter import messagebox
import mysql.connector

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root+customtkinter.CTk()
root.geometry("500x350")

def login():
    print("Test")

frame+customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label= customtkinter.CTkLabel(master=frame, text="Login System", text_font=("Roboto", 24))
label.pac(pady=12, padx=10)

entry1= customtkinter.CTkEntry(master=frame, placeholder_text="Username")
entry1.pack(pady=12, padx=10)

entry2=customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

button=customtkinter.CTkButton(master=frame, text="Login", command=login)
button.pack(pady=12, padx=10)

checkbox=customtkinter.CTkCheckBox(master=frame, text="Remember Me")
checkbox.pack(pady=12, padx=10)

root.mainloop()

# Database connection function
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="pass123",  # Replace with your MySQL password
            database="aviation"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return None

# -------------------- Airline Operations --------------------

# Insert Airline
def insert_airline_gui():
    def insert_airline():
        name = airline_name_entry.get()
        country = airline_country_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO Airline (Airline_Name, Country) VALUES (%s, %s)', (name, country))
                conn.commit()
                messagebox.showinfo("Success", "Airline record inserted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
    
    airline_window = tk.Toplevel()
    airline_window.title("Insert Airline")
    
    tk.Label(airline_window, text="Airline Name:").pack()
    airline_name_entry = tk.Entry(airline_window)
    airline_name_entry.pack()

    tk.Label(airline_window, text="Country:").pack()
    airline_country_entry = tk.Entry(airline_window)
    airline_country_entry.pack()

    tk.Button(airline_window, text="Insert", command=insert_airline).pack()

# Update Airline
def update_airline_gui():
    def update_airline():
        airline_id = airline_id_entry.get()
        name = airline_name_entry.get()
        country = airline_country_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE Airline SET Airline_Name = %s, Country = %s WHERE Airline_ID = %s', (name, country, airline_id))
                conn.commit()
                messagebox.showinfo("Success", "Airline record updated successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    airline_window = tk.Toplevel()
    airline_window.title("Update Airline")
    
    tk.Label(airline_window, text="Airline ID:").pack()
    airline_id_entry = tk.Entry(airline_window)
    airline_id_entry.pack()

    tk.Label(airline_window, text="New Airline Name:").pack()
    airline_name_entry = tk.Entry(airline_window)
    airline_name_entry.pack()

    tk.Label(airline_window, text="New Country:").pack()
    airline_country_entry = tk.Entry(airline_window)
    airline_country_entry.pack()

    tk.Button(airline_window, text="Update", command=update_airline).pack()

# Delete Airline
def delete_airline_gui():
    def delete_airline():
        airline_id = airline_id_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM Airline WHERE Airline_ID = %s', (airline_id,))
                conn.commit()
                messagebox.showinfo("Success", "Airline record deleted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    airline_window = tk.Toplevel()
    airline_window.title("Delete Airline")
    
    tk.Label(airline_window, text="Airline ID:").pack()
    airline_id_entry = tk.Entry(airline_window)
    airline_id_entry.pack()

    tk.Button(airline_window, text="Delete", command=delete_airline).pack()

# Display Airlines
def display_airlines():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Airline')
        records = cursor.fetchall()
        
        display_window = tk.Toplevel()
        display_window.title("Airline Records")
        
        for row in records:
            tk.Label(display_window, text=f"ID: {row[0]}, Name: {row[1]}, Country: {row[2]}").pack()

        cursor.close()
        conn.close()

# -------------------- Airport Operations --------------------

# Insert Airport
def insert_airport_gui():
    def insert_airport():
        name = airport_name_entry.get()
        city = airport_city_entry.get()
        country = airport_country_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO Airport (Airport_Name, City, Country) VALUES (%s, %s, %s)', (name, city, country))
                conn.commit()
                messagebox.showinfo("Success", "Airport record inserted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
    
    airport_window = tk.Toplevel()
    airport_window.title("Insert Airport")
    
    tk.Label(airport_window, text="Airport Name:").pack()
    airport_name_entry = tk.Entry(airport_window)
    airport_name_entry.pack()

    tk.Label(airport_window, text="City:").pack()
    airport_city_entry = tk.Entry(airport_window)
    airport_city_entry.pack()

    tk.Label(airport_window, text="Country:").pack()
    airport_country_entry = tk.Entry(airport_window)
    airport_country_entry.pack()

    tk.Button(airport_window, text="Insert", command=insert_airport).pack()

# Update Airport
def update_airport_gui():
    def update_airport():
        airport_id = airport_id_entry.get()
        name = airport_name_entry.get()
        city = airport_city_entry.get()
        country = airport_country_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE Airport SET Airport_Name = %s, City = %s, Country = %s WHERE Airport_ID = %s', 
                               (name, city, country, airport_id))
                conn.commit()
                messagebox.showinfo("Success", "Airport record updated successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    airport_window = tk.Toplevel()
    airport_window.title("Update Airport")
    
    tk.Label(airport_window, text="Airport ID:").pack()
    airport_id_entry = tk.Entry(airport_window)
    airport_id_entry.pack()

    tk.Label(airport_window, text="New Airport Name:").pack()
    airport_name_entry = tk.Entry(airport_window)
    airport_name_entry.pack()

    tk.Label(airport_window, text="New City:").pack()
    airport_city_entry = tk.Entry(airport_window)
    airport_city_entry.pack()

    tk.Label(airport_window, text="New Country:").pack()
    airport_country_entry = tk.Entry(airport_window)
    airport_country_entry.pack()

    tk.Button(airport_window, text="Update", command=update_airport).pack()

# Delete Airport
def delete_airport_gui():
    def delete_airport():
        airport_id = airport_id_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM Airport WHERE Airport_ID = %s', (airport_id,))
                conn.commit()
                messagebox.showinfo("Success", "Airport record deleted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    airport_window = tk.Toplevel()
    airport_window.title("Delete Airport")
    
    tk.Label(airport_window, text="Airport ID:").pack()
    airport_id_entry = tk.Entry(airport_window)
    airport_id_entry.pack()

    tk.Button(airport_window, text="Delete", command=delete_airport).pack()

# Display Airports
def display_airports():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Airport')
        records = cursor.fetchall()

        display_window = tk.Toplevel()
        display_window.title("Airport Records")
        
        for row in records:
            tk.Label(display_window, text=f"ID: {row[0]}, Name: {row[1]}, City: {row[2]}, Country: {row[3]}").pack()

        cursor.close()
        conn.close()

# -------------------- Aircraft Operations --------------------

# Insert Aircraft
def insert_aircraft_gui():
    def insert_aircraft():
        model = aircraft_model_entry.get()
        airline_id = aircraft_airline_id_entry.get()
        capacity = aircraft_capacity_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO Aircraft (Model, Airline_ID, Capacity) VALUES (%s, %s, %s)', 
                               (model, airline_id, capacity))
                conn.commit()
                messagebox.showinfo("Success", "Aircraft record inserted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    aircraft_window = tk.Toplevel()
    aircraft_window.title("Insert Aircraft")
    
    tk.Label(aircraft_window, text="Aircraft Model:").pack()
    aircraft_model_entry = tk.Entry(aircraft_window)
    aircraft_model_entry.pack()

    tk.Label(aircraft_window, text="Airline ID:").pack()
    aircraft_airline_id_entry = tk.Entry(aircraft_window)
    aircraft_airline_id_entry.pack()

    tk.Label(aircraft_window, text="Capacity:").pack()
    aircraft_capacity_entry = tk.Entry(aircraft_window)
    aircraft_capacity_entry.pack()

    tk.Button(aircraft_window, text="Insert", command=insert_aircraft).pack()

# Update Aircraft
def update_aircraft_gui():
    def update_aircraft():
        aircraft_id = aircraft_id_entry.get()
        model = aircraft_model_entry.get()
        airline_id = aircraft_airline_id_entry.get()
        capacity = aircraft_capacity_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE Aircraft SET Model = %s, Airline_ID = %s, Capacity = %s WHERE Aircraft_ID = %s', 
                               (model, airline_id, capacity, aircraft_id))
                conn.commit()
                messagebox.showinfo("Success", "Aircraft record updated successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    aircraft_window = tk.Toplevel()
    aircraft_window.title("Update Aircraft")
    
    tk.Label(aircraft_window, text="Aircraft ID:").pack()
    aircraft_id_entry = tk.Entry(aircraft_window)
    aircraft_id_entry.pack()

    tk.Label(aircraft_window, text="New Model:").pack()
    aircraft_model_entry = tk.Entry(aircraft_window)
    aircraft_model_entry.pack()

    tk.Label(aircraft_window, text="New Airline ID:").pack()
    aircraft_airline_id_entry = tk.Entry(aircraft_window)
    aircraft_airline_id_entry.pack()

    tk.Label(aircraft_window, text="New Capacity:").pack()
    aircraft_capacity_entry = tk.Entry(aircraft_window)
    aircraft_capacity_entry.pack()

    tk.Button(aircraft_window, text="Update", command=update_aircraft).pack()

# Delete Aircraft
def delete_aircraft_gui():
    def delete_aircraft():
        aircraft_id = aircraft_id_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM Aircraft WHERE Aircraft_ID = %s', (aircraft_id,))
                conn.commit()
                messagebox.showinfo("Success", "Aircraft record deleted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    aircraft_window = tk.Toplevel()
    aircraft_window.title("Delete Aircraft")
    
    tk.Label(aircraft_window, text="Aircraft ID:").pack()
    aircraft_id_entry = tk.Entry(aircraft_window)
    aircraft_id_entry.pack()

    tk.Button(aircraft_window, text="Delete", command=delete_aircraft).pack()

# Display Aircraft
def display_aircraft():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Aircraft')
        records = cursor.fetchall()

        display_window = tk.Toplevel()
        display_window.title("Aircraft Records")
        
        for row in records:
            tk.Label(display_window, text=f"ID: {row[0]}, Model: {row[1]}, Airline ID: {row[2]}, Capacity: {row[3]}").pack()

        cursor.close()
        conn.close()

# -------------------- Flight Operations --------------------

# Insert Flight
def insert_flight_gui():
    def insert_flight():
        aircraft_id = flight_aircraft_id_entry.get()
        departure_airport_id = flight_departure_airport_id_entry.get()
        arrival_airport_id = flight_arrival_airport_id_entry.get()
        departure_date = flight_departure_date_entry.get()
        departure_time = flight_departure_time_entry.get()
        arrival_date = flight_arrival_date_entry.get()
        arrival_time = flight_arrival_time_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO Flight (Aircraft_ID, Departure_Airport_ID, Arrival_Airport_ID, '
                               'Departure_Date, Departure_Time, Arrival_Date, Arrival_Time) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                               (aircraft_id, departure_airport_id, arrival_airport_id, departure_date, 
                                departure_time, arrival_date, arrival_time))
                conn.commit()
                messagebox.showinfo("Success", "Flight record inserted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    flight_window = tk.Toplevel()
    flight_window.title("Insert Flight")
    
    tk.Label(flight_window, text="Aircraft ID:").pack()
    flight_aircraft_id_entry = tk.Entry(flight_window)
    flight_aircraft_id_entry.pack()

    tk.Label(flight_window, text="Departure Airport ID:").pack()
    flight_departure_airport_id_entry = tk.Entry(flight_window)
    flight_departure_airport_id_entry.pack()

    tk.Label(flight_window, text="Arrival Airport ID:").pack()
    flight_arrival_airport_id_entry = tk.Entry(flight_window)
    flight_arrival_airport_id_entry.pack()

    tk.Label(flight_window, text="Departure Date (YYYY-MM-DD):").pack()
    flight_departure_date_entry = tk.Entry(flight_window)
    flight_departure_date_entry.pack()

    tk.Label(flight_window, text="Departure Time (HH:MM:SS):").pack()
    flight_departure_time_entry = tk.Entry(flight_window)
    flight_departure_time_entry.pack()

    tk.Label(flight_window, text="Arrival Date (YYYY-MM-DD):").pack()
    flight_arrival_date_entry = tk.Entry(flight_window)
    flight_arrival_date_entry.pack()

    tk.Label(flight_window, text="Arrival Time (HH:MM:SS):").pack()
    flight_arrival_time_entry = tk.Entry(flight_window)
    flight_arrival_time_entry.pack()

    tk.Button(flight_window, text="Insert", command=insert_flight).pack()

# Update Flight
def update_flight_gui():
    def update_flight():
        flight_id = flight_id_entry.get()
        aircraft_id = flight_aircraft_id_entry.get()
        departure_airport_id = flight_departure_airport_id_entry.get()
        arrival_airport_id = flight_arrival_airport_id_entry.get()
        departure_date = flight_departure_date_entry.get()
        departure_time = flight_departure_time_entry.get()
        arrival_date = flight_arrival_date_entry.get()
        arrival_time = flight_arrival_time_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE Flight SET Aircraft_ID = %s, Departure_Airport_ID = %s, Arrival_Airport_ID = %s, '
                               'Departure_Date = %s, Departure_Time = %s, Arrival_Date = %s, Arrival_Time = %s WHERE Flight_ID = %s',
                               (aircraft_id, departure_airport_id, arrival_airport_id, departure_date,
                                departure_time, arrival_date, arrival_time, flight_id))
                conn.commit()
                messagebox.showinfo("Success", "Flight record updated successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    flight_window = tk.Toplevel()
    flight_window.title("Update Flight")
    
    tk.Label(flight_window, text="Flight ID:").pack()
    flight_id_entry = tk.Entry(flight_window)
    flight_id_entry.pack()

    tk.Label(flight_window, text="New Aircraft ID:").pack()
    flight_aircraft_id_entry = tk.Entry(flight_window)
    flight_aircraft_id_entry.pack()

    tk.Label(flight_window, text="New Departure Airport ID:").pack()
    flight_departure_airport_id_entry = tk.Entry(flight_window)
    flight_departure_airport_id_entry.pack()

    tk.Label(flight_window, text="New Arrival Airport ID:").pack()
    flight_arrival_airport_id_entry = tk.Entry(flight_window)
    flight_arrival_airport_id_entry.pack()

    tk.Label(flight_window, text="New Departure Date:").pack()
    flight_departure_date_entry = tk.Entry(flight_window)
    flight_departure_date_entry.pack()

    tk.Label(flight_window, text="New Departure Time:").pack()
    flight_departure_time_entry = tk.Entry(flight_window)
    flight_departure_time_entry.pack()

    tk.Label(flight_window, text="New Arrival Date:").pack()
    flight_arrival_date_entry = tk.Entry(flight_window)
    flight_arrival_date_entry.pack()

    tk.Label(flight_window, text="New Arrival Time:").pack()
    flight_arrival_time_entry = tk.Entry(flight_window)
    flight_arrival_time_entry.pack()

    tk.Button(flight_window, text="Update", command=update_flight).pack()

# Delete Flight
def delete_flight_gui():
    def delete_flight():
        flight_id = flight_id_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM Flight WHERE Flight_ID = %s', (flight_id,))
                conn.commit()
                messagebox.showinfo("Success", "Flight record deleted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    flight_window = tk.Toplevel()
    flight_window.title("Delete Flight")
    
    tk.Label(flight_window, text="Flight ID:").pack()
    flight_id_entry = tk.Entry(flight_window)
    flight_id_entry.pack()

    tk.Button(flight_window, text="Delete", command=delete_flight).pack()

# Display Flights
def display_flights():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Flight')
        records = cursor.fetchall()

        display_window = tk.Toplevel()
        display_window.title("Flight Records")
        
        for row in records:
            tk.Label(display_window, text=f"ID: {row[0]}, Aircraft ID: {row[1]}, Departure Airport ID: {row[2]}, "
                                         f"Arrival Airport ID: {row[3]}, Departure Date: {row[4]}").pack()

        cursor.close()
        conn.close()

def insert_passenger_gui():
    def insert_passenger():
        name = passenger_name_entry.get()
        age = passenger_age_entry.get()
        gender = passenger_gender_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO Passenger (Name, Age, Gender) VALUES (%s, %s, %s)', (name, age, gender))
                conn.commit()
                messagebox.showinfo("Success", "Passenger record inserted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    passenger_window = tk.Toplevel()
    passenger_window.title("Insert Passenger")
    
    tk.Label(passenger_window, text="Name:").pack()
    passenger_name_entry = tk.Entry(passenger_window)
    passenger_name_entry.pack()

    tk.Label(passenger_window, text="Age:").pack()
    passenger_age_entry = tk.Entry(passenger_window)
    passenger_age_entry.pack()

    tk.Label(passenger_window, text="Gender:").pack()
    passenger_gender_entry = tk.Entry(passenger_window)
    passenger_gender_entry.pack()

    tk.Button(passenger_window, text="Insert", command=insert_passenger).pack()

# Update Passenger
def update_passenger_gui():
    def update_passenger():
        passenger_id = passenger_id_entry.get()
        name = passenger_name_entry.get()
        age = passenger_age_entry.get()
        gender = passenger_gender_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE Passenger SET Name = %s, Age = %s, Gender = %s WHERE Passenger_ID = %s',
                               (name, age, gender, passenger_id))
                conn.commit()
                messagebox.showinfo("Success", "Passenger record updated successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    passenger_window = tk.Toplevel()
    passenger_window.title("Update Passenger")
    
    tk.Label(passenger_window, text="Passenger ID:").pack()
    passenger_id_entry = tk.Entry(passenger_window)
    passenger_id_entry.pack()

    tk.Label(passenger_window, text="New Name:").pack()
    passenger_name_entry = tk.Entry(passenger_window)
    passenger_name_entry.pack()

    tk.Label(passenger_window, text="New Age:").pack()
    passenger_age_entry = tk.Entry(passenger_window)
    passenger_age_entry.pack()

    tk.Label(passenger_window, text="New Gender:").pack()
    passenger_gender_entry = tk.Entry(passenger_window)
    passenger_gender_entry.pack()

    tk.Button(passenger_window, text="Update", command=update_passenger).pack()

# Delete Passenger
def delete_passenger_gui():
    def delete_passenger():
        passenger_id = passenger_id_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM Passenger WHERE Passenger_ID = %s', (passenger_id,))
                conn.commit()
                messagebox.showinfo("Success", "Passenger record deleted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    passenger_window = tk.Toplevel()
    passenger_window.title("Delete Passenger")
    
    tk.Label(passenger_window, text="Passenger ID:").pack()
    passenger_id_entry = tk.Entry(passenger_window)
    passenger_id_entry.pack()

    tk.Button(passenger_window, text="Delete", command=delete_passenger).pack()


def display_passengers():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Passenger')
        records = cursor.fetchall()

        display_window = tk.Toplevel()
        display_window.title("Passenger Records")
        
        for row in records:
            tk.Label(display_window, text=f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Gender: {row[3]}").pack()

        cursor.close()
        conn.close()
 # -------------------- Booking Operations --------------------

# Insert Booking
def insert_booking_gui():
    def insert_booking():
        passenger_id = booking_passenger_id_entry.get()
        flight_id = booking_flight_id_entry.get()
        booking_date = booking_date_entry.get()
        status = booking_status_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO Booking (Passenger_ID, Flight_ID, Booking_Date, Status) VALUES (%s, %s, %s, %s)', 
                               (passenger_id, flight_id, booking_date, status))
                conn.commit()
                messagebox.showinfo("Success", "Booking record inserted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
def update_booking_gui():
    def update_booking():
        booking_id = booking_id_update_entry.get()
        passenger_id = booking_passenger_id_update_entry.get()
        flight_id = booking_flight_id_update_entry.get()
        booking_date = booking_date_update_entry.get()
        status = booking_status_update_entry.get()
  
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE Booking SET Passenger_ID = %s, Flight_ID = %s, Booking_Date = %s, Status = %s WHERE Booking_ID = %s', 
                   (passenger_id, flight_id, booking_date, status, booking_id))
    conn.commit()
    conn.close()
def delete_booking_gui():
    def delete_booking():
        booking_id = booking_id_delete_entry.get()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Booking WHERE Booking_ID = %s', (booking_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Booking record deleted successfully!")

def display_bookings_gui():  
    def display_bookings():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Booking')
        records = cursor.fetchall()
        conn.close()
   
    result_text.delete(1.0, tk.END)  # Clear previous results
    for row in records:
        result_text.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}\n")

    booking_window = tk.Toplevel()
    booking_window.title("Insert Booking")
    
    tk.Label(booking_window, text="Passenger ID:").pack()
    booking_passenger_id_entry = tk.Entry(booking_window)
    booking_passenger_id_entry.pack()

    tk.Label(booking_window, text="Flight ID:").pack()
    booking_flight_id_entry = tk.Entry(booking_window)
    booking_flight_id_entry.pack()

    tk.Label(booking_window, text="Booking Date (YYYY-MM-DD):").pack()
    booking_date_entry = tk.Entry(booking_window)
    booking_date_entry.pack()

    tk.Label(booking_window, text="Status:").pack()
    booking_status_entry = tk.Entry(booking_window)
    booking_status_entry.pack()

    tk.Button(booking_window, text="Insert", command=insert_booking).pack()
       

# Main GUI Window Update
def main_gui():
    root = tk.Tk()
    root.title("Aviation Management System")

    # Buttons for Insert Operations
    tk.Button(root, text="Insert Airline", command=insert_airline_gui).pack()
    tk.Button(root, text="Insert Airport", command=insert_airport_gui).pack()
    tk.Button(root, text="Insert Aircraft", command=insert_aircraft_gui).pack()
    tk.Button(root, text="Insert Flight", command=insert_flight_gui).pack()
    tk.Button(root, text="Insert Passenger", command=insert_passenger_gui).pack()
    tk.Button(root, text="Insert Booking", command=insert_booking_gui).pack()

    # Buttons for Update Operations
    tk.Button(root, text="Update Airline", command=update_airline_gui).pack()
    tk.Button(root, text="Update Airport", command=update_airport_gui).pack()
    tk.Button(root, text="Update Aircraft", command=update_aircraft_gui).pack()
    tk.Button(root, text="Update Flight", command=update_flight_gui).pack()
    tk.Button(root, text="Update Passenger", command=update_passenger_gui).pack()
    tk.Button(root, text="Update Booking", command=update_booking_gui).pack()

    # Buttons for Delete Operations
    tk.Button(root, text="Delete Airline", command=delete_airline_gui).pack()
    tk.Button(root, text="Delete Airport", command=delete_airport_gui).pack()
    tk.Button(root, text="Delete Aircraft", command=delete_aircraft_gui).pack()
    tk.Button(root, text="Delete Flight", command=delete_flight_gui).pack()
    tk.Button(root, text="Delete Passenger", command=delete_passenger_gui).pack()
    tk.Button(root, text="Delete Booking", command=delete_booking_gui).pack()

    # Buttons for Display Operations
    tk.Button(root, text="Display Airlines", command=display_airlines).pack()
    tk.Button(root, text="Display Airports", command=display_airports).pack()
    tk.Button(root, text="Display Aircrafts", command=display_aircraft).pack()
    tk.Button(root, text="Display Flights", command=display_flights).pack()
    tk.Button(root, text="Display Passengers", command=display_passengers).pack()
    tk.Button(root, text="Display Bookings", command=display_bookings_gui).pack()

    root.mainloop()

# Run the main GUI
main_gui()

import tkinter as tk
from tkinter import font

def create_gui():
    root = tk.Tk()
    root.title("Aviation Management System")
    root.geometry("300x500")  # Adjust window size

    # Set window background color
    root.configure(bg="#f0f8ff")  # Light blue background

    # Custom font
    button_font = font.Font(family="Helvetica", size=12, weight="bold")

    # Button configuration
    button_config = {
        "font": button_font,
        "bg": "#007acc",  # Button background color
        "fg": "white",    # Button text color
        "activebackground": "#005f99",  # Button background when clicked
        "activeforeground": "white",    # Button text color when clicked
        "width": 20,
        "height": 2,
    }

    # Buttons
    buttons = [
        "Insert Airline",
        "Insert Airport",
        "Insert Aircraft",
        "Insert Flight",
        "Insert Passenger",
        "Insert Booking",
        "Update Airline",
        "Update Airport",
        "Update Aircraft",
        "Update Flight",
        "Update Passenger",
        "Update Booking",
        "Delete Airline",
        "Delete Airport",
        "Delete Aircraft",
        "Delete Flight",
        "Delete Passenger",
        "Delete Booking",
        "Display Airline",
        "Display Airport",
        "Display Aircraft",
        "Display Flight",
        "Display Passengers",
        "Display Bookings",
    ]

    for btn_text in buttons:
        btn = tk.Button(root, text=btn_text, **button_config)
        btn.pack(pady=5)  # Add some vertical spacing between buttons

    root.mainloop()

create_gui()
