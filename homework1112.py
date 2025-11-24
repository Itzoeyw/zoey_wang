def execute_balance(current_balance, history):
    # Ask for input
    amount_str = input("Enter amount to add (or negative to subtract): ")
    amount = float(amount_str)  # Convert text to number

    # Calculate new balance
    new_balance = current_balance + amount

    # Save to history
    history.append(f"Balance updated by {amount}. New balance: {new_balance}")
    print("Balance updated successfully.")

    # IMPORTANT: Return the new balance so main() can save it
    return new_balance


def execute_purchase(current_balance, inventory, history):
    name = input("Product name: ")
    price = float(input("Price per unit: "))
    qty = int(input("Quantity: "))

    total_cost = price * qty

    # Check 1: Do we have enough money?
    if total_cost > current_balance:
        print(f"Error: Not enough funds. Cost is {total_cost}, you have {current_balance}")
        return current_balance  # Return original balance (nothing spent)

    # Check 2: Update Inventory
    if name in inventory:
        # Product exists, add quantity and update price
        inventory[name]['qty'] = inventory[name]['qty'] + qty
        inventory[name]['price'] = price
    else:
        # New product, create it
        inventory[name] = {'price': price, 'qty': qty}

    # Execute Payment
    new_balance = current_balance - total_cost

    # Update History
    history.append(f"Purchased {qty} {name}. Total cost: {total_cost}")
    print("Purchase recorded.")

    return new_balance  # Return the updated balance


def execute_sale(current_balance, inventory, history):
    name = input("Product name: ")
    price = float(input("Selling price per unit: "))
    qty = int(input("Quantity: "))

    # Check 1: Does product exist?
    if name not in inventory:
        print("Error: Product not found in warehouse.")
        return current_balance  # Return original balance

    # Check 2: Do we have enough stock?
    if inventory[name]['qty'] < qty:
        print(f"Error: Not enough stock. Available: {inventory[name]['qty']}")
        return current_balance  # Return original balance

    # Execute Sale
    inventory[name]['qty'] = inventory[name]['qty'] - qty

    total_revenue = price * qty
    new_balance = current_balance + total_revenue

    # Update History
    history.append(f"Sold {qty} {name}. Total revenue: {total_revenue}")
    print("Sale recorded.")

    return new_balance  # Return the updated balance


def execute_list(inventory):
    print("\n--- Warehouse Inventory ---")
    # Check if empty
    if not inventory:
        print("Warehouse is empty.")

    # Loop through dictionary
    for name in inventory:
        p = inventory[name]['price']
        q = inventory[name]['qty']
        print(f"Product: {name} | Price: {p} | Qty: {q}")


def execute_warehouse(inventory):
    name = input("Enter product name to check: ")
    if name in inventory:
        p = inventory[name]['price']
        q = inventory[name]['qty']
        print(f"Status: {name} -> Price: {p}, Quantity: {q}")
    else:
        print("Product not found.")


def execute_review(history):
    print(f"\nTotal operations recorded: {len(history)}")
    from_input = input("From index (leave empty for all): ")
    to_input = input("To index (leave empty for all): ")

    # If inputs are empty, show everything
    if from_input == "" and to_input == "":
        for line in history:
            print(line)
    else:
        # Convert inputs to integers
        start = int(from_input)
        end = int(to_input)

        # Check for valid range
        if start < 0 or end > len(history):
            print("Error: Indices out of range.")
        else:
            # Slice the list and print
            subset = history[start:end]
            for line in subset:
                print(line)


# --- MAIN PROGRAM ---

def main():
    # 1. Initialize Variables
    balance = 0.0
    inventory = {}
    history = []

    print("Welcome to the Company Management System.")

    # 2. Start Infinite Loop
    while True:
        print("\nAvailable commands: balance, sale, purchase, account, list, warehouse, review, end")
        command = input("Enter command: ")

        if command == "end":
            print("Terminating program. Goodbye!")
            break

        elif command == "balance":
            # Pass balance in, receive new balance out
            balance = execute_balance(balance, history)

        elif command == "purchase":
            # Pass balance in, receive new balance out
            balance = execute_purchase(balance, inventory, history)

        elif command == "sale":
            # Pass balance in, receive new balance out
            balance = execute_sale(balance, inventory, history)

        elif command == "account":
            print(f"Current Account Balance: {balance}")

        elif command == "list":
            execute_list(inventory)

        elif command == "warehouse":
            execute_warehouse(inventory)

        elif command == "review":
            execute_review(history)

        else:
            print("Error: Invalid command. Please try again.")


main()