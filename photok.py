import os
from flask import Flask, render_template
from flask_user import roles_required, UserManager, UserMixin, SQLAlchemyAdapter
from wtforms.validators import ValidationError
from models import users, images, db

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
    if not users.User.query.filter(users.User.username=='test').first():
        user1 = users.User(username='test', email='test@example.com', active=True,
                password=userManager.hash_password('test'))
        user1.roles.append(users.Role(name='admin'))
        user1.roles.append(users.Role(name='user'))
        db.session.add(user1)
        db.session.commit()



@app.route('/')
def homepage():
    return render_template('pages/homepage.html',active="home")

@app.route('/link')
@roles_required('admin')
def link():
    return render_template('pages/page.html',active="page")

if __name__ == '__main__':
    app.run()
