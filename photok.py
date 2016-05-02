import os
from flask import Flask, render_template, request
from flask_user import roles_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask_restful import reqparse, Resource, Api
from sqlalchemy.orm import  class_mapper
from pprint import pprint
import json
import sqlalchemy
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

# the next line is important so that flask-sqlalchemy knows  on which database
# it should perate on
with app.app_context():
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

        argCon1 = {
                "headline": "Link\ouml;pings most beautifull spring flower", 
                "workingTitle": "spring contest 2016",
                "startDate": datetime.utcnow() + timedelta(days=10),
                "endDate": datetime.utcnow() + timedelta(days=20),
                "voteMethod": "simple"
                }

        argCon2 = {
                "headline": "Link\ouml;pings most beautifull autumn flower",
                "workingTitle": "summer contest 2016",
                "startDate": datetime.utcnow() + timedelta(days=10),
                "endDate": datetime.utcnow() + timedelta(days=20),
                "voteMethod": "simple"
                }

        argCon3 = {
                "headline": "Link\ouml;pings most beautifull winter flower",
                "workingTitle": "winter contest 2016",
                "startDate": datetime.utcnow() + timedelta(days=10),
                "endDate": datetime.utcnow() + timedelta(days=20),
                "voteMethod": "simple"
                }

        contest1 = Contest(argCon1)
        contest2 = Contest(argCon2)
        contest3 = Contest(argCon3)

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

    # converts f.e. datetime objects to strings
    def prepare_dict_for_json(d):
        del(d['_sa_instance_state'])
        for k,v in d.iteritems():
            if isinstance(v, datetime):
                d[k] = str(v)
        return d


    parser = reqparse.RequestParser()
    # accept in a magical way all properties of our model :)
    for prop in class_mapper(Contest).iterate_properties:
        if isinstance(prop, sqlalchemy.orm.ColumnProperty):
            parser.add_argument(str(prop).replace("Contest.", ""))


    class ContestApi(Resource):
        def get(self, contestId):
            return prepare_dict_for_json(Contest.query.get(contestId).__dict__)

        def delete(self, contestId):
            contest = Contest.query.get(contestId)
            db.session.delete(contest)
            db.session.commit()
            return '', 204


        # put -> update existing contest
        def put(self, contestId):
            # deserialize json :)
            args = parser.parse_args()
            #save only the changed attributes
            for k, v in args.iteritems():
                if v is not None:
                    # parse datetime back
                    if isinstance(Contest.__table__.c[k].type,
                            sqlalchemy.sql.sqltypes.DateTime):
                        v = datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
                    db.session.query(Contest).filter_by(id=contestId).update({k:v})
            db.session.commit()
            return 201

    class ContestListApi(Resource):
        def get(self):
            contests = {}
            for c in Contest.query.all():
                contest = prepare_dict_for_json(c.__dict__)
                contests[contest['id']] = contest
            return contests

        # post -> add new contest
        def post(self):
            args = parser.parse_args()
            for k,v in args.iteritems():
                if isinstance(Contest.__table__.c[k].type,
                        sqlalchemy.sql.sqltypes.DateTime):
                    args[k] = datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
            contest =  Contest(args)
            db.session.add(contest)
            db.session.commit()
            return 201


    api.add_resource(ContestApi, '/api/contests/<contestId>')
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
