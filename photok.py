import os
from flask import Flask, render_template, request
from flask_user import roles_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask_restful import reqparse, Resource, Api
from pprint import pprint
import json
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
api = Api(app)


with app.app_context():
    # Create all database tables
    db.create_all()

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


        contest1 = Contest("Link\ouml;pings most beautifull spring flower", "spring contest 2016", datetime.utcnow() + timedelta(days=10), datetime.utcnow() + timedelta(days=20), "simple")
        contest2 = Contest("Link\ouml;pings most beautifull autumn flower",
                "summer contest 2016", datetime.utcnow() + timedelta(days=10), datetime.utcnow() + timedelta(days=20), "simple")
        contest3 = Contest("Link\ouml;pings most beautifull winter flower",
                "winter contest 2016", datetime.utcnow() + timedelta(days=10), datetime.utcnow() + timedelta(days=20), "simple")

        db.session.add(contest1)
        db.session.add(contest2)
        db.session.add(contest3)
 
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


    # 1. get contests from database
    # 2. define all reqired arguments
    # 3. create new contest
    # 4. save contest to database :)

    def serialize(model):
        columns = [c.key for c in class_mapper(model.__class__).columns]
        return dict((c, getattr(model,c)) for c in columns)
    
    contests = {}
    for c in Contest.query.all(): 
        contest = c.__dict__
        del(contest['_sa_instance_state'])
        for key, value in contest.iteritems():
            if isinstance(value, datetime):
                contest[key] = str(value)
        contests[contest['id']] = contest


    pprint(contests)


    parser = reqparse.RequestParser()
    parser.add_argument('title')

    class ContestApi(Resource):
        def get(self, contest_id):
            return contests[contest_id]

        def delete(self, contest_id):
            del contests[contest_id]
            return '', 204

        def put(self, contest_id):
            args = parser.parse_args()
            contest = {'title': args['title']}
            contests[contest_id] = contest
            return contest, 201

    class ContestListApi(Resource):
        def get(self):
            return contests

        def post(self):
            args = parser.parse_args()

            # getting the id of the next contest -> database!
            contest_id = int(max(contests.keys()).lstrip('title')) +1
            contest_id = 'title%i' % todo_id
            contests[contest_id] = {'title': args['title']}
            return contests[contest_id], 201


    api.add_resource(ContestApi, '/api/contests/<contest_id>')
    api.add_resource(ContestListApi, '/api/contests')



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
