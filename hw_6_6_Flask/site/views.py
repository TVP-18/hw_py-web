from flask import make_response, jsonify, request

from main import app, db
from models import Ad, User
from validator import validate
from schema import AD_CREATE


@app.route('/ads/', methods=['GET'])
def get_ads():
    ads = Ad.query.all()
    resp = {'count': len(ads), 'items': [ad.to_dict() for ad in ads]}

    return make_response(jsonify(resp), 200)


@app.route('/ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):

    ad = Ad.query.get(ad_id)

    if ad is None:
        return make_response({'error': 'Not Found Ad'}, 404)
    else:
        return make_response(jsonify(ad.to_dict()), 200)


@app.route('/ads/', methods=['POST'])
@validate('json', AD_CREATE)
def post_ad():

    user = User.query.get(request.json['id_owner'])
    if user is None:
        return make_response(jsonify({'error': 'Not Found Owner'}), 404)

    ad = Ad(**request.json)
    db.session.add(ad)
    db.session.commit()

    return make_response(jsonify(ad.to_dict()), 200)


@app.route('/ads/<int:ad_id>', methods=['PUT'])
# @validate('json', AD_CREATE)
def put_ad(ad_id):
    ad = Ad.query.get(ad_id)

    if ad is None:
        return make_response(jsonify({'error': 'Not Found Ad'}), 404)
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
        return make_response(jsonify({'error': 'Not Found Ad'}), 404)
    else:
        db.session.delete(ad)
        db.session.commit()

        return make_response(jsonify({}), 200)
