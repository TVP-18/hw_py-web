from datetime import datetime

import pydantic
from aiohttp import web
from gino import Gino

PG_DSN = f'postgres://postgres:super@127.0.0.1:5432/aiohttp_test'

app = web.Application()
db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return f'User({self.id}, {self.name})'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.username,
            'email': self.email
        }


class Ad(db.Model):
    __tablename__ = 'ads'

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
            'date_create': str(self.date_create),
            'id_owner': self.id_owner
        }


class AdSerializer(pydantic.BaseModel):
    title: str
    text: str
    id_owner: int


# views
async def get_ads(request):
    ads = await Ad.query.gino.all()
    resp = {'count': len(ads), 'items': [ad.to_dict() for ad in ads]}

    return web.json_response(resp, status=200)


async def get_ad(request):
    ad_id = request.match_info['ad_id']
    ad = await Ad.get(int(ad_id))
    ad_data = ad.to_dict()
    return web.json_response(ad_data, status=200)


async def post_ad(request):
    ad_data = await request.json()

    user = await User.get(int(ad_data['id_owner']))
    if user is None:
        return web.json_response({'error': 'Not Found Owner'}, status=404)

    ad_serialized = AdSerializer(**ad_data)
    ad_data = ad_serialized.dict()
    new_ad = await Ad.create(**ad_data)
    return web.json_response(new_ad.to_dict(), status=200)


async def put_ad(request):
    ad_id = request.match_info['ad_id']

    ad = await Ad.get(int(ad_id))

    if ad is None:
        return web.json_response({'error': 'Not Found Ad'}, status=404)
    else:
        ad_data = await request.json()

        await ad.update(title=ad_data['title'], text=ad_data['text'], id_owner=ad_data['id_owner']).apply()

        return web.json_response(ad.to_dict(), status=200)


async def delete_ad(request):
    ad_id = request.match_info['ad_id']

    ad = await Ad.get(int(ad_id))

    if ad is None:
        return web.json_response({'error': 'Not Found Ad'}, status=404)
    else:
        await ad.delete()

        return web.json_response({}, status=200)


async def init_orm(app):
    await db.set_bind(PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


app.add_routes([web.get('/ads/', get_ads)])
app.add_routes([web.get('/ads/{ad_id}', get_ad)])
app.add_routes([web.post('/ads/', post_ad)])
app.add_routes([web.put('/ads/{ad_id}', put_ad)])
app.add_routes([web.delete('/ads/{ad_id}', delete_ad)])

app.cleanup_ctx.append(init_orm)
web.run_app(app, port=8000)
