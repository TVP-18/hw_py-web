from datetime import datetime
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# 'postgresql://postgres:super@127.0.0.1:5432/flask_test'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(100))
    ads = db.relationship('Ad', backref='owner', lazy=True)

    def __repr__(self):
        return f'User({self.id}, {self.name})'


class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    text = db.Column(db.String(500), index=True)
    id_owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f'Ad({self.id}, {self.title})'



# migrate = Migrate(app, db)
#
#
# if __name__ == "__main__":
#     app.run()
