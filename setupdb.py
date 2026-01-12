import mysql.connector
from database import cursor
from mysql.connector import errorcode, Error
DB_NAME = 'aviation_cli'

TABLES= {
"airlines": {"query":    """CREATE TABLE IF NOT EXISTS airlines(airlines_ID INT AUTO_INCREMENT PRIMARY KEY,
                                                                    airlines_Name VARCHAR(100) NOT NULL,
                                                                    country VARCHAR(20));"""},
"airports":{
            "query":"""CREATE TABLE IF NOT EXISTS airports( airport_ID INT AUTO_INCREMENT PRIMARY KEY,
                                                            name VARCHAR(100) NOT NULL,
                                                            city VARCHAR(20),
                                                            country VARCHAR(20) );"""},

"aircrafts":{"query":"""CREATE TABLE IF NOT EXISTS aircrafts(aircraft_ID INT AUTO_INCREMENT PRIMARY KEY,
                                                             model VARCHAR(20),
                                                             country VARCHAR(20),
                                                             capacity INT,
                                                             airlines_ID INT,
                                                             FOREIGN KEY (airlines_ID) REFERENCES airlines(airlines_ID));"""},

"flights":{ "query":"""CREATE TABLE IF NOT EXISTS flights(  flight_ID INT AUTO_INCREMENT PRIMARY KEY,
                                                            airlines_ID INT,
                                                            departure_airport_ID INT,
                                                            arrival_airport_ID INT,
                                                            departure_time DATETIME,
                                                            arrival_time DATETIME,
                                                            FOREIGN KEY (airlines_ID) REFERENCES airlines(airlines_ID),
                                                            FOREIGN KEY (departure_airport_ID) REFERENCES airports(airport_ID),
                                                            FOREIGN KEY (arrival_airport_ID) REFERENCES airports(airport_ID));"""},

"bookings":{ "query":"""CREATE TABLE IF NOT EXISTS bookings(booking_ID INT AUTO_INCREMENT PRIMARY KEY,
                                                            passenger_ID INT,
                                                            flight_ID INT,
                                                            bookings_Date DATE,
                                                            Status VARCHAR(50),
                                                            FOREIGN KEY (passenger_ID) REFERENCES passengers(passenger_ID),
                                                            FOREIGN KEY (flight_ID) REFERENCES flights(flight_ID));"""},

"passengers": {"query":"""CREATE TABLE IF NOT EXISTS passengers(passenger_ID INT AUTO_INCREMENT PRIMARY KEY,
                                                              Name VARCHAR(100),
                                                              Age INT,
                                                              Gender VARCHAR(10));"""},

"users": {"query":"""CREATE TABLE IF NOT EXISTS users(  user_ID INT AUTO_INCREMENT PRIMARY KEY,
                                                        username VARCHAR(50) UNIQUE NOT NULL,
                                                        password_hash VARCHAR(255) NOT NULL,
                                                        email VARCHAR(100),
                                                        is_admin BOOLEAN DEFAULT FALSE,
                                                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                                        );"""}
}
def create_database():
    cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'UTF8'".format(DB_NAME))
    print("Database {} created.".format(DB_NAME))

def create_tables():
    cursor.execute("USE {}".format(DB_NAME))

    for table_name, create_sql in TABLES.items():
        try:
            print(f"Creating table({table_name})")
            cursor.execute(create_sql)
        except mysql.connector.Error as err:
            if err.errno== errorcode.ER_TABLE_EXISTS_ERROR:
                print("Already exists")
            else:
                print(err.msg)

    
create_database()
create_tables()