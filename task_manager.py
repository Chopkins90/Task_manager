# Importing libraries
import os
from datetime import datetime, date
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function for registering new user
def reg_user():
    new_user = False
    new_pass = False

    # Takes new username and password and checks for duplicates
    while new_user == False:
        print('(-1 to return to the menu)')
        new_username = input("New Username: ")
        if new_username in username_password.keys():
            print("User already exists.")
        elif new_username == '-1':
            print('')
            break
        elif new_username == "":
            print('Username cannot be empty.')
        else:
            new_user = True

        while new_pass == False and new_user == True:
            new_password = input("New Password: ") 
            if new_password == '':
                print('Password cannot be empty.')
            else:
                confirm_password = input("Confirm Password: ")

                if new_password == confirm_password:
                    print("New user added.\n")
                    username_password[new_username] = new_password
                    new_pass = True
                    
                    # Adds user and password to user.txt file.
                    with open('user.txt', 'w') as out_file:
                        user_data = []
                        for k in username_password:
                            user_data.append(f"{k};{username_password[k]}")
                        out_file.write("\n".join(user_data))
                
                else:
                    print("Passwords do no match")


# Function to add new tasks
def add_task():
    task_menu = 0
    curr_date = date.today()

    # Takes username and checks if valid
    while task_menu == 0:
        print('(-1 to return to the menu)')
        task_username = input("User assigned to task: ")
        if task_username == '-1':
            print('')
            return
        elif task_username not in username_password.keys(): 
            print("\nUser does not exist. Please enter a valid username")
        else:
            task_menu += 1 

    # Takes task title
    while task_menu == 1:
        task_title = input("Task title: ")
        if task_title == '-1':
            break
        elif task_title != '':
            task_menu += 1
        else:
            print('\nTask title cannot be empty')
    
    # Takes task decription
    while task_menu == 2:
        task_description = input("Task description: ")
        if task_description == '-1':
            break
        elif task_description != '':
            task_menu += 1
        else:
            print('\nTask description cannot be empty')

    # Takes task due date
    while task_menu == 3:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            if task_due_date == '-1':
                break
            datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            task_menu += 1
        except ValueError:
            print("\nInvalid entry. Please use the format specified")

    if task_menu == 4:
        # Adds task to tasks.txt file
        try:
            with open('tasks.txt', 'a') as file:
                file.writelines(f'{task_username};{task_title};{task_description};{task_due_date};{curr_date};No\n')
                print('\nTask sucessfully added\n')
            
        # Created tasks file if not found
        except FileNotFoundError:
            file = open('tasks.txt','w')
            file.writelines(f'{task_username};{task_title};{task_description};{task_due_date};{curr_date};No\n')
            print('\nTask sucessfully added\n')
            file.close()
        
        # Writes created task to file
        


# Function to view all tasks
def view_all():
    with open('tasks.txt','r') as file: 
        display_list = file.readlines()
        for line in display_list:
            line = line.split(';')
            print(f'Task:              {line[1]}')
            print(f'Assigned To:       {line[0]}')
            print(f'Date assigned:     {line[4]}')
            print(f'Date Due:          {line[3]}')
            if line[5] == 'No\n' or line[5] == 'No':
                print('Task Complete?     No')
            else:
                print('Task Complete?     Yes')
            print(f'Task Desription:   {line[2]}\n')


# Function to view and edit current user tasks
def view_mine():
    edit_menu = 0
    user_tasks = []
    tasks_list = []
    task_number = 1

    while edit_menu == 0:
        # Reads tasks.txt file and seperates users tasks
        with open('tasks.txt','r+') as file:
            content = file.readlines()
        for i in content:
            i = i.split(';')
            if i[0] == curr_user:
                i = ';'.join(i)
                user_tasks.append(i)
            else:
                i = ';'.join(i)
                tasks_list.append(i)

        # Displays users tasks
        for i in user_tasks:
            i = i.split(';')
            print(f'Task Number:       {task_number}')
            print(f'Task:              {i[1]}')
            print(f'Assigned To:       {i[0]}')
            print(f'Date assigned:     {i[4]}')
            print(f'Date Due:          {i[3]}')
            if i[5] == 'No\n' or i[5] == 'No':
                print('Task Complete?     No')
            else:
                print('Task Complete?     Yes')
            print(f'Task Desription:   {i[2]}\n')
            task_number += 1
        edit_menu += 1

    while edit_menu == 1: 
        # Takes user task number input 
        print('(-1 to return to the menu)')
        print('Enter the task number of the task you want to view:')
        try:
            input_task_number = int(input(': '))
            input_task_number -=1
        except ValueError:
            print('Task not found')
            continue
        if input_task_number == -1:
            break

        # Displays users selected task
        try:
            user_tasks[input_task_number] = user_tasks[input_task_number].split(';')
            print(f'Task:              {user_tasks[input_task_number][1]}')
            print(f'Assigned To:       {user_tasks[input_task_number][0]}')
            print(f'Date assigned:     {user_tasks[input_task_number][4]}')
            print(f'Date Due:          {user_tasks[input_task_number][3]}')
        except IndexError:
            print('Task not found')
            continue
        if user_tasks[input_task_number][5] == 'No\n' or user_tasks[input_task_number][5] == 'No':
            print('Task Complete?     No')
        else:
            print('Task Complete?     Yes')
        print(f'Task Desription:   {user_tasks[input_task_number][2]}\n')
        edit_menu += 1
    
    # Task edit menu
    while edit_menu == 2:
        menu = input('''Enter one of the following Options:
m  - Mark task as complete
eu - Edit the user assigned to the task
ed - Edit Due Date
r  - Return to main menu
: ''').lower()
        
        # Marks task as complete
        if menu == 'm':
            if user_tasks[input_task_number][5] == 'Yes\n' or user_tasks[input_task_number][5] == 'Yes':
                print('\nTask is already marked as complete')
                continue
            else:
                user_tasks[input_task_number][5] = 'Yes\n'
                user_tasks[input_task_number] = ';'.join(user_tasks[input_task_number])
                print('Task marked as complete!')
                edit_menu += 1
        
        # Changes to user assigned to task and checks for valid username
        elif menu == 'eu':
            if user_tasks[input_task_number][5] == 'No\n' or user_tasks[input_task_number][5] == 'No':
                print(f'Current user assigned to task: {user_tasks[input_task_number][0]}')
                print('Enter new user assigned to task: ')
                new_task_user  = input(': ')
                if new_task_user in username_password.keys():
                    user_tasks[input_task_number][0] = new_task_user
                    user_tasks[input_task_number] = ';'.join(user_tasks[input_task_number])
                    edit_menu += 1
                else:
                    print('Username not found')
                    continue
            else:
                print('\nCannot edit completed tasks.')
                continue
            
        # Changes Due date
        elif menu == 'ed':
            if user_tasks[input_task_number][5] == 'No\n':
                print(f'\nCurrent Due Date: {user_tasks[input_task_number][3]}')
                print('Enter new Due Date: ')
                try:
                    user_tasks[input_task_number][3]  = input("Due date of task (YYYY-MM-DD): ") 
                    datetime.strptime(user_tasks[input_task_number][3], DATETIME_STRING_FORMAT)
                    print(user_tasks[input_task_number][3])
                    user_tasks[input_task_number] = ';'.join(user_tasks[input_task_number])
                    edit_menu += 1
                except ValueError:
                    print("Invalid datetime format. Please use the format specified")
            else:
                print('\nCannot edit completed tasks.')
                continue

        elif menu == 'r':
            break

        else:
            print('\nInvalid input')
            continue

        # Updates task changes to tasks.txt file
        if edit_menu == 3:
            user_tasks += tasks_list
            user_tasks = ''.join(user_tasks)
            with open('tasks.txt', 'w+') as file:
                file.write(user_tasks)
                break


#Function to generate task overview
def task_overview():
    completed_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0

    with open('tasks.txt','r') as file:
        content = file.readlines()

        # Counts total number of tasks
        for count, line in enumerate(content):
            total_tasks = count + 1
        
        # Counts complete and incomplete tasks
        for i in content:
            i = i.split(';')
            if i[5] == 'Yes\n' or i[5] == 'Yes':
                completed_tasks += 1
            else:
                incomplete_tasks += 1

            # Counts overdue tasks
            i[3] = datetime.strptime(i[3],'%Y-%m-%d')
            i[4] = datetime.strptime(i[4],'%Y-%m-%d')
            if i[3] < i[4] and i[5] == 'No\n':
                overdue_tasks +=1

    incomplete_percent = incomplete_tasks / total_tasks * 100
    overdue_percent = overdue_tasks / total_tasks * 100

    # Created file_overview.txt file and updates task statistics
    with open('file_overview.txt','w') as file:
        file.write(f'Completed Tasks: {completed_tasks}\n')
        file.write(f'Incomplete Tasks: {incomplete_tasks}\n')
        file.write(f'Overdue Tasks: {overdue_tasks}\n')
        file.write(f'Incomplete: {int(incomplete_percent)}%\n')
        file.write(f'Overdue: {int(overdue_percent)}%\n')


#Function to generate user task overview
def user_overview():
    total_users = 0
    total_tasks = 0
    tasks_list = []
    complete_list = []
    incomplete_list = []
    incomplete_overdue = []
    
    # Counts total number of users
    with open('user.txt','r') as file:
        content = file.readlines()
        for count, line in enumerate(content): 
            total_users = count + 1

     # Counts total number of tasks
    with open('tasks.txt','r') as file:
        content = file.readlines()
        for count, line in enumerate(content):
            total_tasks = count + 1
        
        # Creates a list of users for each task
        for i in content:
            i = i.split(';')
            tasks_list.append(i[0])

            # Checks if task is complete/incomplete and adds to relevent list
            if i[5] == 'No\n' or i[5] == 'No':
                incomplete_list.append(i[0])

            else:
                complete_list.append(i[0])

            i[3] = datetime.strptime(i[3],'%Y-%m-%d')
            i[4] = datetime.strptime(i[4],'%Y-%m-%d')
            if i[3] < i[4] and i[5] == 'No\n':
                incomplete_overdue.append(i[0])
                
    # Counts how many tasks for each user 
    task_dict = {i:tasks_list.count(i) for i in tasks_list}
    file_list = list(task_dict.items())

    # Counts how many complete tasks for each user
    complete_dict = {i:complete_list.count(i) for i in complete_list}
    complete_file_list = list(complete_dict.items())

    # Counts how many incomplete tasks for each user
    incomplete_dict = {i:incomplete_list.count(i) for i in incomplete_list}
    incomplete_file_list = list(incomplete_dict.items())

    # Counts how many incomplete, overdue tasks for each user
    overdue_dict = {i:incomplete_overdue.count(i) for i in incomplete_overdue}
    overdue_file_list = list(overdue_dict.items())

    # Creates file_overview.txt and updates file 
    with open('user_overview.txt','w') as file:
        file.write(f'Total number of users: {total_users}\n')
        file.write(f'Total number of tasks: {total_tasks}\n')

        # Total tasks assigned to user and percentage of total tasks assigned
        for i in file_list:
            user_total_percent = i[1] / total_tasks * 100
            file.write(f'\nTotal tasks assigned to {i[0]}: {i[1]}\n')
            file.write(f'Percentage of total tasks assigned: {int(user_total_percent)}%\n')

            # Calculates percentage of tasks complete
            for j in complete_file_list:
                if i[0] == j[0]:
                    complete_percent = j[1] / i[1] * 100 
                    file.write(f'Tasks complete: {int(complete_percent)}%\n')

            # Calculates percentage of tasks incomplete
            for j in incomplete_file_list:
                if i[0] == j[0]:
                    incomplete_percent = j[1] / i[1] * 100 
                    file.write(f'Tasks incomplete: {int(incomplete_percent)}%\n')

            # Calculates percentage of tasks incomplete and overdue
            for j in overdue_file_list:
                if i[0] == j[0]:
                    overdue_percent = j[1] / i[1] * 100 
                    file.write(f'Tasks overdue percent: {int(overdue_percent)}%\n')
               

#====Login Section====
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Creates user.txt file with a default account if one is not found
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Opening user.txt file for login checks
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    # User login input and validation checks
    print("LOGIN")
    curr_user = input('Username: ')
    curr_pass = input('Password: ')
    if curr_user not in username_password.keys():
        print('\nIncorrect username or password')
        continue
    elif username_password[curr_user] != curr_pass:
        print('\nIncorrect Password')
        continue
    else:
        print('Login Successful\n')
        logged_in = True

#=====Opening Menu=====
while True:
    menu = input('''Enter one of the following options:
r  - Register a new user
a  - Add a task
va - View all tasks
vm - View and edit my tasks
gr - Generate reports
ds - Display statistics
e  - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr':
        task_overview()
        user_overview()
        print('\nReport files created!')

    elif menu == 'ds':
        if curr_user == 'admin':
            task_overview()
            user_overview()
            with open('file_overview.txt','r') as file:
                content = file.readlines()
                for line in content:
                    print(line, end= '',)
                print('')
            
            with open('user_overview.txt','r') as file:
                content = file.readlines()
                for line in content:
                    print(line, end= '',)
                print('')
        else:
            print('\nTask statistics can only be viewed by an admin')
    elif menu == 'e':
        exit()

    else:
        print('\nInvalid input')