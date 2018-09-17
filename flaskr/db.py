# Define and Access the Database
# SQLite is convenient because it does not require setting up a separate database server and is built-in to Python
# 我们使用SQLite 在我们这个数据库的原因非常的简单. 因为并SQLite不需要set up a server. It can store the data locally.
# The first thing to do when working with a SQLite database is to create a connection to it. w
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
# 首先，我们应该如何来理解g ?
# g is a special object that is unique for each request. It is used to store data that might be accessed by multiple functions during the request.
# 就是这个g 可以储存的数据，这个数据会被多个function access
# The connection is stored and reused instead of creating a new connection if get_db is called a 2nd time in the same request.
# 然后，如何理解current_app?
# A proxy to the application handling the current request. This is useful to access the application without needing to import it, or if it can’t be imported, such as when using the application factory pattern or in blueprints and extensions.
# 简单的来说，就是application的建立已经被set up. 所以我们就只能够用 current)app to handle the current request
# sqlite3.connect() establishes a connection to the file pointed at by the DATABASE configuration key. 在这个地方我们define一个和database之间的关系
# sqlite3.Row tells the connection to return rows that behave like dicts. 就是我们获得的数据的row
# close_db checks if a connection was created by checking if g.db was set. 这个会被叫each time after the request.

"""  SQLite will not be used to compete with the client server database such as mongoDB, sqlalchemy which will involves with a lot of users. Rather SQLite is very useful for persional applicaiton and sotre the local data"""

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db) # tells flask to call that function when cleaning up after returning the response
    app.cli.add_command(init_db_command) # adds a new command that can be called with the flask command.










