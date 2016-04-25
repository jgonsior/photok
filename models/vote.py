from models import db
from datetime import datetime

class Vote(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    vote = db.Column(db.Integer, nullable=False)

    # Relationships
    imageId = db.Column(db.Integer, db.ForeignKey('image.id', ondelete='CASCADE'))
    image = db.relationship('Image', backref=db.backref('Votes', lazy='dynamic'))

    contestId = db.Column(db.Integer, db.ForeignKey('contest.id', ondelete='CASCADE'))
    contest = db.relationship('Contest', backref=db.backref('Votes', lazy='dynamic'))


    def __init__(self, vote, image, contest):
        self.vote = vote
        self.image = image
        self.contest = contest
