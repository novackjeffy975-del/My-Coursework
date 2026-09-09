import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("orders.json")

# PART: Menu (a) - Data
# Assigned to: Gordon Brighton
menu = {
    "Meals": {"1": ["Chicken Rice", 10000], "2": ["Beef Rice", 8000], "3": ["Pizza", 15000], "4": ["Rolex", 3000]},
    "Drinks": {"5": ["Water", 1000], "6": ["Sodas", 2000], "7": ["Milk", 2500], "8": ["Oner juice", 3000]},
    "Snacks": {"9": ["Samosa", 1000], "10": ["Mandazi", 500]}
}

riders = ["Lule", "Gordon", "Ibraah", "Ngise"]
statuses = ["Pending", "Out for Delivery", "Delivered"]
orders = []


# PART: Data Persistence
# Assigned to: Kirabo Mercynitah
def load_orders():
    global orders
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            loaded_data = json.load(file)
            if isinstance(loaded_data, list):
                orders = loaded_data
            else:
                orders = []
                print("Saved order data was invalid. Starting a new session.")
    except FileNotFoundError:
        print("No saved file found. Starting new session.")
    except json.JSONDecodeError:
        print("Saved order data is corrupted. Starting new session.")
        orders = []


def save_orders():
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(orders, file, indent=2)


# PART: Menu (b) - Display
# Assigned to: Garang Machar
def show_menu():
    print("\n--- CANTEEN MENU ---")
    for category in menu:
        print("\n" + category + ":")
        for item_num in menu[category]:
            item_name, price = menu[category][item_num]
            print(f"{item_num}. {item_name} - {price} UGX")


# PART: Order Taking (a) - Input helpers
# Assigned to: Asaba Emmanuel
def find_item(choice):
    for category in menu:
        if choice in menu[category]:
            return category, menu[category][choice]
    return None


def get_valid_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a number greater than 0.")
                continue
            return value
        except ValueError:
            print("Invalid number. Please enter a valid integer.")


# Take a new order from customer
# PART: Order Taking (a) - Cart building
# Assigned to: Ababa Emmanuel
# PART: Order Taking (b) - Processing (fee, total, saving)
# Assigned to: Lule Alex
def add_order():
    show_menu()
    cart = []
    subtotal = 0

    while True:
        choice = input("\nEnter item number (or 0 to stop): ")
        if choice == "0":
            break

        item = find_item(choice)
        if item is None:
            print("Invalid item number!")
            continue

        category, item_data = item
        name, price = item_data
        quantity = get_valid_integer("Enter quantity: ")
        cost = price * quantity
        subtotal += cost
        cart.append([name, quantity, cost])
        print(f"Added {name} x{quantity}")

    if len(cart) == 0:
        print("Order cancelled.")
        return

    # Lule Alex: Order Taking (b)
    if subtotal >= 30000:
        fee = 0
    elif subtotal >= 15000:
        fee = 1500
    else:
        fee = 3000

    total = subtotal + fee
    assigned_rider = riders[len(orders) % len(riders)]
    order_id = "ORD-" + str(len(orders) + 1)

    new_order = {
        "id": order_id,
        "items": cart,
        "subtotal": subtotal,
        "delivery_fee": fee,
        "total": total,
        "rider": assigned_rider,
        "status": "Pending"
    }

    orders.append(new_order)
    save_orders()
    print(f"\nSubtotal: {subtotal} UGX")
    print(f"Delivery fee: {fee} UGX")
    print(f"Total: {total} UGX. Rider: {assigned_rider}")
    # --- Lule Alex: Order Taking (b) ends here ---


# PART: Status Updates
# Assigned to: Ssekamate Hassan
# PART: Status Updates
# Assigned to: Atulinda Patrah Kamara
# Update status step by step
def change_status():
    if len(orders) == 0:
        print("\nNo orders found.")
        return

    order_id = input("\nEnter Order ID (e.g ORD-1): ").strip()
    for order in orders:
        if order["id"] == order_id:
            order["Status"] = "Out for Delivery"
            print("Status changed to Out for Delivery.")
            return # stop here, don't fall through to other logic
    print("Order not found.")


# PART: Sales Report
# Assigned to: Katongole Ibrahim
# PART: Sales Report
# Assigned to: Isaac Ngise
# Print basic summary report
def show_report():
    if len(orders) == 0:
        print("\nNo sales yet.")
        return

    total_sales = 0
    status_counts = {status: 0 for status in statuses}
    item_sales = {}
    for order in orders:
        total_sales += order["total"]
        if order.get("status") in status_counts:
            status_counts[order["status"]] += 1
        for item in order.get("items", []):
            name, quantity, _ = item
            item_sales[name] = item_sales.get(name, 0) + quantity

    print("\n--- SALES REPORT ---")
    print(f"Total Orders: {len(orders)}")
    print(f"Total Revenue: {total_sales} UGX")
    print("\nOrders by Status:")
    for status, count in status_counts.items():
        print(f"{status}: {count}")
    if item_sales:
        best_seller = max(item_sales, key=item_sales.get)
        print(f"\nBest-Selling Item: {best_seller} ({item_sales[best_seller]} sold)")



# PART: Integration (main program loop)
# Assigned to: All members - Lule Alex, Gordon Brighton, Garang Machar,
# Ababa Emmanuel, Kirabo Mercynitah, Atulinda Patrah Kamara
# Ssekamate Hassan, Isaac Ngise, Katongole Ibrahim
def main():
    load_orders()

    while True:
        print("\n==== Group 23 Fooddelivery App ====")
        print("\n1. Show Menu\n2. New Order\n3. Update Status\n4. View Report\n5. Exit")
        option = input("Choose option (1-5): ")
        if option == "1":
            show_menu()
        elif option == "2":
            add_order()
        elif option == "3":
            change_status()
        elif option == "4":
            show_report()
        elif option == "5":
            print("Goodbye!")
            break
        else:
            print("Wrong choice, try again.")


if __name__ == "__main__":
    main()