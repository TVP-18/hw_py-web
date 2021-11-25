from datetime import datetime
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# 'postgresql://postgres:super@127.0.0.1:5432/flask_test'
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
            'date_create': self.date_create
        }


# views
def get_ads():
    if request.method == 'GET':
        ads = [{ad.id: ad.to_dict()} for ad in Ad.query.all()]
        # сделать словарь
        return jsonify(ads)

    return {'status': 'OK'}


def get_ad(ad_id):
    if request.method == 'GET':
        ad = Ad.query.get(ad_id)

        return jsonify(ad.to_dict())

    return {'status': 'OK'}


app.add_url_rule('/ads/', view_func=get_ads, methods=['GET', ])
app.add_url_rule('/ads/<int:ad_id>', view_func=get_ad, methods=['GET', ])


# migrate = Migrate(app, db)
#
#
if __name__ == '__main__':
    app.run()
