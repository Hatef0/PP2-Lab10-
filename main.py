import psycopg2
import csv
#Connectionn to database
conn = psycopg2.connect(host="localhost", dbname="phonebook",user="postgres", password="postgres", port=5432)
cur = conn.cursor()
#table creation
cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone BIGINT NOT NULL UNIQUE
            );
            """)

user_choice = int(input("Select the number of action you want to do :\n"
"1)Insert data (from CSV)\n" \
"2)Insert data (Manual)\n" \
"3)Update data\n" \
"4)Query\n" \
"5)Delete Data\n"\
"Select :"))
# resets the id to 1 if table is empty
def reset_sequence_if_empty():
    cur.execute("SELECT COUNT(*) FROM phonebook")
    row_count = cur.fetchone()[0]

    if row_count == 0:
        cur.execute("ALTER SEQUENCE phonebook_id_seq RESTART WITH 1")

def insert_csv():
  reset_sequence_if_empty()
  
  with open(r'/Users/hatefchalak/Desktop/Lab10/phonebook.csv', 'r') as file:
    data_reader = csv.reader(file)
    next(data_reader)
    for row in data_reader:
        cur.execute("""INSERT INTO phonebook (name, phone)  VALUES (%s, %s)""", row)
  print("Insert successful!")
def insert_manual():
  reset_sequence_if_empty()
  name_input = input("Enter name: ")
  phone_input = input("Enter phone number: ")
  cur.execute("""
      INSERT INTO phonebook(name, phone) VALUES (%s, %s)
      """, (name_input, phone_input)
  )
  print("input successful")
def update():
  id_to_update = input("Enter the ID of the record to update: ")
  choice_input = int(input("Update 1)Name or 2)Phone number ? "))
  if choice_input == 1:
    name_input = input("Enter new name: ")
    cur.execute(""" UPDATE phonebook SET name = %s WHERE id = %s
     """, (name_input, id_to_update))
    print("Update successful!")
  elif choice_input == 2:
    phone_input = int(input("Enter new phone number: "))
    cur.execute("""UPDATE phonebook SET phone = %s WHERE id = %s""", (phone_input, id_to_update))
    print("Update successful!")
  else:
    print("Enter a valid number")
def query():
  cur.execute("SELECT * FROM phonebook")
  for records in cur.fetchall():
    print(records)
def deletedata():
  query()
  user_input = input("Who to delete(names seperated by comma) ?").split(',')
  for name in user_input:
    name = name.strip()
    cur.execute("""DELETE FROM phonebook WHERE name = %s""", (name,))
  print("Delete successful!")


if 1 <= user_choice <= 5:
  if user_choice == 1:
    insert_csv()
  elif user_choice == 2:
    insert_manual()
  elif user_choice == 3:
    update()
  elif user_choice == 4:
    query()
  elif user_choice == 5:
    deletedata()
else:
  print("invalid input")

conn.commit()
cur.close()
conn.close()