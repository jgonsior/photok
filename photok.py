import os
from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from wtforms.validators import ValidationError

app = Flask(__name__)
app.config.from_pyfile('flask.cfg')

# some configs depending on if we're running the code locally or remotely
if 'OPENSHIFT_POSTGRESQL_DB_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] =os.environ['OPENSHIFT_MYSQL_DB_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///testdb.db"
    app.config['DEBUG'] = True
    app.config['CSRF_ENABLED'] = False

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
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')



# Define the UserRoles DataModel
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

# should be used only for development mode
def stupid_non_productive_password_validator(form, field):
    password = field.data
    if len(password) < 3:
        raise ValidationError(_('Password must have at least 3 characters'))

# Create all database tables
db.create_all()


db_adapter =  SQLAlchemyAdapter(db, User) 
userManager = UserManager(db_adapter, app, password_validator=stupid_non_productive_password_validator,)


@app.route('/')
def hello_world():
    return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Home page</h2>
                <p>This page can be accessed by anyone.</p><br/>
                <p><a href={{ url_for('hello_world') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('julius') }}>Members page</a> (login required)</p>
            {% endblock %}
            """)

@app.route('/julius')
@login_required
def julius():
    return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Members page</h2>
                <p>This page can only be accessed by authenticated users.</p><br/>
                <p><a href={{ url_for('hello_world') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('julius') }}>Members page</a> (login required)</p>
            {% endblock %}
            """)

if __name__ == '__main__':
    app.run()
