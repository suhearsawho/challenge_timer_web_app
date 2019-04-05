import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from models.db import get_db

# Creates a blueprint called 'auth'
# __name__ indicates where blueprint is defined
# url_prefix will be prepended to all URLs associated with blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Registers a new user and associated password
    Username must not have any special characters and be < 15 characters
    Password must not have any spaces and must be < 30 characters
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        error = verify_username(username)
        if error is None:
            error = verify_password(password)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Verifies user login information
    Error will be displayed if wrong input.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    """Sets up the information of logged in user
    Value stored in g.user will be referenced throughout code
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    """Decorator that is used to check that a user is logged in"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def verify_username(username):
    """Verifies that username has less than 15 characters
    And has no special characters
    """
    if type(username) is not str:
        return 'Username is not a string.'
    if len(username) > 14:
        return 'Username must be less than 15 characters.'

    for char in username:
        num = ord(char)
        if not ((num >= ord('a') and num <= ord('z')) or
                (num >= ord('A') and num <= ord('Z')) or
                (num >= ord('0') and num <= ord('9'))):
            return 'Only characters and numbers allowed in username.'

def verify_password(password):
    """Verifies that the password has less than 30 characters
    And contains no spaces
    """
    if type(password) != str:
        return 'Password is not a string.'
    if len(password) > 30:
        return 'Password must be less than 30 characters.'

    for char in password:
        num = ord(char)
        if num == ord(' '):
            return 'No spaces allowed in password.'
