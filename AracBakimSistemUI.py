import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

# Connecting the database
def connect_to_db():
    return pyodbc.connect('DRIVER={SQL Server};SERVER=Babay;DATABASE=AracBakimSistemi;Trusted_Connection=yes;')

# Function to execute a query and return results
def execute_query(query, params=()):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            return results
        else:
            conn.commit()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        cursor.close()
        conn.close()

# Function to add a new customer
def add_customer():
    def submit():
        customer_id = id_entry.get()
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()

        if customer_id and name and phone and email and address:
            query = "INSERT INTO Musteriler (MusteriID, TamAd, TelefonNumarasi, Email, Adres) VALUES (?, ?, ?, ?, ?)"
            execute_query(query, (customer_id, name, phone, email, address))
            messagebox.showinfo("Success", "Customer added successfully!")
            add_window.destroy()
        else:
            messagebox.showerror("Input Error", "All fields are required.")

    add_window = tk.Toplevel(root)
    add_window.title("Add New Customer")

    tk.Label(add_window, text="Customer ID:").grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(add_window)
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Full Name:").grid(row=1, column=0, padx=10, pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Phone Number:").grid(row=2, column=0, padx=10, pady=5)
    phone_entry = tk.Entry(add_window)
    phone_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Email:").grid(row=3, column=0, padx=10, pady=5)
    email_entry = tk.Entry(add_window)
    email_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Address:").grid(row=4, column=0, padx=10, pady=5)
    address_entry = tk.Entry(add_window)
    address_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Button(add_window, text="Submit", command=submit).grid(row=5, column=0, columnspan=2, pady=10)

# Function to add a new vehicle
def add_vehicle():
    def submit():
        vehicle_id = id_entry.get()
        plate = plate_entry.get()
        brand = brand_entry.get()
        model = model_entry.get()
        customer_id = customer_id_entry.get()

        if vehicle_id and plate and brand and model and customer_id:
            query = "INSERT INTO Araclar (AracID, Plaka, Marka, Model, MusteriID) VALUES (?, ?, ?, ?, ?)"
            execute_query(query, (vehicle_id, plate, brand, model, customer_id))
            messagebox.showinfo("Success", "Vehicle added successfully!")
            add_window.destroy()
        else:
            messagebox.showerror("Input Error", "All fields are required.")

    add_window = tk.Toplevel(root)
    add_window.title("Add New Vehicle")

    tk.Label(add_window, text="Vehicle ID:").grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(add_window)
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_window, text="License Plate:").grid(row=1, column=0, padx=10, pady=5)
    plate_entry = tk.Entry(add_window)
    plate_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Brand:").grid(row=2, column=0, padx=10, pady=5)
    brand_entry = tk.Entry(add_window)
    brand_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Model:").grid(row=3, column=0, padx=10, pady=5)
    model_entry = tk.Entry(add_window)
    model_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Customer ID:").grid(row=4, column=0, padx=10, pady=5)
    customer_id_entry = tk.Entry(add_window)
    customer_id_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Button(add_window, text="Submit", command=submit).grid(row=5, column=0, columnspan=2, pady=10)

# Function to view all customers
def view_customers():
    customers = execute_query("SELECT MusteriID, TamAd, TelefonNumarasi, Email, Adres FROM Musteriler")

    if customers:
        view_window = tk.Toplevel(root)
        view_window.title("Customers")

        tree = ttk.Treeview(view_window, columns=("ID", "Full Name", "Phone", "Email", "Address"), show="headings")
        tree.heading("ID", text="Customer ID")
        tree.heading("Full Name", text="Full Name")
        tree.heading("Phone", text="Phone Number")
        tree.heading("Email", text="Email")
        tree.heading("Address", text="Address")

        for customer in customers:
            tree.insert("", "end", values=customer)

        tree.pack(fill=tk.BOTH, expand=True)
    else:
        messagebox.showinfo("No Data", "No customers found.")

# Query: Total Revenue by Service Type
def query_total_revenue():
    results = execute_query(
        "SELECT ST.ServisAdi, '' AS BlankColumn, SUM(SK.ToplamUcret) AS TotalRevenue FROM ServisTipleri ST "
        "JOIN ServisKayitlari SK ON ST.ServisTipiID = SK.ServisTipiID "
        "GROUP BY ST.ServisAdi"
    )

    if results:
        result_window = tk.Toplevel(root)
        result_window.title("Total Revenue by Service Type")

        tree = ttk.Treeview(result_window, columns=("Service Name", "", "Total Revenue"), show="headings")
        tree.heading("Service Name", text="Service Name")
        tree.heading("", text="")  # Blank column for the second part of the service name
        tree.heading("Total Revenue", text="Total Revenue")

        for result in results:
            tree.insert("", "end", values=result)

        tree.pack(fill=tk.BOTH, expand=True)
    else:
        messagebox.showinfo("No Data", "No revenue data found.")

# Query: View Service Records
def query_service_records():
    results = execute_query(
        "SELECT SK.ServisID, ST.ServisAdi, SK.ToplamUcret, A.Plaka "
        "FROM ServisKayitlari SK "
        "JOIN ServisTipleri ST ON SK.ServisTipiID = ST.ServisTipiID "
        "JOIN Araclar A ON SK.AracID = A.AracID"
    )

    if results:
        result_window = tk.Toplevel(root)
        result_window.title("Service Records")

        tree = ttk.Treeview(result_window, columns=("Record ID", "Service Name", "", "Total Cost", "License Plate"), show="headings")
        tree.heading("Record ID", text="Record ID")
        tree.heading("Service Name", text="Service Name")
        tree.heading("", text="")
        tree.heading("Total Cost", text="Total Cost")
        tree.heading("License Plate", text="License Plate")

        for result in results:
            tree.insert("", "end", values=result)

        tree.pack(fill=tk.BOTH, expand=True)
    else:
        messagebox.showinfo("No Data", "No service records found.")

# Query: View Vehicles
def query_vehicles():
    results = execute_query("SELECT AracID, Plaka, Marka, Model FROM Araclar")

    if results:
        result_window = tk.Toplevel(root)
        result_window.title("Vehicles")

        tree = ttk.Treeview(result_window, columns=("Vehicle ID", "License Plate", "Brand", "Model"), show="headings")
        tree.heading("Vehicle ID", text="Vehicle ID")
        tree.heading("License Plate", text="License Plate")
        tree.heading("Brand", text="Brand")
        tree.heading("Model", text="Model")

        for result in results:
            tree.insert("", "end", values=result)

        tree.pack(fill=tk.BOTH, expand=True)
    else:
        messagebox.showinfo("No Data", "No vehicles found.")

# Main application
def main_app():
    global root
    root = tk.Tk()
    root.title("Vehicle Maintenance System")
    root.geometry("400x600")
    root.configure(bg="#f0f0f0")

    tk.Label(root, text="Vehicle Maintenance System", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)

    buttons = [
        ("Add Customer", add_customer),
        ("View Customers", view_customers),
        ("Add Vehicle", add_vehicle),
        ("View Vehicles", query_vehicles),
        ("Total Revenue by Service Type", query_total_revenue),
        ("View Service Records", query_service_records)
    ]

    for text, command in buttons:
        tk.Button(root, text=text, command=command, font=("Arial", 12), bg="#0078d7", fg="white", width=30, height=2).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main_app()
