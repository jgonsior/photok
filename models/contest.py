from models import db
from datetime import datetime
from flask_restful import reqparse, Resource
from sqlalchemy.orm import class_mapper
import sqlalchemy


class Contest(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    headline = db.Column(db.String(255), nullable=False)
    workingTitle = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
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
        # save only the changed attributes
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
        contests = []
        for c in Contest.query.all():
            contest = prepare_dict_for_json(c.__dict__)
            contests.append(contest)
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
