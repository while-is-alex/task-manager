from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import shortuuid
import datetime
from dotenv import load_dotenv
import os

# Application setup
app = Flask(__name__)
app.app_context().push()
load_dotenv()
# app.config['SECRET_KEY'] can be any key, and it will work
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap(app)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task-manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)


# Database tables configuration
class List(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), unique=True, nullable=False)
    user = relationship('User', back_populates='lists')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tasks = relationship('Task', back_populates='parent_list')


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    lists = relationship('List', back_populates='user')
    tasks = relationship('Task', back_populates='user')


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    user = relationship('User', back_populates='tasks')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parent_list = relationship('List', back_populates='tasks')
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))
    due_date = db.Column(db.String(250), nullable=True)
    complete = db.Column(db.Boolean)
    starred = db.Column(db.Boolean)


# Creates the tables if they don't already exist
db.create_all()


@app.route('/')
def home():
    # Every time the home page is called, the code goes through all the lists in the database
    # and erases all lists that haven't been saved (i.e. lists without an user id)
    all_lists = List.query.all()
    for list_ in all_lists:
        if not list_.user_id:
            for task in list_.tasks:
                db.session.delete(task)
            db.session.delete(list_)
            db.session.commit()

    return redirect(url_for('create_list'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please, log in.')
            return redirect(url_for('login'))

        password = request.form['password']

        hashed_and_salted_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        new_user = User(email=email, password=hashed_and_salted_password, name=name.title())
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('my_lists'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Email does not exist in our database.')
            return redirect(url_for('login'))

        elif not check_password_hash(user.password, password):
            flash('Password incorrect.')
            return redirect(url_for('login'))

        else:
            login_user(user)
            return redirect(url_for('my_lists'))

    return render_template('login.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('home'))


@app.route('/my-lists')
@login_required
def my_lists():
    name = current_user.name

    return render_template('my-lists.html', name=name)


@app.route('/new-list')
def create_list():
    url = shortuuid.ShortUUID().random(length=10)
    list_name = 'New List'
    new_list = List(
        list_name=list_name,
        url=url,
    )

    db.session.add(new_list)
    db.session.commit()

    return redirect(url_for('show_list', list_url=url))


@app.route('/save-list/<list_url>')
@login_required
def save_list(list_url):
    current_list = List.query.filter_by(url=list_url).first()
    for task in current_list.tasks:
        task.user_id = current_user.id
    current_list.user_id = current_user.id
    db.session.commit()

    return redirect(url_for('show_list', list_url=current_list.url))


@app.route('/list/<list_url>')
def show_list(list_url):
    current_list = List.query.filter_by(url=list_url).first()

    # Passes today's date so the due date can change color when the due date comes
    now = datetime.date.today()
    unformatted_today = now.strftime("%d/%m/%Y")
    today = unformatted_today.replace('/', '-')

    return render_template('edit-list.html', list=current_list, today=today)


@app.route('/update/<list_url>', methods=['POST'])
def update_list(list_url):
    list_to_be_updated = List.query.filter_by(url=list_url).first()
    list_name = request.form['listname']
    list_to_be_updated.list_name = list_name
    db.session.commit()

    return redirect(url_for('show_list', list_url=list_to_be_updated.url))


@app.route('/delete/<list_id>')
@login_required
def delete_list(list_id):
    list_to_be_deleted = List.query.filter_by(id=list_id).first()
    # Deletes all the tasks related to the list being deleted
    for task in list_to_be_deleted.tasks:
        db.session.delete(task)
    db.session.delete(list_to_be_deleted)
    db.session.commit()

    return redirect(url_for('my_lists'))


@app.route('/add-task/<list_id>', methods=['POST'])
def new_task(list_id):
    if current_user.is_authenticated:
        current_task = Task(
            task=request.form['task'],
            user_id=current_user.id,
            list_id=list_id,
            complete=False,
            starred=False,
        )
        db.session.add(current_task)
        db.session.commit()
    else:
        current_task = Task(
            task=request.form['task'],
            list_id=list_id,
            complete=False,
            starred=False,
        )
        db.session.add(current_task)
        db.session.commit()

    current_list = List.query.filter_by(id=list_id).first()

    return redirect(url_for('show_list', list_url=current_list.url))


@app.route('/date/<task_id>', methods=['POST'])
def due_date(task_id):
    print(request.form)
    task_to_be_updated = Task.query.filter_by(id=task_id).first()
    current_list = List.query.filter_by(id=task_to_be_updated.list_id).first()

    if request.form['due_date']:
        new_due_date = request.form['due_date']
        date_split = new_due_date.split('-')
        formatted_due_date = f'{date_split[2]}-{date_split[1]}-{date_split[0]}'

    task_to_be_updated.due_date = formatted_due_date
    db.session.commit()

    return redirect(url_for('show_list', list_url=current_list.url))


@app.route('/complete/<task_id>')
def complete_task(task_id):
    task_to_be_updated = Task.query.filter_by(id=task_id).first()
    current_list = List.query.filter_by(id=task_to_be_updated.list_id).first()
    if task_to_be_updated.complete:
        task_to_be_updated.complete = False
    else:
        task_to_be_updated.complete = True
    db.session.commit()

    return redirect(url_for('show_list', list_url=current_list.url))


@app.route('/star/<task_id>')
def star_task(task_id):
    task_to_be_updated = Task.query.filter_by(id=task_id).first()
    current_list = List.query.filter_by(id=task_to_be_updated.list_id).first()
    if task_to_be_updated.starred:
        task_to_be_updated.starred = False
    else:
        task_to_be_updated.starred = True
    db.session.commit()

    return redirect(url_for('show_list', list_url=current_list.url))


@app.route('/delete-task/<task_id>')
def delete_task(task_id):
    task_to_be_deleted = Task.query.filter_by(id=task_id).first()
    current_list = List.query.filter_by(id=task_to_be_deleted.list_id).first()
    db.session.delete(task_to_be_deleted)
    db.session.commit()
    return redirect(url_for('show_list', list_url=current_list.url))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
