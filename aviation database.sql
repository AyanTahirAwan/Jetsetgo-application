CREATE DATABASE aviation;

USE aviation;

CREATE TABLE Airline (
    Airline_ID INT AUTO_INCREMENT PRIMARY KEY,
    Airline_Name VARCHAR(100),
    Country VARCHAR(100)
);

CREATE TABLE Airport (
    Airport_ID INT AUTO_INCREMENT PRIMARY KEY,
    Airport_Name VARCHAR(100),
    City VARCHAR(100),
    Country VARCHAR(100)
);

CREATE TABLE Aircraft (
    Aircraft_ID INT AUTO_INCREMENT PRIMARY KEY,
    Model VARCHAR(100),
    Airline_ID INT,
    Capacity INT,
    FOREIGN KEY (Airline_ID) REFERENCES Airline(Airline_ID)
);

CREATE TABLE Flight (
    Flight_ID INT AUTO_INCREMENT PRIMARY KEY,
    Aircraft_ID INT,
    Departure_Airport_ID INT,
    Arrival_Airport_ID INT,
    Departure_Date DATE,
    Departure_Time TIME,
    Arrival_Date DATE,
    Arrival_Time TIME,
    FOREIGN KEY (Aircraft_ID) REFERENCES Aircraft(Aircraft_ID),
    FOREIGN KEY (Departure_Airport_ID) REFERENCES Airport(Airport_ID),
    FOREIGN KEY (Arrival_Airport_ID) REFERENCES Airport(Airport_ID)
);

CREATE TABLE Passenger (
    Passenger_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Age INT,
    Gender VARCHAR(10)
);

CREATE TABLE Booking (
    Booking_ID INT AUTO_INCREMENT PRIMARY KEY,
    Passenger_ID INT,
    Flight_ID INT,
    Booking_Date DATE,
    Status VARCHAR(50),
    FOREIGN KEY (Passenger_ID) REFERENCES Passenger(Passenger_ID),
    FOREIGN KEY (Flight_ID) REFERENCES Flight(Flight_ID)
);