from datetime import datetime
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(100))
    ads = db.relationship('Ad', backref='owner', lazy=True)

    def __repr__(self):
        return f'User({self.id}, {self.name})'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.username,
            'email': self.email
        }


class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    text = db.Column(db.String(500), index=True)
    id_owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f'Ad({self.id}, {self.title})'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'date_create': self.date_create,
            'id_owner': self.id_owner
        }


# views
@app.route('/ads/', methods=['GET'])
def get_ads():
    ads = Ad.query.all()
    resp = {'count': len(ads), 'items': [ad.to_dict() for ad in ads]}

    return make_response(jsonify(resp), 200)


@app.route('/ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):

    ad = Ad.query.get(ad_id)

    if ad is None:
        return make_response('error: Not Found', 404)
    else:
        return make_response(jsonify(ad.to_dict()), 200)


@app.route('/ads/', methods=['POST'])
def post_ad():

    ad = Ad(**request.json)
    db.session.add(ad)
    db.session.commit()

    return make_response(jsonify(ad.to_dict()), 200)


@app.route('/ads/<int:ad_id>', methods=['PUT'])
def put_ad(ad_id):
    ad = Ad.query.get(ad_id)

    if ad is None:
        return make_response(jsonify('error: Not Found'), 404)
    else:
        ad.id_owner = request.json['id_owner']
        ad.title = request.json['title']
        ad.text = request.json['text']

        db.session.commit()

    return make_response(jsonify(ad.to_dict()), 200)


@app.route('/ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    ad = Ad.query.get(ad_id)

    if ad is None:
        return make_response(jsonify('error: Not Found'), 404)
    else:
        db.session.delete(ad)
        db.session.commit()

        return make_response(jsonify({}), 204)


if __name__ == '__main__':
    app.run()
