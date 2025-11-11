packages_sent = 0
total_weight_sent = 0
current_package_weight = 0

most_unused_capacity = -1
package_with_most_unused = 0


print("Enter the maximum number of items to be shipped:")
max_items = int(input())


for item_count in range(max_items):
    print(f"Enter weight for item {item_count + 1} (1-10 kg, or 0 to finish):")
    item_weight = int(input())

    if item_weight == 0:
        print("Finishing program because weight 0 was entered.")
        break

    elif item_weight < 1 or item_weight > 10:
        print("Error: Item weight must be between 1 and 10 kg. Skipping this item.")
        continue

    else:
        total_weight_sent = total_weight_sent + item_weight


        if current_package_weight + item_weight > 20:
            unused_capacity = 20 - current_package_weight
            if unused_capacity > most_unused_capacity:
                most_unused_capacity = unused_capacity
                package_with_most_unused = packages_sent + 1
            packages_sent = packages_sent + 1

            current_package_weight = item_weight

        else:

            current_package_weight = current_package_weight + item_weight


if current_package_weight > 0:


    unused_capacity = 20 - current_package_weight
    if unused_capacity > most_unused_capacity:
        most_unused_capacity = unused_capacity
        package_with_most_unused = packages_sent + 1


    packages_sent = packages_sent + 1

print("----------------------------------------------------")

if packages_sent > 0:
    total_unused_capacity = (packages_sent * 20) - total_weight_sent

    print("\n--- Shipping Report ---")
    print(f"Number of packages sent: {packages_sent}")
    print(f"Total weight of packages sent: {total_weight_sent} kg")
    print(f"Total 'unused' capacity: {total_unused_capacity} kg")
    print(f"Package with most unused capacity: Package #{package_with_most_unused}")
    print(f"Unused capacity in that package: {most_unused_capacity} kg")
else:
    print("No items were shipped.")