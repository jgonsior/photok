import os
from flask import Flask, render_template
from flask_user import roles_required, UserManager, UserMixin, SQLAlchemyAdapter
from wtforms.validators import ValidationError
from models import db
from models.contest import Contest
from models.vote import Vote
from models.image import Image
from models.user import User, Role
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

with app.app_context():
    # Create all database tables
    db.create_all()

    contest1 = Contest("Link\ouml;pings most beautifull spring flower", "spring contest 2016", datetime.utcnow() + timedelta(days=10), datetime.utcnow() + timedelta(days=20), "simple")
    
    def passwordValidator(form, field):
        password = field.data
        if app.config['DEBUG']:
            limit = 3
        else:
            limit = 8
        if len(password) < limit:
            raise ValidationError('Password must have at least 3 characters')


    dbAdapter =  SQLAlchemyAdapter(db, User) 
    userManager = UserManager(dbAdapter, app, password_validator=passwordValidator,)

    # create some fake data for deveoloping
    # Create a test user/admin
    if not User.query.filter(User.username=='test').first():
        user1 = User(username='test', email='test@example.com', active=True,
                password=userManager.hash_password('test'))
        user1.roles.append(Role(name='admin'))
        user1.roles.append(Role(name='user'))
        db.session.add(user1)
        db.session.add(contest1)

        image1 = Image("Tulip", "Gold", user1, contest1)
        image2 = Image("Sunflower", "Silver", user1, contest1)
        image3 = Image("Onion", "Bronze", user1, contest1)
        db.session.add(image1)
        db.session.add(image2)
        db.session.add(image3)

        # fifty points to griffyndor
        vote1 = Vote("50", image1, contest1)
        vote2 = Vote("20", image2, contest1)
        vote3 = Vote("10", image3, contest1)
        db.session.add(vote1)
        db.session.add(vote2)
        db.session.add(vote3)
        db.session.commit()


@app.route('/')
def homepage():
    return render_template('pages/homepage.html',active="home")


@app.route('/browse')
def browse_contests():
    return render_template('pages/browse.html',active="browse")


@app.route('/contest') # /<contestName>') TODO, load actual contest
def view_contest(): # contestName): TODO, load actual contest
    return render_template('pages/contest.html',active="")


@app.route('/link')
@roles_required('admin')
def link():
    return render_template('pages/page.html',active="page")

if __name__ == '__main__':
    app.run()
