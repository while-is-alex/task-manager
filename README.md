# Task Manager
A web-application built with Python, Flask, SQL and Bootstrap. Create lists for tasks you need to finish. Set a due date, star important tasks and mark them as complete. Project developed independently.

## Getting started
1. Clone the repository:
```
git clone https://github.com/while-is-alex/task-manager.git
```

2. Change the directory to the project folder.

3. Create a virtual environment:
```
py -m venv venv
venv/Scripts/activate
```

4. Install the required packages:
```
pip install -r requirements.txt
```

5. Finally, to get the website running, run the `main.py` file. The website will launch and display the home screen.

## Features
### Unregistered use
The application supports unregistered users, who are able to fully utilize all of the features of the Task Manager web-app, and are only not able to save their lists (unless they register to the website).

To implement that feature, however, a limitation of the initial version of the web-app had to be overcome, since every list that is created gets registered into the database. That's how the website remembers what tasks belong to which lists (a SQL parent-child relationship). But that created 2 problems: 

1. lists also belong to users, and now there were lists that belonged to no one;

2. these lists were getting registered to the database, but the user wouldn't have access to them ever again unless they registered to the website, so these lists were occupying unnecessary space in the database;

To overcome the first problem, a "save to my lists" button was implemented, so registered users could decide which lists they wanted to keep and which they didn't. And to overcome the second problem, the code was modified to periodically delete lists that didn't belong to an active user.

![home.png](https://i.ibb.co/F33xG2b/home-page.png)

### Password protection
When users register to the website, their e-mail is their unique identifier, and users can feel safe knowing that no one – even behind the scenes – has access to their password, as every password gets hashed and salted with Werkzeug security. So, in case of a leak, user's passwords are encripted with a salt length of 8, guaranteeing that even the most advanced computers won't be able to brute-force crack their password.

![register-page.png](https://i.ibb.co/7yDnmZK/register-page.png)

### Authentication
When accessing the login page, users get feedback whenever their credentials are invalid, as in every try the database is consulted and feedback is flashed to the user. And in case the user tries to register again using an e-mail already registered in the database, they're automatically redirected to the login page, letting them know to log in.

![login-page.png](https://i.ibb.co/7rPhdL2/already-registered.png)

### Automatic reordering
The Task Manager has automatic features behind the scenes to provide efficient functionality. Users can set a due date to their tasks, they can star task to mark them as a priority, they can check tasks as complete (or uncheck them) and delete tasks directly from the Task Manager page. Starred tasks are automatically brought to the top of the list, while complete tasks are brought to the bottom and color-coded to let users intuitivelly infer the relevance of tasks just by looking at their list. And just as a last touch of optimization, complete tasks cannot be starred or get a new due-date.

![automatic-reordering.png](https://i.ibb.co/rFzTd28/automatic-reordering.png)

### List sharing and protection
Users can share a link to their lists with their friends, who are able to see all of the tasks contained in a list, their due-dates, their state of completion and their priority. Lists are protected for modification, so only the user who owns that list is able to modify it, and someone who is accessing the list on view-mode will not be able to change the lists name or add a new task or mark a task as complete or as a priority and, most importantly, won't be able to delete anything as well.

![protected-list.png](https://i.ibb.co/f2hwHyv/protected-list.png)

### Due date alert
When the day when a task is due comes, the label for that date will automatically turn orange in order to call user's attention to that fact.

![due-date.png](https://i.ibb.co/kgRmSDH/due-date.png)

### Easy access to lists
From the Task Manager page, users can easily access all of their lists from a dropdown that will take them to the respective list's page.

![easy-access.png](https://i.ibb.co/WWKHx41/easy-access-to-lists.png)

### User page
Each user can access their saved lists from a user page. On that page, users can also delete saved lists, which will trigger the deletion of the tasks contained on that list from the database as well.

![user-page.png](https://i.ibb.co/6JnQtzw/user-page.png)

## Requirements
This app requires the following:

+ Python 3
+ Flask
+ Flask-Bootstrap
+ Flask-SQLAlchemy
+ Werkzeug
+ python-dotenv
+ shortuuid
