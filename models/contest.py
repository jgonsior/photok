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


    def __init__(self, args):
        self.createdDate =  datetime.utcnow()
        for k,v in args.iteritems():
           # if k == "createdDate" and v is None:
           #     v = datetime.utcnow()
            setattr(self, k, v)
