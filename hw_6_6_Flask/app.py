from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session

import config
from flask_migrate import Migrate
from flask import request, jsonify

from models import Ad





app = Flask(__name__)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=config.POSTGRE_URI)
db = SQLAlchemy(app)
# migrate = Migrate(app, db)

#
#
#
# def get_ads():
#     if request.method == 'GET':
#         session = Session()
#         query = session.query(Ad).all()
#         print(query)
#         return jsonify({'status': 'OK'})
#
#     return {'status': 'OK'}
#
#
# def get_ad(id_ad):
#     session = Session()
#     # query = Query([Track], session=session)
#     query = session.query(Ad).get(id_ad)
#     print(query)
#     print(id_ad)
#     if request.method == 'GET':
#         return jsonify({'status': 'OK'})
#
#     return {'status': 'OK'}
#
#
# app.add_url_rule('/ads/', view_func=get_ads, methods=['GET', ])
# app.add_url_rule('/ads/<int:id_ad>', view_func=get_ad, methods=['GET', ])
#
#
# if __name__ == '__main__':
#     app.run()
