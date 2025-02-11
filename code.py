import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import re

# Graph for city connections and distances
city_graph = {
    'Warehouse_Mumbai': [('Pune', 50), ('Nashik', 200), ('Goa', 400), ('Mumbai', 0)],
    'Warehouse_Delhi': [('Jaipur', 280), ('Agra', 210), ('Chandigarh', 260), ('Delhi', 0)],
    'Pune': [('Nashik', 100), ('Hyderabad', 500), ('Goa', 350)],
    'Nashik': [('Indore', 300), ('Ahmedabad', 400)],
    'Jaipur': [('Agra', 200), ('Udaipur', 400), ('Chandigarh', 500)],
    'Agra': [('Lucknow', 330), ('Kanpur', 280), ('Jaipur', 200)],
    'Hyderabad': [('Bangalore', 570), ('Chennai', 630), ('Pune', 500)],
    'Indore': [('Bhopal', 200), ('Ahmedabad', 250), ('Nashik', 300)],
    'Bhopal': [('Nagpur', 350), ('Indore', 200)],
    'Nagpur': [('Bhopal', 350), ('Hyderabad', 450)],
    'Lucknow': [('Kanpur', 90), ('Agra', 330)],
    'Bangalore': [('Chennai', 350), ('Kochi', 540), ('Hyderabad', 570)],
    'Udaipur': [('Ahmedabad', 260), ('Jaipur', 400)],
    'Chennai': [('Kochi', 700), ('Bangalore', 350)],
    'Goa': [('Pune', 350), ('Mumbai', 540)],
    'Ahmedabad': [('Jaipur', 670), ('Indore', 250)],
    'Chandigarh': [('Delhi', 250), ('Jaipur', 500)],
    'Mumbai': [],
    'Delhi': []
}

# Product catalog
product_list = [
    {"id": 1, "name": "Smartphone", "price": 30000},
    {"id": 2, "name": "Feature Phone", "price": 5000},
    {"id": 3, "name": "Gaming Laptop", "price": 60000},
    {"id": 4, "name": "Business Laptop", "price": 55000},
    {"id": 5, "name": "Mixer Grinder", "price": 4000},
    {"id": 6, "name": "Microwave", "price": 10000},
    {"id": 7, "name": "Air Conditioner", "price": 25000},
    {"id": 8, "name": "Heater", "price": 8000}
]

# User data storage (orders are stored per user)
user_data = {}
user_orders = {}
current_user = None

# Dijkstra's algorithm for shortest path
def dijkstra(graph, start):
    queue = [(0, start, [])]
    visited = set()
    shortest_paths = {}

    while queue:
        (distance, node, path) = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            path = path + [node]
            shortest_paths[node] = (distance, path)

            for (neighbor, weight) in graph.get(node, []):
                if neighbor not in visited:
                    heapq.heappush(queue, (distance + weight, neighbor, path))

    return shortest_paths

# Precompute shortest paths
shortest_paths_from_mumbai = dijkstra(city_graph, 'Warehouse_Mumbai')
shortest_paths_from_delhi = dijkstra(city_graph, 'Warehouse_Delhi')

# Tkinter Application
app = tk.Tk()
app.title("Warehouse Delivery System")
app.geometry("800x600")

def switch_frame(frame_func):
    for widget in app.winfo_children():
        widget.destroy()
    frame_func()

# Validation Functions
def is_valid_email(email):
    return bool(re.match(r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$", email))

def is_valid_password(password):
    return bool(re.match(r"^(?=.*[A-Z])(?=.*\d).{6,}$", password))

def is_valid_name(name):
    return bool(re.match(r"^[a-zA-Z]+$", name))

def is_valid_phone(phone):
    return bool(re.match(r"^\d{10}$", phone))

# Frame: Sign-In (First Page)
def sign_in_frame():
    frame = tk.Frame(app)
    frame.pack(expand=True)
    tk.Label(frame, text="Welcome to the Warehouse Delivery System", font=("Arial", 20)).pack(pady=20)
    tk.Button(frame, text="Log In", command=lambda: switch_frame(log_in_frame), width=20).pack(pady=10)
    tk.Button(frame, text="Sign Up", command=lambda: switch_frame(sign_up_frame), width=20).pack(pady=10)

# Frame: Sign-Up
def sign_up_frame():
    def handle_sign_up():
        email = email_var.get().strip()
        password = password_var.get().strip()
        confirm_password = confirm_password_var.get().strip()
        name = name_var.get().strip()
        phone = phone_var.get().strip()

        if email in user_data:
            messagebox.showerror("Error", "Account already exists. Try logging in.")
            return

        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format. Email must include '@' and '.com'.")
            return
        if not is_valid_password(password):
            messagebox.showerror("Error", "Invalid password. Must include one uppercase letter, one digit, and be at least 6 characters.")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if not is_valid_name(name):
            messagebox.showerror("Error", "Invalid name. Only letters are allowed.")
            return
        if not is_valid_phone(phone):
            messagebox.showerror("Error", "Invalid phone number. Must be exactly 10 digits.")
            return

        user_data[email] = {'password': password, 'name': name, 'phone': phone}
        user_orders[email] = []  # Initialize empty order history for the user
        messagebox.showinfo("Success", "Account created successfully!")
        switch_frame(log_in_frame)

    email_var, password_var, confirm_password_var, name_var, phone_var = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()

    frame = tk.Frame(app)
    frame.pack(expand=True)
    tk.Label(frame, text="Sign Up", font=("Arial", 20)).pack(pady=20)
    tk.Label(frame, text="Email:").pack()
    tk.Entry(frame, textvariable=email_var).pack()
    tk.Label(frame, text="Password:").pack()
    tk.Entry(frame, textvariable=password_var, show="*").pack()
    tk.Label(frame, text="Confirm Password:").pack()
    tk.Entry(frame, textvariable=confirm_password_var, show="*").pack()
    tk.Label(frame, text="Name:").pack()
    tk.Entry(frame, textvariable=name_var).pack()
    tk.Label(frame, text="Phone Number:").pack()
    tk.Entry(frame, textvariable=phone_var).pack()
    tk.Button(frame, text="Sign Up", command=handle_sign_up).pack(pady=10)
    tk.Button(frame, text="Back to Sign In", command=lambda: switch_frame(sign_in_frame)).pack(pady=5)

# Frame: Log-In
def log_in_frame():
    def handle_log_in():
        global current_user
        email = email_var.get().strip()
        password = password_var.get().strip()

        if email in user_data and user_data[email]['password'] == password:
            current_user = email
            switch_frame(main_menu_frame)
        else:
            messagebox.showerror("Error", "Incorrect email or password.")

    email_var, password_var = tk.StringVar(), tk.StringVar()

    frame = tk.Frame(app)
    frame.pack(expand=True)
    tk.Label(frame, text="Log In", font=("Arial", 20)).pack(pady=20)
    tk.Label(frame, text="Email:").pack()
    tk.Entry(frame, textvariable=email_var).pack()
    tk.Label(frame, text="Password:").pack()
    tk.Entry(frame, textvariable=password_var, show="*").pack()
    tk.Button(frame, text="Log In", command=handle_log_in).pack(pady=10)
    tk.Button(frame, text="Back to Sign In", command=lambda: switch_frame(sign_in_frame)).pack(pady=5)

# Frame: Main Menu
def main_menu_frame():
    frame = tk.Frame(app)
    frame.pack(expand=True)
    tk.Label(frame, text=f"Welcome, {user_data[current_user]['name']}!", font=("Arial", 20)).pack(pady=20)
    tk.Button(frame, text="View Products", command=view_products_frame).pack(pady=10)
    tk.Button(frame, text="Place Order", command=place_order_frame).pack(pady=10)
    tk.Button(frame, text="Order History", command=order_history_frame).pack(pady=10)
    tk.Button(frame, text="Log Out", command=lambda: switch_frame(sign_in_frame)).pack(pady=10)

# Frame: View Products
def view_products_frame():
    frame = tk.Frame(app)
    frame.pack(expand=True)
    tk.Label(frame, text="Available Products", font=("Arial", 20)).pack(pady=20)
    for product in product_list:
        tk.Label(frame, text=f"{product['id']}. {product['name']} - ₹{product['price']}").pack()
    tk.Button(frame, text="Back to Menu", command=lambda: switch_frame(main_menu_frame)).pack(pady=10)

# Frame: Place Order
def place_order_frame():
    frame = tk.Frame(app)
    frame.pack(expand=True)
    tk.Label(frame, text="Place an Order", font=("Arial", 20)).pack(pady=20)

    dest_city_var = tk.StringVar()
    cities = sorted([city for city in city_graph if not city.startswith('Warehouse')])
    tk.Label(frame, text="Select Destination City:").pack()
    ttk.Combobox(frame, textvariable=dest_city_var, values=cities).pack()

    product_idx_var = tk.StringVar()
    tk.Label(frame, text="Enter Product Number:").pack()
    tk.Entry(frame, textvariable=product_idx_var).pack()

    tk.Label(frame, text="Available Products", font=("Arial", 16)).pack(pady=10)
    for product in product_list:
        tk.Label(frame, text=f"{product['id']}. {product['name']} - ₹{product['price']}").pack()

    def confirm_order():
        try:
            dest_city = dest_city_var.get()
            product_idx = int(product_idx_var.get())

            if dest_city not in cities:
                messagebox.showerror("Error", "Invalid destination city.")
                return

            selected_product = next((p for p in product_list if p['id'] == product_idx), None)
            if not selected_product:
                messagebox.showerror("Error", "Invalid product selection.")
                return

            product_name = selected_product['name']
            product_price = selected_product['price']

            mumbai_path = shortest_paths_from_mumbai.get(dest_city, (float('inf'), []))
            delhi_path = shortest_paths_from_delhi.get(dest_city, (float('inf'), []))

            if mumbai_path[0] < delhi_path[0]:
                optimal_warehouse = 'Warehouse_Mumbai'
                optimal_distance, optimal_path = mumbai_path
            else:
                optimal_warehouse = 'Warehouse_Delhi'
                optimal_distance, optimal_path = delhi_path

            if optimal_distance == float('inf'):
                messagebox.showerror("Error", "Delivery to this city is not possible.")
                return

            delivery_charge = optimal_distance
            total_cost = product_price + delivery_charge

            order_summary = (
                f"Product: {product_name}\n"
                f"Destination: {dest_city}\n"
                f"Warehouse: {optimal_warehouse}\n"
                f"Delivery Path: {' -> '.join(optimal_path)}\n"
                f"Distance: {optimal_distance} km\n"
                f"Product Price: ₹{product_price}\n"
                f"Delivery Charge: ₹{delivery_charge}\n"
                f"Total Cost: ₹{total_cost}"
            )
            confirm = messagebox.askyesno("Confirm Order", f"Order Summary:\n\n{order_summary}\n\nConfirm order?")
            if confirm:
                user_orders[current_user].append({
                    'product': product_name,
                    'product_cost': product_price,
                    'delivery_charge': delivery_charge,
                    'destination': dest_city,
                    'warehouse': optimal_warehouse,
                    'delivery_path': optimal_path,
                    'total_cost': total_cost
                })
                messagebox.showinfo("Success", f"Order placed successfully! Total Cost: ₹{total_cost}")
                switch_frame(main_menu_frame)
            else:
                messagebox.showinfo("Cancelled", "Order cancelled.")
        except ValueError:
            messagebox.showerror("Error", "Invalid product selection.")

    tk.Button(frame, text="Confirm Order", command=confirm_order).pack(pady=10)
    tk.Button(frame, text="Back to Menu", command=lambda: switch_frame(main_menu_frame)).pack(pady=5)

# Frame: Order History
def order_history_frame():
    frame = tk.Frame(app)
    frame.pack(expand=True)
    tk.Label(frame, text="Order History", font=("Arial", 20)).pack(pady=20)

    if not user_orders[current_user]:
        tk.Label(frame, text="No orders placed yet.").pack()
    else:
        for idx, order in enumerate(user_orders[current_user], 1):
            tk.Label(frame, text=f"Order {idx}:").pack()
            tk.Label(frame, text=f"Product: {order['product']}").pack()
            tk.Label(frame, text=f"Product Cost: ₹{order['product_cost']}").pack()
            tk.Label(frame, text=f"Delivery Charge: ₹{order['delivery_charge']}").pack()
            tk.Label(frame, text=f"Total Cost: ₹{order['total_cost']}").pack()
            tk.Label(frame, text=f"Delivery Path: {' -> '.join(order['delivery_path'])}").pack()
            tk.Label(frame, text="-"*50).pack()

    tk.Button(frame, text="Back to Menu", command=lambda: switch_frame(main_menu_frame)).pack(pady=10)

# Start with Sign-In Frame
switch_frame(sign_in_frame)

app.mainloop()