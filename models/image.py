from models import db
from datetime import datetime

from flask_restful import reqparse, Resource

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


# converts f.e. datetime objects to strings
def prepare_dict_for_json(d):
    del(d['_sa_instance_state'])
    for k,v in d.iteritems():
        if isinstance(v, datetime):
            d[k] = str(v)
    return d

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
        #save only the changed attributes
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
    def get(self):
        images = {}
        for c in Image.query.all():
            image = prepare_dict_for_json(c.__dict__)
            images[image['id']] = image
        return images

    # post -> add new image
    def post(self):
        args = parser.parse_args()
        for k,v in args.iteritems():
            if isinstance(Image.__table__.c[k].type,
                    sqlalchemy.sql.sqltypes.DateTime):
                args[k] = datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
        image =  Image(args)
        db.session.add(image)
        db.session.commit()
        return 201
