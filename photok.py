import os
from datetime import date
import random
from flask import Flask, render_template, request, send_file, make_response, redirect, url_for
from flask_user import roles_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask_restful import reqparse, Resource, Api
from wtforms.validators import ValidationError
from wtforms.fields.html5 import DateField
from wtforms import Form, BooleanField, StringField, FileField, TextAreaField, validators
from models import db
from models.contest import Contest, ContestApi, ContestListPublicApi, ContestListPrivateApi
from models.vote import Vote, VoteApi, VoteListApi
from models.image import Image, ImageApi, ImageListApi
from models.user import User, Role
from datetime import datetime, timedelta, date
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_object('config.Config')
app.config['UPLOAD_FOLDER'] = "./static/images"
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


    dbAdapter = SQLAlchemyAdapter(db, User)

    userManager = UserManager(dbAdapter, app, password_validator=passwordValidator, )

    # create some fake data for developing
    # Create a test user/admin
    if not User.query.filter(User.username == 'test').first():
        user1 = User(username='test', email='test@example.com', active=True,
                     password=userManager.hash_password('test'))
        user1.roles.append(Role(name='admin'))
        user1.roles.append(Role(name='user'))
        db.session.add(user1)

        argCon1 = {
            "headline": "Saint Saturnin les Avignon's most beautiful spring flower",
            "theme": "flower",
            "workingTitle": "spring contest 2016",
            "description": "This contest takes place in France, the most beautiful country there is",
            "startDate": datetime.utcnow() - timedelta(days=30),
            "endDate": datetime.utcnow() - timedelta(days=20),
            "voteMethod": "simple"
        }

        argCon2 = {
            "headline": "Klotzsche's most beautiful pint of beer",
            "theme": "beer",
            "workingTitle": "summer contest 2016",
            "description": "Beer is the world's most widely consumed and probably the oldest alcoholic beverage; it is the third most popular drink overall, after water and tea. The production of beer is called brewing, which involves the fermentation of starches, mainly derived from cereal grains most commonly malted barley, although wheat, maize (corn), and rice are widely used.",
            "startDate": datetime.utcnow() - timedelta(days=20),
            "endDate": datetime.utcnow() - timedelta(days=10),
            "voteMethod": "simple"
        }

        argCon3 = {
            "headline": "Roelofarendsveen's most beautiful winter flower",
            "workingTitle": "winter contest 2016",
            "theme": "flower",
            "description": "If you manage to say the name of this city, you win",
            "startDate": datetime.utcnow() - timedelta(days=10),
            "endDate": datetime.utcnow() + timedelta(days=10),
            "voteMethod": "simple"
        }

        contest1 = Contest(argCon1)
        contest2 = Contest(argCon2)
        contest3 = Contest(argCon3)

        db.session.add(contest1)
        db.session.add(contest2)
        db.session.add(contest3)

        image1 = Image({'uploadedOn': None, 'title': "Tulip", 'path': "static/images/T.jpg", 'prize': 0, 'userId': 1,
                        'contestId': 1})
        image2 = Image(
                {'uploadedOn': None, 'title': "Sunflower", 'path': "static/images/S.jpg", 'prize': 0, 'userId': 1,
                 'contestId': 1})
        image3 = Image({'uploadedOn': None, 'title': "Onion", 'path': "static/images/O.jpg", 'prize': 0, 'userId': 1,
                        'contestId': 1})
        image4 = Image(
                {'uploadedOn': None, 'title': "The Mighty Pint", 'path': "static/images/B.jpg", 'prize': 0, 'userId': 1,
                 'contestId': 2})
        db.session.add(image1)
        db.session.add(image2)
        db.session.add(image3)
        db.session.add(image4)

        # Third contest has lots of pictures now
        words = ["Power", "Flower", "Art", "Photo", "Best"]
        path = ["T", "S", "O", "B"]
        for i in range(0, 15):
            image = Image({'uploadedOn': None, 'title': words[random.randint(0, 4)] + " " + words[random.randint(0, 4)],
                           'path': "static/images/" + path[random.randint(0, 3)] + ".jpg", 'prize': 0, 'userId': 1,
                           'contestId': 3})
            db.session.add(image)

        # Give points to images
        # TODO: not needed right now
        """
        vote1 = Vote("50", image1, contest1)
        vote2 = Vote("20", image2, contest1)
        vote3 = Vote("10", image3, contest1)
        db.session.add(vote1)
        db.session.add(vote2)
        db.session.add(vote3)
        """

        db.session.commit()

    # define REST api entry points
    api.add_resource(ContestApi, '/api/contests/<contestId>')
    api.add_resource(ContestListPublicApi, '/api/contestsPublic')
    api.add_resource(ContestListPrivateApi, '/api/contestsPrivate')

    api.add_resource(ImageApi, '/api/images/<imageId>')
    api.add_resource(ImageListApi, '/api/images/contest/<contestId>')

    api.add_resource(VoteApi, '/api/votes/<voteId>')
    api.add_resource(VoteListApi, '/api/votes')


# some help functions to make the authentication with jwt working
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and userManager.verify_password(password, user):
        print("hui")
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)


jwt = JWT(app, authenticate, identity)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# TODO: maybe move this? does it belong here?
@app.route('/api/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        name = request.form["name"]  # get name from post
        # check if the post request has the file part
        if 'file' not in request.files:
            return "-1"
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return "-2"
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
            return "0"
    return "-3"


@app.route('/')
@app.route('/admin')
@app.route('/add')
@app.route('/edit/<contestId>')
@app.route('/vote/<contestId>')
@app.route('/login')
@app.route('/logout')
@app.route('/error-404')
def basic_pages(**kwargs):
    return render_template('main.html')


@app.route('/submit', methods=['GET', 'POST'])
def register():
    form = CreateContestForm(request.form)
    if request.method == 'POST' and form.validate():
        return 'success'
    return render_template('pages/create_contest.html', active="create_contest", form=form)


@app.route('/contests')
@app.route('/contests/<contestId>')
def contests(contestId=''):
    return render_template('main.html', contestId=contestId)


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
