import os
#import datetime
from datetime import date
from flask import Flask, render_template, request
from flask_user import roles_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask_restful import reqparse, Resource, Api
from wtforms.validators import ValidationError
from wtforms.fields.html5 import DateField
from wtforms import Form, BooleanField, StringField, FileField, TextAreaField, validators
from models import db
from models.contest import Contest, ContestApi, ContestListApi
from models.vote import Vote
from models.image import Image, ImageApi, ImageListApi
from models.user import User, Role
from datetime import datetime, timedelta, date

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

    # define REST api entry points
    api.add_resource(ContestApi, '/api/contests/<contestId>')
    api.add_resource(ImageApi, '/api/images/<imageId>')
    api.add_resource(ContestListApi, '/api/contests')
    api.add_resource(ImageListApi, '/api/images')



@app.route('/')
def homepage():
    return render_template('pages/homepage.html',active="home")


@app.route('/browse')
def browse_contests():
    return render_template('pages/browse.html',active="browse")


@app.route('/contest')  # /<contestName>') TODO, load actual contest
def view_contest():  # contestName): TODO, load actual contest
    return render_template('pages/show_contest.html',active="")


@app.route('/add')
def create_contest():
    return render_template('pages/create_contest.html', active="create_contest", form=CreateContestForm())


@app.route('/submit', methods=['GET', 'POST'])
def register():
    form = CreateContestForm(request.form)
    if request.method == 'POST' and form.validate():
        return 'success'
    return render_template('pages/create_contest.html', active="create_contest", form=form)


@app.route('/link')
@roles_required('admin')
def link():
    return render_template('pages/page.html',active="page")


class CreateContestForm(Form):
    headline = StringField('Headline', [validators.Length(min=4, max=25)])
    thumbnail = FileField('Thumbnail')
    theme = StringField('Theme', [validators.Length(min=4, max=25)])
    workingTitle = StringField('Working title', [validators.Length(min=4, max=25)])
    description = TextAreaField('description', [validators.Length(min=0, max=300)])
    startDate = DateField('Start date', default=date.today)
    endDate = DateField('End date')
    onlyJuryVote = BooleanField('Only a jury can vote')


if __name__ == '__main__':
    app.run()
