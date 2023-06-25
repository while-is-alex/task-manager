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
The application supports unregistered users, who are able to fully utilize all of the features of the Task Manager web-app, and are only not able to save their lists (unless they register to the website). To implement that feature, however, a limitation of the initial version of the web-app had to be overcome, since every list that is created gets registered into the database. That's how the website remembers what tasks belong to which lists (a SQL parent-child relationship). But that created 2 problems: 1. lists also belong to users, and now there were lists that belong to no one; 2. these lists were getting registered to the database, but the user wouldn't have access to them anymore unless they registered to the website. To overcome the first problem, a "save to my lists" button was implemented, so registered users could decide which lists they wanted to keep and which they didn't. And to overcome the latter, the code was modified to periodically delete lists that didn't belong to an user.

![home.png](https://i.ibb.co/F33xG2b/home-page.png)

### Password protection
When users register to the website, their e-mail is their unique identifier, and users can feel safe knowing that no one – even behind the scenes – has access to their password, as every password gets hashed and salted with Werkzeug security.

![register-page.png](https://i.ibb.co/7yDnmZK/register-page.png)

### Authentication
When accessing the login page, users get feedback whenever their credentials are invalid, as in every try the database is consulted and feedback is flashed to the user. In case the user is trying to register again when they're already registered, the user is redirected to the login page.

![login-page.png](https://i.ibb.co/7rPhdL2/already-registered.png)

## Requirements
This app requires the following:

+ Python 3
+ Flask
+ Flask-Bootstrap
+ Flask-SQLAlchemy
+ Werkzeug
+ python-dotenv
+ shortuuid
