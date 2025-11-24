def execute_balance(current_balance, history):
    amount_str = input("Enter amount to add (or negative to subtract): ")
    amount = float(amount_str)  # Convert text to number

    new_balance = current_balance + amount

    history.append(f"Balance updated by {amount}. New balance: {new_balance}")
    print("Balance updated successfully.")

    return new_balance


def execute_purchase(current_balance, inventory, history):
    name = input("Product name: ")
    price = float(input("Price per unit: "))
    qty = int(input("Quantity: "))

    total_cost = price * qty

    if total_cost > current_balance:
        print(f"Error: Not enough funds. Cost is {total_cost}, you have {current_balance}")
        return current_balance  # Return original balance (nothing spent)

    if name in inventory:
        inventory[name]['qty'] = inventory[name]['qty'] + qty
        inventory[name]['price'] = price
    else:
        inventory[name] = {'price': price, 'qty': qty}

    new_balance = current_balance - total_cost

    history.append(f"Purchased {qty} {name}. Total cost: {total_cost}")
    print("Purchase recorded.")

    return new_balance  # Return the updated balance


def execute_sale(current_balance, inventory, history):
    name = input("Product name: ")
    price = float(input("Selling price per unit: "))
    qty = int(input("Quantity: "))

    if name not in inventory:
        print("Error: Product not found in warehouse.")
        return current_balance  # Return original balance

    if inventory[name]['qty'] < qty:
        print(f"Error: Not enough stock. Available: {inventory[name]['qty']}")
        return current_balance  # Return original balance

    inventory[name]['qty'] = inventory[name]['qty'] - qty

    total_revenue = price * qty
    new_balance = current_balance + total_revenue

    history.append(f"Sold {qty} {name}. Total revenue: {total_revenue}")
    print("Sale recorded.")

    return new_balance  


def execute_list(inventory):
    print("\n--- Warehouse Inventory ---")
    # Check if empty
    if not inventory:
        print("Warehouse is empty.")

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

    if from_input == "" and to_input == "":
        for line in history:
            print(line)
    else:
        start = int(from_input)
        end = int(to_input)

        if start < 0 or end > len(history):
            print("Error: Indices out of range.")
        else:
            subset = history[start:end]
            for line in subset:
                print(line)


def main():
    balance = 0.0
    inventory = {}
    history = []

    print("Welcome to the Company Management System.")

    while True:
        print("\nAvailable commands: balance, sale, purchase, account, list, warehouse, review, end")
        command = input("Enter command: ")

        if command == "end":
            print("Terminating program. Goodbye!")
            break

        elif command == "balance":
            balance = execute_balance(balance, history)

        elif command == "purchase":
            balance = execute_purchase(balance, inventory, history)

        elif command == "sale":
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
