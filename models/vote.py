from models import db
from datetime import datetime
from flask_restful import reqparse, Resource
from sqlalchemy.orm import class_mapper
from flask_jwt import jwt_required

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


# converts f.e. datetime objects to strings
def prepare_dict_for_json(d):
    del(d['_sa_instance_state'])
    for k, v in d.iteritems():
        if isinstance(v, datetime):
            d[k] = str(v)
    return d

""" Why ?
parser = reqparse.RequestParser()
# accept in a magical way all properties of our model :)
for prop in class_mapper(Vote).iterate_properties:
    if isinstance(prop, sqlalchemy.orm.ColumnProperty):
        parser.add_argument(str(prop).replace("Vote.", ""))
"""


class VoteApi(Resource):
    decorators = [jwt_required()]
    def get(self, voteId):
        return prepare_dict_for_json(Vote.query.get(voteId).__dict__)

    def delete(self, voteId):
        vote = Vote.query.get(voteId)
        db.session.delete(vote)
        db.session.commit()
        return '', 204

    # put -> update existing vote
    def put(self, voteId):
        # deserialize json :)
        args = parser.parse_args()
        # save only the changed attributes
        for k, v in args.iteritems():
            if v is not None:
                # parse datetime back
                if isinstance(Vote.__table__.c[k].type,
                        sqlalchemy.sql.sqltypes.DateTime):
                    v = datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
                db.session.query(Vote).filter_by(id=voteId).update({k: v})
        db.session.commit()
        return 201


class VoteListApi(Resource):
    decorators = [jwt_required()]
    def get(self):
        votes = {}
        for c in Vote.query.all():
            vote = prepare_dict_for_json(c.__dict__)
            votes[vote['id']] = vote
        return votes

    # post -> add new vote
    def post(self):
        args = parser.parse_args()
        for k, v in args.iteritems():
            if isinstance(Vote.__table__.c[k].type,
                    sqlalchemy.sql.sqltypes.DateTime):
                args[k] = datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
        vote = Vote(args)
        db.session.add(vote)
        db.session.commit()
        return 201
