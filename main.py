import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from datetime import datetime
import mysql.connector

# ----------------- DATABASE CONNECTION -----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="CafeDB"
)
cursor = db.cursor()

# ----------------- RESET AUTO-INCREMENT IF TABLE EMPTY -----------------
cursor.execute("SELECT COUNT(*) FROM Customer")
if cursor.fetchone()[0] == 0:
    cursor.execute("ALTER TABLE Customer AUTO_INCREMENT = 1")
    db.commit()

cursor.execute("SELECT COUNT(*) FROM Orders")
if cursor.fetchone()[0] == 0:
    cursor.execute("ALTER TABLE Orders AUTO_INCREMENT = 1")
    db.commit()

# ----------------- ROOT WINDOW -----------------
root = tk.Tk()
root.geometry("1250x750")
root.config(bg="#f5f0e1")
root.title("☕ Uncle Joe's Café")

# ----------------- UPDATE TIME -----------------
def update_time():
    current_time = datetime.now().strftime("%d-%m-%Y  |  %I:%M:%S %p")
    time_label.config(text=current_time)
    root.after(1000, update_time)

# ----------------- HOME PAGE FUNCTION -----------------
def show_home_page(event=None):
    for widget in image_frame.winfo_children():
        widget.destroy()
    try:
        image = Image.open("img.webp")
        image = image.resize((950, 450), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(image)
        img_label = tk.Label(image_frame, image=img, bg="#f5f0e1")
        img_label.image = img
        img_label.pack(pady=10)
    except:
        tk.Label(image_frame, text="Image not found.", bg="#f5f0e1", fg="red").pack()

# ----------------- CUSTOMER PAGE FUNCTION -----------------
def show_customer_page(event=None):
    for widget in image_frame.winfo_children():
        widget.destroy()

    form_frame = tk.Frame(image_frame, bg="#f5f0e1")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Enter Your Name:", font=("Georgia", 12, "bold"), bg="#f5f0e1").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(form_frame, font=("Georgia", 12), width=25)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Enter Phone Number:", font=("Georgia", 12, "bold"), bg="#f5f0e1").grid(row=1, column=0, padx=5, pady=5)
    phone_entry = tk.Entry(form_frame, font=("Georgia", 12), width=25)
    phone_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(image_frame, text="What would you like to have?", font=("Georgia", 18, "bold italic"), bg="#f5f0e1", fg="#3e2723").pack(pady=15)

    menu_items = {
        "Pizzas": [
            ("Margherita", 200), ("Veggie Delight", 220), ("Paneer Tikka", 250), ("Cheese Burst", 300),
            ("Farmhouse", 280), ("Mushroom Pizza", 260), ("BBQ Veg", 270), ("Double Cheese", 320)
        ],
        "Beverages": [
            ("Cold Coffee", 100), ("Cappuccino", 120), ("Green Tea", 70), ("Lemonade", 60),
            ("Masala Chai", 80), ("Black Coffee", 90), ("Hot Chocolate", 130), ("Iced Latte", 110)
        ],
        "Desserts": [
            ("Chocolate Brownie", 150), ("Gulab Jamun", 80), ("Cheesecake", 180), ("Cupcake", 100),
            ("Donut", 120), ("Apple Pie", 140), ("Ice Cream", 100), ("Caramel Pudding", 130)
        ],
        "Burgers": [
            ("Veg Burger", 120), ("Cheese Burger", 150), ("Paneer Burger", 160), ("Classic Burger", 140),
            ("Spicy Bean Burger", 160), ("Crispy Veg", 150), ("Deluxe Burger", 180), ("Jumbo Veg", 210)
        ]
    }

    container = tk.Frame(image_frame, bg="#f5f0e1")
    container.pack(fill="both", expand=True, padx=10, pady=10)

    left_frame = tk.Frame(container, bg="#f5f0e1")
    left_frame.pack(side="left", fill="both", expand=True)

    right_frame = tk.Frame(container, bg="#f5f0e1", relief="ridge", bd=2)
    right_frame.pack(side="right", fill="y", padx=10)

    order_vars = {}

    for col, (category, items) in enumerate(menu_items.items()):
        cat_frame = tk.LabelFrame(
            left_frame,
            text=category,
            font=("Georgia", 13, "bold italic"),
            bg="#f5f0e1",
            fg="#3e2723",
            labelanchor="n",
            bd=2,
            relief="ridge",
            padx=10,
            pady=5
        )
        cat_frame.grid(row=0, column=col, padx=10, sticky="n")

        for item, price in items:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(
                cat_frame,
                text=f"{item}\n₹{price}",
                variable=var,
                font=("Georgia", 10),
                bg="#f5f0e1",
                anchor="w",
                justify="left"
            )
            chk.pack(anchor="w", pady=2)
            order_vars[item] = (var, price)

    tk.Label(right_frame, text="🧾 Order Summary", font=("Georgia", 14, "bold"), bg="#f5f0e1", fg="#3e2723").pack(pady=5)
    summary_text = tk.Text(right_frame, width=45, height=25, font=("Georgia", 11), bg="#fffaf0")
    summary_text.pack(padx=5, pady=5)
    total_label = tk.Label(right_frame, text="Total: ₹0", font=("Georgia", 12, "bold"), bg="#f5f0e1", fg="#3e2723")
    total_label.pack(pady=5)

    confirm_frame = tk.Frame(left_frame, bg="#f5f0e1")
    confirm_frame.grid(row=1, column=0, columnspan=5, pady=15)
    tk.Label(confirm_frame, text="Confirm your order?", font=("Georgia", 12, "bold"), bg="#f5f0e1").pack(side="left", padx=5)

    def confirm_order():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning("Missing Info", "Please enter your name and phone number before confirming!")
            return

        summary_text.delete("1.0", tk.END)
        total = 0
        ordered_items = []

        summary_text.insert(tk.END, "🧾 Your Order Summary:\n\n")

        for item, (var, price) in order_vars.items():
            if var.get():
                summary_text.insert(tk.END, f"• {item} - ₹{price}\n")
                ordered_items.append(f"{item} (₹{price})")
                total += price

        summary_text.insert(tk.END, "\n-----------------------------------\n")
        summary_text.insert(tk.END, f"Total Bill Amount: ₹{total}\n")
        total_label.config(text=f"Total: ₹{total}")

        try:
            cursor.execute("SELECT CustomerID FROM Customer WHERE PhoneNumber = %s", (phone,))
            result = cursor.fetchone()
            if result:
                customer_id = result[0]
            else:
                cursor.execute("INSERT INTO Customer (Name, PhoneNumber) VALUES (%s, %s)", (name, phone))
                db.commit()
                customer_id = cursor.lastrowid

            ordered_str = ", ".join(ordered_items)
            cursor.execute(
                "INSERT INTO Orders (CustomerID, OrderedItems, TotalAmount) VALUES (%s, %s, %s)",
                (customer_id, ordered_str, total)
            )
            db.commit()
            order_id = cursor.lastrowid

            popup = tk.Toplevel(root)
            popup.title("Order Confirmed ✅")
            popup.geometry("420x280")
            popup.config(bg="#fffaf0")

            tk.Label(
                popup,
                text="🎉 Order Placed Successfully!",
                font=("Georgia", 14, "bold"),
                bg="#fffaf0",
                fg="#3e2723"
            ).pack(pady=10)

            tk.Label(
                popup,
                text=f"🧍 Customer ID: {customer_id}\n🧾 Order ID: {order_id}\n💰 Total Bill: ₹{total}\n\n💵 Please pay ₹{total} at the counter\nand collect your order after 15 minutes.",
                font=("Georgia", 12),
                bg="#fffaf0",
                fg="#3e2723",
                justify="left"
            ).pack(pady=10)

            tk.Label(
                popup,
                text="Redirecting to Orders Corner in 10 seconds...",
                font=("Georgia", 10, "italic"),
                bg="#fffaf0",
                fg="gray"
            ).pack(pady=5)

            popup.after(10000, lambda: [popup.destroy(), show_order_page()])

        except Exception as e:
            messagebox.showerror("Database Error", f"Error saving order: {e}")

    def cancel_order():
        summary_text.delete("1.0", tk.END)
        total_label.config(text="Total: ₹0")
        for var, _ in order_vars.values():
            var.set(False)

    tk.Button(confirm_frame, text="Yes", command=confirm_order, bg="#4e342e", fg="white", font=("Georgia", 11, "bold"), width=10).pack(side="left", padx=5)
    tk.Button(confirm_frame, text="No", command=cancel_order, bg="#3e2723", fg="white", font=("Georgia", 11, "bold"), width=10).pack(side="left", padx=5)

# ----------------- ORDER CORNER -----------------
def show_order_page(event=None):
    for widget in image_frame.winfo_children():
        widget.destroy()

    tk.Label(image_frame, text="Welcome to Orders Corner!", font=("Georgia", 18, "bold italic"), bg="#f5f0e1", fg="#3e2723").pack(pady=10)

    input_frame = tk.Frame(image_frame, bg="#f5f0e1")
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Enter Customer ID or Order ID:", font=("Georgia", 12, "bold"), bg="#f5f0e1").grid(row=0, column=0, padx=5, pady=5)
    id_entry = tk.Entry(input_frame, font=("Georgia", 12), width=20)
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    def fetch_order():
        entered_id = id_entry.get().strip()
        if not entered_id:
            messagebox.showwarning("Missing Info", "Please enter your Customer ID or Order ID.")
            return

        for widget in image_frame.winfo_children():
            if widget not in [input_frame]:
                widget.destroy()

        try:
            cursor.execute("""
                SELECT o.OrderID, c.Name, o.OrderedItems, o.TotalAmount
                FROM Orders o
                JOIN Customer c ON o.CustomerID = c.CustomerID
                WHERE o.OrderID = %s
            """, (entered_id,))
            order = cursor.fetchone()

            if not order:
                cursor.execute("""
                    SELECT o.OrderID, c.Name, o.OrderedItems, o.TotalAmount
                    FROM Orders o
                    JOIN Customer c ON o.CustomerID = c.CustomerID
                    WHERE c.CustomerID = %s
                    ORDER BY o.OrderID DESC LIMIT 1
                """, (entered_id,))
                order = cursor.fetchone()

            if not order:
                messagebox.showerror("Not Found", "No order found with that ID. Please try again.")
                return

            order_id, name, ordered_items, total = order

            tk.Label(image_frame, text=f"Hello {name}! 👋", font=("Georgia", 16, "bold"), bg="#f5f0e1", fg="#3e2723").pack(pady=(20, 5))
            tk.Label(image_frame, text="Thank you for your patience — your order details are below:", font=("Georgia", 12, "italic"), bg="#f5f0e1", fg="#4e342e").pack(pady=5)

            summary_frame = tk.Frame(image_frame, bg="#f5f0e1")
            summary_frame.pack(pady=10)

            scrollbar = tk.Scrollbar(summary_frame)
            scrollbar.pack(side="right", fill="y")

            summary_box = tk.Text(summary_frame, width=70, height=12, font=("Georgia", 12), bg="#fffaf0", yscrollcommand=scrollbar.set)
            summary_box.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=summary_box.yview)

            summary_box.insert(tk.END, f"🧾 Order ID: {order_id}\n\n")
            summary_box.insert(tk.END, "Your Order:\n")
            summary_box.insert(tk.END, f"{ordered_items}\n\n")
            summary_box.insert(tk.END, f"💰 Total Billing Amount: ₹{total}\n")
            summary_box.config(state="disabled")

            # --- Updated Cancel Order Button ---
            def cancel_this_order():
                oid = simpledialog.askinteger("Cancel Order", "Enter Order ID to cancel:")
                if not oid:
                    return
                try:
                    cursor.execute("""
                        SELECT c.Name 
                        FROM Orders o
                        JOIN Customer c ON o.CustomerID = c.CustomerID
                        WHERE o.OrderID = %s
                    """, (oid,))
                    result = cursor.fetchone()
                    if not result:
                        messagebox.showerror("Not Found", f"No order found with Order ID {oid}.")
                        return
                    customer_name = result[0]

                    cursor.execute("DELETE FROM Orders WHERE OrderID = %s", (oid,))
                    db.commit()

                    # Reset AUTO_INCREMENT in Python
                    cursor.execute("SELECT IFNULL(MAX(OrderID), 0) FROM Orders")
                    max_id = cursor.fetchone()[0]
                    cursor.execute(f"ALTER TABLE Orders AUTO_INCREMENT = {max_id + 1}")
                    db.commit()

                    messagebox.showinfo("Order Cancelled", f"Order ID {oid} for customer '{customer_name}' has been deleted successfully!")

                    show_order_page()

                except Exception as e:
                    messagebox.showerror("Error", f"Unable to cancel order:\n{e}")

            tk.Button(image_frame, text="❌ Cancel Order", command=cancel_this_order, bg="#8b0000", fg="white", font=("Georgia", 11, "bold"), width=15).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error fetching order details:\n{e}")

    tk.Button(input_frame, text="Show Order", command=fetch_order, bg="#4e342e", fg="white", font=("Georgia", 11, "bold"), width=12).grid(row=0, column=2, padx=10)

# ----------------- HEADING -----------------
heading_frame = tk.Frame(root, bg="#3e2723")
heading_frame.pack(fill="x")

heading = tk.Label(heading_frame, text="Welcome to Uncle Joe's Café", font=("Georgia", 26, "italic bold"), bg="#3e2723", fg="#fbe9e7", pady=15)
heading.pack()

# ----------------- MENU BAR -----------------
menu_frame = tk.Frame(root, bg="#3e2723")
menu_frame.pack(fill="x", pady=5)

menu_labels = ["Home", "Customer Corner", "Orders Corner"]
menu_functions = [show_home_page, show_customer_page, show_order_page]

for i, (label_text, func) in enumerate(zip(menu_labels, menu_functions)):
    label = tk.Label(menu_frame, text=label_text, font=("Georgia", 11, "italic bold"), bg="#5d4037", fg="#fbe9e7", width=15, relief="raised", bd=1)
    label.grid(row=0, column=i, padx=6, pady=5, sticky="nsew")
    label.bind("<Button-1>", func)
    menu_frame.columnconfigure(i, weight=1)

# ----------------- IMAGE FRAME -----------------
image_frame = tk.Frame(root, bg="#f5f0e1")
image_frame.pack(fill="both", expand=True, pady=(10, 0))
show_home_page()

# ----------------- FOOTER -----------------
footer_frame = tk.Frame(root, bg="#f5f0e1")
footer_frame.pack(fill="x", side="bottom", pady=5, padx=15)

footer = tk.Label(footer_frame, text="The 2 main caretakers are Tanu Priya and Niharika", font=("Georgia", 12, "italic"), bg="#f5f0e1", fg="#4e342e")
footer.pack(side="left")

time_label = tk.Label(footer_frame, font=("Georgia", 11, "italic"), bg="#f5f0e1", fg="#3e2723")
time_label.pack(side="right")

update_time()
root.mainloop()
