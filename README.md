Overview
The Café Management System is a desktop-based Python application designed to simplify café operations by automating customer management, order tracking, and billing. It features a user-friendly GUI built with Tkinter and a MySQL backend for persistent storage.

Features
✅ Customer registration and management
✅ Order taking with menu items (Pizzas, Beverages, Desserts, Burgers)
✅ Real-time order summary with total billing
✅ Order history management
✅ Order cancellation with database auto-update
✅ Interactive and intuitive GUI
✅ Real-time clock display

Installation
Clone the repository:
git clone https://github.com/yourusername/cafe-management-system.git
cd cafe-management-system
Install dependencies:
pip install pillow mysql-connector-python

Set up MySQL Database:
Create a database named CafeDB.

Create the following tables:
sql
Copy code
CREATE TABLE Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    PhoneNumber VARCHAR(15)
);

CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    OrderedItems TEXT,
    TotalAmount FLOAT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

Run the application:
Launch the app to view the home page.
Navigate to Customer Corner to add a new customer and take orders.
Confirm orders to automatically generate the bill.
Go to Orders Corner to view or cancel previous orders.

Tools & Technologies
Python 3.x – Core programming language
Tkinter – Graphical User Interface (GUI)
MySQL – Database for storing customers and orders
PIL (Pillow) – Image handling for GUI
IDE – Visual Studio Code or PyCharm

Future Enhancements
Inventory management integration
Online ordering and delivery tracking
Analytics dashboard for sales and customer insights
Multi-user login with role-based access (Admin, Staff)
Author

Niharika Bhardwaj – Student, Chandigarh University
Acknowledgements
Professor Sobit Rehan, University Institute of Computing (UIC), Chandigarh University
Python, Tkinter, and MySQL official documentation

License
This project is for educational purposes and can be freely used and modified.
