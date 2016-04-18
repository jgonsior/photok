import os
from flask import Flask, render_template_string
from flask_user import roles_required, UserManager, UserMixin, SQLAlchemyAdapter
from wtforms.validators import ValidationError
from models import users, db

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

with app.app_context():
    # Create all database tables
    db.create_all()


    def passwordValidator(form, field):
        password = field.data
        if app.config['DEBUG'] == True:
            limit = 3
        else:
            limit = 8
        if len(password) < limit:
            raise ValidationError(('Password must have at least 3 characters'))


    dbAdapter =  SQLAlchemyAdapter(db, users.User) 
    userManager = UserManager(dbAdapter, app, password_validator=passwordValidator,)

    # Create a test user
    if app.config['DEBUG'] == True:
        if not users.User.query.filter(users.User.username=='test').first():
            user1 = users.User(username='test', email='test@example.com', active=True,
                    password=userManager.hash_password('test'))
            user1.roles.append(users.Role(name='admin'))
            user1.roles.append(users.Role(name='user'))
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
