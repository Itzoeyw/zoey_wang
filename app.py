from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================
# APP CONFIGURATION
# ============================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-super-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ============================================
# DATABASE MODELS (This is your SQL!)
# ============================================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Create all database tables
with app.app_context():
    db.create_all()


# ============================================
# HELPER — Check if user is logged in
# ============================================
def is_logged_in():
    return 'user_id' in session


# ============================================
# ROUTES — Pages and Actions
# ============================================

# HOME PAGE — Shows all tasks for logged-in user
@app.route('/')
def index():
    if not is_logged_in():
        return redirect(url_for('login'))

    todos = Todo.query.filter_by(user_id=session['user_id']).order_by(Todo.date_created.desc()).all()

    # Count tasks for stats
    total_tasks = len(todos)
    completed_tasks = len([t for t in todos if t.completed])
    pending_tasks = total_tasks - completed_tasks

    return render_template('index.html',
                           todos=todos,
                           total_tasks=total_tasks,
                           completed_tasks=completed_tasks,
                           pending_tasks=pending_tasks)


# ADD TASK
@app.route('/add', methods=['POST'])
def add():
    if not is_logged_in():
        return redirect(url_for('login'))

    content = request.form.get('content')
    if content and content.strip():
        new_task = Todo(content=content.strip(), user_id=session['user_id'])
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
    else:
        flash('Task cannot be empty!', 'danger')

    return redirect(url_for('index'))


# MARK TASK COMPLETE / INCOMPLETE
@app.route('/complete/<int:todo_id>')
def complete(todo_id):
    if not is_logged_in():
        return redirect(url_for('login'))

    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == session['user_id']:
        todo.completed = not todo.completed
        db.session.commit()
        if todo.completed:
            flash('Task completed! Great job! 🎉', 'success')
        else:
            flash('Task marked as pending.', 'info')

    return redirect(url_for('index'))


# DELETE TASK
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    if not is_logged_in():
        return redirect(url_for('login'))

    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == session['user_id']:
        db.session.delete(todo)
        db.session.commit()
        flash('Task deleted!', 'success')

    return redirect(url_for('index'))


# REGISTER — Create new account
@app.route('/register', methods=['GET', 'POST'])
def register():
    if is_logged_in():
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Validation
        if not username or not password:
            flash('Please fill in all fields!', 'danger')
            return redirect(url_for('register'))

        if len(username) < 3:
            flash('Username must be at least 3 characters!', 'danger')
            return redirect(url_for('register'))

        if len(password) < 4:
            flash('Password must be at least 4 characters!', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken! Try another one.', 'danger')
            return redirect(url_for('register'))

        # Create new user
        new_user = User(
            username=username,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}! 👋', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')


# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out. See you soon! 👋', 'info')
    return redirect(url_for('login'))


# ============================================
# RUN THE APP
# ============================================
if __name__ == '__main__':
    app.run(debug=True)