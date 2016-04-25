from models import db
from datetime import datetime

class Contest(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    headline = db.Column(db.String(255), nullable=False)
    workingTitle = db.Column(db.String(255), nullable=False)
    createdDate = db.Column(db.DateTime(), nullable=False)
    startDate = db.Column(db.DateTime(), nullable=False)
    endDate = db.Column(db.DateTime(), nullable=False)
    voteMethod = db.Column(db.String(255), nullable=False)


    def __init__(self, headline, workingTitle, createdDate, startDate, endDate, voteMethod):
        self.headline = headline
        self.workingTitle = workingTitle
        
        if createdDate is None:
            createdDate = datetime.utcnow()

        self.createdDate = createdDate
        self.startDate = startDate
        self.endDate = endDate
        self.voteMethod = voteMethod
