import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """Creates a connection to SQLite Database"""

    # g is an object used to store data during a connection.
    # g is unique for EVERY request
    if 'db' not in g:
        # Creates connection to file pointed at by DATABASE configuration key
        g.db = sqlite3.connect(
            # Recall, we defined DATABASE in __init__.py
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Closes connection to database if exists"""
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# Defines a command line command called init-db that calls init_db function
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    # Tells Flask to call this function when cleaning up before returning response
    app.teardown_appcontext(close_db)
    # Adds a new command that can be called with flask command
    app.cli.add_command(init_db_command)

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
