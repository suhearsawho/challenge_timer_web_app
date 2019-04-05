from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from models.auth import login_required
from models.db import get_db
from models.db import make_dicts
import json

bp = Blueprint('timer', __name__)

@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    if request.method == 'POST':
        challenge = request.form['challenge']
        time = request.form['time']
        error = None
        # Put Timer data into User Profile

        if not challenge:
            error = 'Challenge is required.'
        elif not time:
            error = 'Time is required.'
        elif all_int(time) is False:
            error = 'Numerical value is required.'
        
        error = verify_challenge(challenge)
        if error is None:
            error = verify_time(time)

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO challenges' 
                ' (task, time_allocated, time_finished, author_id, complete)'
                ' VALUES (?, ?, ?, ?, ?)',
                (challenge, time, time, g.user['id'], 0)
            )
            cursor = db.execute(
                'SELECT last_insert_rowid()',
            )
            task_id = cursor.fetchone()[0]
            cursor.close()
            db.commit()
            return redirect(url_for('timer.challenges', id=g.user['id'], task_id=task_id))
    return render_template('timer/index.html')

#@bp.route('/challenges/', methods=('GET', 'POST'))
@bp.route('/challenges/<int:id>/<int:task_id>/', methods=('GET', 'POST'))
@login_required
def challenges(id, task_id=None):
    # Retrieve task and time associated with task_id
    db = get_db()
    cursor = db.execute(
        'SELECT task, time_allocated'
        ' FROM challenges'
        ' WHERE id = ?'
        ' AND author_id = ?',
        (task_id, id)
    )
    row = cursor.fetchone()
    task = row['task']
    time = row['time_allocated']
    # Response to buttons 
    if request.method == 'POST':
        # request.form returns an immutable dict (Part of Werkzeug)
        button_type = list(request.form.to_dict().keys())[0]
        if button_type == 'finish':
            db.execute(
                'UPDATE challenges'
                ' SET complete = ?'
                ' WHERE id = ?',
                (1, task_id)
            )
            db.commit()
            return redirect(url_for('timer.index'))
    return render_template('timer/challenges.html', task_id=task_id, task=task, time=time)

@bp.route('/history/<int:id>', methods=('GET', 'POST'))
@login_required
def history(id):
    db = get_db()
    if request.method == 'POST':
        button_type = list(request.form.to_dict().keys())[0]
        if button_type == 'delete_all':
            db.execute(
                'DELETE FROM challenges'
            )
            db.commit()
            return redirect(url_for('timer.history', id=g.user['id']))

    cursor = db.execute(
        'SELECT task, time_allocated, time_finished, complete'
        ' FROM challenges'
        ' WHERE author_id = ?',
        (id,)
    )
    rows = cursor.fetchall()

    # Need to return a list of dictionaries with all the entries
    values = []
    for row in rows:
        values.append(make_dicts(cursor, row))
    cursor.close()
    return render_template('timer/history.html', work_history=values)

def all_int(text):
    for char in text:
        if ord(char) < ord('0') or ord(char) > ord('9'):
            return False

@bp.route('/five/<int:id>/<int:task_id>/', methods=('GET', 'POST'))
def five(id, task_id=None):
    db = get_db()

    db.execute(
        'UPDATE challenges'
        ' SET time_finished = time_finished + 5'
        ' WHERE id = ?',
        (task_id, )
    )
    db.commit()
    return 'finish'

@bp.route('/fifteen/<int:id>/<int:task_id>/', methods=('GET', 'POST'))
def fifteen(id, task_id=None):
    db = get_db()

    db.execute(
        'UPDATE challenges'
        ' SET time_finished = time_finished + 15'
        ' WHERE id = ?',
        (task_id, )
    )
    db.commit()
    return 'finish'

def verify_challenge(challenge):
    if len(challenge) > 30:
        return 'Please limit challenge description to 30 or less characters.'

def verify_time(time):
    if int(time) > 200:
        return 'Please limit challenge time to 200 minutes or less for max productivity.'

# Debugging     
@bp.route('/hi/', methods=('GET', 'POST'))
@login_required
def hi():
    print('YOU ARE IN THE HI FUNCTION')
    return 'empty'
