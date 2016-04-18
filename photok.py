import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

app = Flask(__name__)
app.config.from_pyfile('flask.cfg')

# some configs depending on if we're running the code locally or remotely
if 'OPENSHIFT_POSTGRESQL_DB_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] =os.environ['OPENSHIFT_MYSQL_DB_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///testdb.db"
    app.config['DEBUG'] = True

db = SQLAlchemy(app)


# Define the User data model. Make sure to add flask.ext.user UserMixin !!!
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    # User authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    
    # User email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())
    
    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

# Create all database tables
db.create_all()


db_adapter =  SQLAlchemyAdapter(db, User)    
userManager = UserManager(db_adapter, app)


@app.route('/')
def hello_world():
    return 'Hello <a href="laurent">Laurent</a>, Sijmen and Julius!'

@app.route('/laurent')
def laurent_fun():
    return 'Hello Laurent only!'

@app.route('/sijmen')
def sijmen_fun():
    return 'Hello Laurent, Sijmen and Julius!'

@app.route('/julius')
def julius_fun():
    return 'Hello <b>Julius</b>!'


if __name__ == '__main__':
    app.run()
