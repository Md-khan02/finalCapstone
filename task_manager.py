# This project will focus on working with files and string manipulation. It also requies usage of conditional logic and loops in this task.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Ensuring the existence of necessary files
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Function to read task data from file
def read_tasks():
    task_list = []
    with open("tasks.txt", "r") as task_file:
        for line_number, line in enumerate(task_file, start=1):
            if line.strip():
                components = line.strip().split(";")
                if len(components) != 6:
                    print(f"Skipping line {line_number}: Incorrect number of components.")
                    continue
                try:
                    # Attempt to parse the date according to the expected format
                    due_date = datetime.strptime(components[3], DATETIME_STRING_FORMAT)
                    assigned_date = datetime.strptime(components[4], DATETIME_STRING_FORMAT)
                except ValueError as e:
                    print(f"Error parsing date on line {line_number}: {e}. Skipping this task.")
                    continue
                task = {
                    'username': components[0],
                    'title': components[1],
                    'description': components[2],
                    'due_date': due_date,
                    'assigned_date': assigned_date,
                    'completed': components[5].strip() == "Yes"
                }
                task_list.append(task)
    return task_list
       
# Function to read user data from file
def read_users():
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")
    username_password = {user.split(';')[0]: user.split(';')[1] for user in user_data if user}
    return username_password

# Function to register a new user
def reg_user(username_password):
    new_username = input("New Username: ")
    if new_username in username_password:
        print("This username already exists. Please try a different username.")
        return
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    if new_password == confirm_password:
        username_password[new_username] = new_password
        with open("user.txt", "w") as out_file:
            for username, password in username_password.items():
                out_file.write(f"{username};{password}\n")
            print("New user added.")
    else:
        print("Passwords do not match.")

# Function to add a new task
def add_task(username_password):
    task_list = read_tasks() # Read currecnt tasks
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password:
        print("User does not exist. Please enter a valid username. ")
        return
    task_title = input("Title of task: ")
    task_description = input("Description of Task: ")
    while True:
        task_due_date = input("Due date of task (YYYY-MM-DD): ")
        try:
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
    curr_date = datetime.now()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    # Write updated tasks back to file
    with open("tasks.txt", "w") as file:
        for task in task_list:
            file.write(f"{task['username']};{task['title']};{task['description']};{task['due_date'].strftime(DATETIME_STRING_FORMAT)};{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{'Yes' if task['completed'] else 'No'}\n")
    print("Task successfully added.")

# Function to view all tasks
def view_all():
    task_list = read_tasks()
    for task in task_list:
        print(f"Task: {task['title']}\nAssigned to: {task['username']}\nDate Assigned: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{'Yes' if task['completed'] else 'No'}\n")


# Function to aloow users to mark a task as complete or edit if it is not completed.
def edit_task(task_index, user_tasks, curr_user):
    selected_task = user_tasks[task_index]
    print("\n1. Mark the task as complete")
    print("2. Edit the task")
    option = input("Select an option: ")
    if option == '1':
        selected_task['completed'] = True
        save_tasks(user_tasks)
        print("Task marked as complete.")
    elif option == '2' and not selected_task['completed']:
        new_user = input("Enter the username of the person to assign the task to (press enter to leave unchanged): ")
        if new_user and new_user in read_users().keys():
            selected_task['username'] = new_user
        new_due_date = input("Enter new due date (YYYY-MM-DD) (press enter to leave unchanged): ")
        if new_due_date: 
            try:
                selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
            except ValueError:
                print("Invalid date format.")
            print("Task updated.")
        else:
            print("Completed tasks cannot be edited.")
        
# Function to save the chnages
def save_tasks(task_list):
    with open("tasks.txt", "w") as file:
        for task in task_list:
            file.write(f"{task['username']};{task['title']};{task['description']};{task['due_date'].strftime(DATETIME_STRING_FORMAT)};{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{'Yes' if task['completed'] else 'No'}\n")
# Function to view tasks assigned to the current user
def view_mine(curr_user):
    task_list = read_tasks()
    user_tasks = [task for task in task_list if task['username'] == curr_user]
    if not user_tasks:
        print("No tasks assigned to you.")
        return
    for i, task in enumerate(user_tasks, 1):
        print(f"{i}. Task: {task['title']} - Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\nDue Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\nTask Description: {task['description']}\nCompleted: {'Yes' if task['completed'] else 'No'}\n") 
    print("\nEnter a task number to edit or mark as complete, or '-1' to return to the main menu.")
    selection = input("Enter your choice: ")
    if selection.isdigit() and 0 < int(selection) <= len (user_tasks):
        edit_task(int(selection) -1, user_tasks, curr_user)
    elif selection == '-1':
        return
    else:
        print("Invalid selection.")


# Function to generate reports. This function generates 'task_overview.txt' and 'user_overview.txt'
def generate_reports():
    task_list = read_tasks()
    users = read_users()
    total_tasks = len(task_list)
    completed_tasks = sum(task['completed'] for task in task_list)
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(task['due_date'] < datetime.now() and not task['completed'] for task in task_list)
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    incomplete_percentage = (incomplete_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    with open("task_overview.txt", "w") as file:
        file.write(f"Total tasks: {total_tasks}\n")
        file.write(f"Completed tasks: {completed_tasks}\n")
        file.write(f"Incomplete tasks: {incomplete_tasks}\n")
        file.write(f"Overdue tasks: {overdue_tasks}\n")
        file.write(f"Percentage of tasks incomplete: {incomplete_percentage}%\n")
        file.write(f"Percentage of tasks overdue: {overdue_percentage}%\n")
    
    with open("user_overview.txt", "w") as file:
        total_users = len(users)
        file.write(f"Total users: {total_users}\n")
        file.write(f"Total tasks: {total_tasks}\n")
        for user, _ in users.items():
            user_tasks = [task for task in task_list if task['username'] == user]
            num_user_tasks = len(user_tasks)
            completed_user_tasks = sum(task['completed'] for task in user_tasks)
            incomplete_user_tasks = num_user_tasks - completed_user_tasks
            if num_user_tasks > 0:
                percentage_user_tasks = (num_user_tasks / total_tasks) * 100
                percentage_completed_user_tasks = (completed_user_tasks / num_user_tasks) * 100
                percentage_incomplete_user_tasks = (incomplete_user_tasks / num_user_tasks) * 100
            else:
                percentage_user_tasks = percentage_completed_user_tasks = percentage_incomplete_user_tasks = 0
            file.write(f"\nUser: {user}\n")
            file.write(f"Tasks assigned: {num_user_tasks}\n")
            file.write(f"Percentage of total tasks: {percentage_user_tasks}%n")
            file.write(f"Percentage of tasks completed: {percentage_completed_user_tasks}%\n")
            file.write(f"Percentage of tasks incomplete: {percentage_incomplete_user_tasks}%\n\n")


# Function to display statistics. This function will check if the 'task_overview.txt' and 'user_overview.txt' file exist. If they don't, it will call 'generate_reports()' to generate them.
def display_statistics():
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        print("Generating missing reports....")
        generate_reports()
    # Displaying task overview statistics
    print("\nTask Overview:")
    with open("task_overview.txt", "r") as file:
        print(file.read())
    
    # Displaying user overview statistics
    print("User Overview:")
    with open("user_overview.txt", "r") as file:
        print(file.read())

# Main program flow
def main():
    username_password = read_users()  # Load user data
    curr_user = None  # Variable to track the current logged-in user

    # User Login
    while curr_user is None:
        print("LOGIN")
        username = input("Username: ")
        password = input("Password: ")
        if username in username_password and username_password[username] == password: 
            print("Login successful!")
            curr_user = username
        else:
            print("Invalid login credentials.")
    
    # Main menu
    while True:
        print("\nPlease select one of the following options:")
        print("r - Register user")
        print("a - Add task")
        print("va - View all tasks")
        print("vm - View my tasks")
        print("gr - Generate reports")
        if curr_user == 'admin':
            print("ds- Display statistics")
        print("e - Exit")
        choice = input(": ").lower()

        if choice == 'r' and curr_user == 'admin':
            reg_user(username_password)
        elif choice == 'a':
            add_task(username_password)
        elif choice == 'va':
            view_all()
        elif choice == 'vm':
            view_mine(curr_user)
        elif choice == 'gr':
            generate_reports()
            print("Reports generated.")
        elif choice =='ds' and curr_user == 'admin':
            display_statistics()
        elif choice == 'e':
            print("Goodbye!")
            break
        else:
            print("Invalid option, Please try again.")

if __name__ == "__main__":
    main()



