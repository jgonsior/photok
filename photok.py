import os
import datetime
from datetime import date
from flask import Flask, render_template, request
from flask_user import roles_required, UserManager, UserMixin, SQLAlchemyAdapter
from wtforms.validators import ValidationError
from models import users, db
from wtforms.fields.html5 import DateField
from wtforms import Form, BooleanField, StringField, FileField, TextAreaField, validators

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

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


    dbAdapter = SQLAlchemyAdapter(db, users.User)
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
