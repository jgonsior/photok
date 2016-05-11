from models import db
from datetime import datetime
from flask_restful import reqparse, Resource
from sqlalchemy.orm import class_mapper
import sqlalchemy
from models.user import User



class Image(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    uploadedOn = db.Column(db.DateTime(), nullable=False)

    title = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    exifData = db.Column(db.Text)
    prize = db.Column(db.String(255), nullable=False)

    # Relationships
    userId = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref('Image', lazy='dynamic'))

    contestId = db.Column(db.Integer, db.ForeignKey('contest.id', ondelete='CASCADE'))
    contest = db.relationship('Contest', backref=db.backref('Image', lazy='dynamic'))


    def __init__(self, args):
        self.createdDate =  datetime.utcnow()
        for k,v in args.iteritems():
           if k == "uploadedOn" and v is None:
               v = datetime.utcnow()
           setattr(self, k, v)


# converts f.e. datetime objects to strings
def prepare_dict_for_json(d):
    del(d['_sa_instance_state'])
    for k,v in d.iteritems():
        if isinstance(v, datetime):
            d[k] = str(v)
    return d


parser = reqparse.RequestParser()
# accept in a magical way all properties of our model :)
for prop in class_mapper(Image).iterate_properties:
    if isinstance(prop, sqlalchemy.orm.ColumnProperty):
        parser.add_argument(str(prop).replace("Image.", ""))


class ImageApi(Resource):
    def get(self, imageId):
        return prepare_dict_for_json(Image.query.get(imageId).__dict__)

    def delete(self, imageId):
        image = Image.query.get(imageId)
        db.session.delete(image)
        db.session.commit()
        return '', 204

    # update an image
    def put(self, imageId):
        # deserialize json :)
        args = parser.parse_args()
        # save only the changed attributes
        for k, v in args.iteritems():
            if v is not None:
                # parse datetime back
                if isinstance(Image.__table__.c[k].type,
                        sqlalchemy.sql.sqltypes.DateTime):
                    v = datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
                db.session.query(Image).filter_by(id=imageId).update({k:v})
        db.session.commit()
        return 201


class ImageListApi(Resource):
    def get(self, contestId):
        images = {}
        for c in Image.query.filter(Image.contestId == contestId):
            image = prepare_dict_for_json(c.__dict__)
            images[image['id']] = image
        return images

    # post -> add new image
    def post(self, contestId):
        args = parser.parse_args()

        for k,v in args.iteritems():
            if isinstance(Image.__table__.c[k].type,
                    sqlalchemy.sql.sqltypes.DateTime):
                if v != None:
                    args[k] = datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")

        image = Image(args)

        db.session.add(image)
        db.session.commit()
        return 201
