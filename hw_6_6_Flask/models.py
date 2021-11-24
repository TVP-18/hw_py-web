from sqlalchemy import exc

from app import db


class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    text = db.Column(db.String(500), index=True)
    id_owner = db.Column(db.Integer)
    date_create = db.Column(db.String(10))

    def __str__(self):
        return f'ID{self.id}'

