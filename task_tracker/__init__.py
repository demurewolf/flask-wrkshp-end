import os

from flask import Flask

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'task_tracker.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    """
    As the project got more advance this serves as a reminder of how far we've come.

    # A simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello World!'

    """

    # Added by step 7
    from . import db
    db.init_app(app)

    # Added by step 11
    from . import tasks
    app.register_blueprint(tasks.bp)
    app.add_url_rule('/', endpoint='index')

    return app