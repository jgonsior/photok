import os
from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, UserMixin, SQLAlchemyAdapter, roles_required
from wtforms.validators import ValidationError
import config

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)


# some models -> need to be transfered to a different file later one :)
# Define the Role DataModel
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the User data model. Make sure to add flask.ext.user UserMixin !!!
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))


    # User authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

    # User email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')



# Define the UserRoles DataModel
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

def passwordValidator(form, field):
    password = field.data
    if app.config['DEBUG'] == True:
        limit = 3
    else:
        limit = 8
    if len(password) < limit:
        raise ValidationError(_('Password must have at least 3 characters'))

# Create all database tables
db.create_all()

dbAdapter =  SQLAlchemyAdapter(db, User) 
userManager = UserManager(dbAdapter, app, password_validator=passwordValidator,)


# Create a test user
if app.config['DEBUG'] == True:
    if not User.query.filter(User.username=='test').first():
        user1 = User(username='test', email='test@example.com', active=True,
                password=userManager.hash_password('test'))
        user1.roles.append(Role(name='admin'))
        user1.roles.append(Role(name='user'))
        db.session.add(user1)
        db.session.commit()




@app.route('/')
def hello_world():
    return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Home page</h2>
                <p>This page can be accessed by anyone.</p><br/>
                <p><a href={{ url_for('hello_world') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('secret') }}>Members page</a> (login required)</p>
            {% endblock %}
            """)

@app.route('/secret')
@roles_required('admin')
def secret():
    return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Members page</h2>
                <p>This page can only be accessed by authenticated users.</p><br/>
                <p><a href={{ url_for('hello_world') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('secret') }}>Members page</a> (login required)</p>
            {% endblock %}
            """)

if __name__ == '__main__':
    app.run()
