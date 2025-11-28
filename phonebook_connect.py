import psycopg2
import csv

def connect():
    return psycopg2.connect(
        dbname="phonebook_db",
        user="postgres",
        password="123456789",  
        host="localhost",
        port="5432"
    )

def insert_from_csv():
    with open(r'/Users/hatefchalak/Desktop/Lab_10/phonebook.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip the header
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)",
                (row[0], row[1])
            )
    print("Data from CSV successfully added.")

def insert_from_input():
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    cur.execute(
        "INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)",
        (name, phone)
    )
    print("Data successfully added manually.")

# Function for updating data
def update_data():
    print("Choose what you want to update:")
    print("1 — Update name")
    print("2 — Update phone number")
    choice = input("Your choice: ")

    if choice == "1":
        # Update name
        old_name = input("Enter old name: ")
        new_name = input("Enter new name: ")
        cur.execute(
            "UPDATE phonebook SET first_name = %s WHERE first_name = %s",
            (new_name, old_name)
        )
        print(f"User name {old_name} updated to {new_name}.")
    
    elif choice == "2":
        # Update phone
        name = input("Enter username: ")
        new_phone = input("Enter new phone number: ")
        cur.execute(
            "UPDATE phonebook SET phone_number = %s WHERE first_name = %s",
            (new_phone, name)
        )
        print(f"Phone number for {name} updated to {new_phone}.")
    
    else:
        print("Invalid choice!")

# Added function query_data() to get data with filters
def query_data():
    print("Choose a filter for search:")
    print("1 — Show all users")
    print("2 — Find by name")
    print("3 — Find by phone number")
    print("4 — Find by part of the name")

    choice = input("Your choice: ")

    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
        results = cur.fetchall()
    elif choice == "2":
        name = input("Enter name to search: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (name,))
        results = cur.fetchall()
    elif choice == "3":
        phone = input("Enter phone number to search: ")
        cur.execute("SELECT * FROM phonebook WHERE phone_number = %s", (phone,))
        results = cur.fetchall()
    elif choice == "4":
        part = input("Enter part of the name: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", ('%' + part + '%',))
        results = cur.fetchall()
    else:
        print("Invalid choice!")
        return

    # Print the result
    if results:
        print("Search results:")
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("Nothing found.")

# Added ability to delete records from the table
def delete_data():
    print("Choose a deletion method:")
    print("1 — Delete by name")
    print("2 — Delete by phone number")

    choice = input("Your choice: ")

    if choice == "1":
        name = input("Enter username to delete: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
        print(f"User(s) with name '{name}' deleted.")
    
    elif choice == "2":
        phone = input("Enter phone number to delete: ")
        cur.execute("DELETE FROM phonebook WHERE phone_number = %s", (phone,))
        print(f"User with number '{phone}' deleted.")
    
    else:
        print("Invalid choice!")

# Connection
conn = connect()
cur = conn.cursor()

print("Choose data entry method:")
print("1 - Load from CSV")
print("2 - Enter manually")
print("3 - Update data")
print("4 - Find data")
print("5 - Delete data")

choice = input("Your choice: ")

if choice == "1":
    insert_from_csv()
elif choice == "2":
    insert_from_input()
elif choice =="3":
    update_data()
elif choice =="4":
    query_data()
elif choice =="5":
    delete_data()
else:
    print("Invalid choice!")

conn.commit()
cur.close()
conn.close()