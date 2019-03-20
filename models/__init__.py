import os

from flask import Flask


def create_app(test_config=None):
    """Creates and configures the application"""
    
    # Creates a Flask instance
    app = Flask(__name__, instance_relative_config=True)
    
    # Sets app's default configurations
    app.config.from_mapping(
            # Used by Flask and extensions to keep data safe
            SECRET_KEY='dev',
            # DATABASE is the path where the SQLite Database File will be saved
            DATABASE=os.path.join(app.instance_path, 'models.sqlite'),
    )

    # Overrides default configuration with values from config.py or test_config
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Checks that app.instance_path exists. 
    # We will use this path to store SQLite Database File
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import timer
    app.register_blueprint(timer.bp)
    app.add_url_rule('/', endpoint='index')

    return app
