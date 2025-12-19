import ast
import os

# --- INITIALIZE DATA ---
balance = 0.0
inventory = {}
history = []

# --- LOAD DATA (At the start) ---
# We check if files exist. If they do, we read them.
# If not, we keep the empty starting values.

try:
    if os.path.exists("balance.txt"):
        with open("balance.txt", "r") as f:
            balance = float(f.read())

    if os.path.exists("inventory.txt"):
        with open("inventory.txt", "r") as f:
            inventory = ast.literal_eval(f.read())

    if os.path.exists("history.txt"):
        with open("history.txt", "r") as f:
            history = ast.literal_eval(f.read())
except Exception as e:
    print("Error loading files, starting with empty data.")

# --- MAIN PROGRAM LOOP ---
while True:
    print("\n--- Company Account & Warehouse ---")
    print("1. Balance  2. Sale  3. Purchase  4. Account  5. List  6. Warehouse  7. History  8. Quit")

    action = input("Choose an option: ")

    if action == "1":  # Balance (Add/Subtract money)
        amount = float(input("Enter amount to add/subtract: "))
        balance += amount
        history.append(f"Balance changed by {amount}")

    elif action == "2":  # Sale
        item = input("Product name: ")
        qty = int(input("Quantity: "))
        price = float(input("Price per unit: "))
        if item in inventory and inventory[item] >= qty:
            inventory[item] -= qty
            balance += (price * qty)
            history.append(f"Sold {qty} {item} for {price * qty}")
        else:
            print("Error: Not enough stock.")

    elif action == "3":  # Purchase
        item = input("Product name: ")
        qty = int(input("Quantity: "))
        price = float(input("Price per unit: "))
        cost = price * qty
        if balance >= cost:
            balance -= cost
            inventory[item] = inventory.get(item, 0) + qty
            history.append(f"Bought {qty} {item} for {cost}")
        else:
            print("Error: Not enough money.")

    elif action == "4":  # Account
        print(f"Current Balance: {balance}")

    elif action == "5":  # List (Inventory)
        print("Inventory:", inventory)

    elif action == "8":  # Quit and SAVE
        print("Saving data and exiting...")

        # Save Balance
        with open("balance.txt", "w") as f:
            f.write(str(balance))

        # Save Inventory (Write the dictionary as a string)
        with open("inventory.txt", "w") as f:
            f.write(str(inventory))

        # Save History (Write the list as a string)
        with open("history.txt", "w") as f:
            f.write(str(history))

        break