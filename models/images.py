from models import db
from datetime import datetime

class Image(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    uploadedOn = db.Column(db.DateTime(), nullable=False)

    title = db.Column(db.String(255), nullable=False)
    exifData = db.Column(db.Text)
    prize = db.Column(db.String(255), nullable=False)


    # Relationships
    userId = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref('Image', lazy='dynamic'))

    contestId = db.Column(db.Integer, db.ForeignKey('contest.id', ondelete='CASCADE'))
    contest = db.relationship('Contest', backref=db.backref('Image', lazy='dynamic'))


    def __init__(self, title, prize, user, contest, uploadedOn=None, exifData=None):
        self.title = title
        self.prize = prize
        self.user = user
        
        if uploadedOn is None:
            uploadedOn = datetime.utcnow()
        self.uploadedOn = uploadedOn

        self.exifData = exifData
