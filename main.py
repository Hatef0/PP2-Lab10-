from db import create_tables, get_or_create_user, get_user_game
import subprocess  # Running snake.py as a separate process

# Create tables (if they are not created yet)
create_tables()

# Ask for the player's name
username = input("Enter your username: ")
user_id = get_or_create_user(username)

# Try to load the progress
data = get_user_game(user_id)
if data:
    score, level, _ = data
    print(f"Welcome back, {username}!")
    print(f"Current level: {level}, score: {score}")
else:
    print(f"New player {username} created.")

# Start the game and pass user_id as an argument
subprocess.run(["python", r"/Users/hatefchalak/Desktop/Lab_10/Snake/snake.py", str(user_id)])
