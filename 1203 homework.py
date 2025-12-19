import sys
import csv
import os

# 1. Check if the basic arguments (src and dst) are provided
if len(sys.argv) < 3:
    print("Usage: python reader.py <src> <dst> <change1> <change2> ...")
    sys.exit()

src = sys.argv[1]
dst = sys.argv[2]
changes = sys.argv[3:]

# 2. Check if the source file exists
if not os.path.isfile(src):
    print(f"Error: The file '{src}' does not exist.")
    print("Files in this directory:", os.listdir('.'))
    sys.exit()

# 3. Read the CSV file into a list of lists
data = []
try:
    with open(src, mode='r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit()

# 4. Apply the changes
for change in changes:
    # A change looks like "0,0,piano"
    parts = change.split(',')

    if len(parts) != 3:
        print(f"Skipping invalid change format: {change}")
        continue

    try:
        col = int(parts[0])
        row = int(parts[1])
        new_value = parts[2]

        # Apply the change (Note: data[row][column])
        data[row][col] = new_value

    except IndexError:
        print(f"Error: Row {row} or Column {col} is out of bounds for {change}")
    except ValueError:
        print(f"Error: Row/Col must be numbers in {change}")

# 5. Display the modified content in the terminal
print("\nModified CSV Content:")
for row in data:
    print(",".join(row))

# 6. Save the modified data to the destination path
try:
    with open(dst, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    print(f"\nSuccess! Modified file saved as: {dst}")
except Exception as e:
    print(f"Error saving file: {e}")