from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from models.auth import login_required
from models.db import get_db

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

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO challenges (task, time_allocated, author_id, complete)'
                ' VALUES (?, ?, ?, ?)',
                (challenge, time, g.user['id'], 0)
            )
            
            db.commit()
            return redirect(url_for('timer.challenges', task=challenge, time=time))
    return render_template('timer/index.html')

@bp.route('/challenges/', methods=('GET', 'POST'))
@bp.route('/challenges/<task>/<time>', methods=('GET', 'POST'))
@login_required
def challenges(task=None, time=25):
    if request.method == 'POST':
        return redirect(url_for('timer.index'));
    # TODO redirect to index when timer is complete
    return render_template('timer/challenges.html', task=task, time=time)


def all_int(text):
    for char in text:
        if ord(char) < ord('0') or ord(char) > ord('9'):
            return False
