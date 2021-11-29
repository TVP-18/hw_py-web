from datetime import datetime

from aiohttp import web
from gino import Gino

PG_DSN = f'postgres://db:pass@127.0.0.1:5432/aiohttp_test'

app = web.Application()
db = Gino()


class Ad(db.Model):
    __tablename__ = 'ads'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    text = db.Column(db.String(500), index=True)
    id_owner = db.Column(db.Integer)
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
async def get_ads(self):
    return web.json_response({'count': 0, 'item': []})

async def get_ad(self):
    print(self)
    ad_id = self.request.match_info['ad_id']
    print(ad_id)
    ad = await Ad.get(int(ad_id))
    print(ad)
    ad_data = ad.to_dict()
    return web.json_response(ad_data)


async def init_orm(app):
    # print('приложение стартовало')

    await db.set_bind(PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


app.add_routes([web.get('/ads/', get_ads)])
app.add_routes([web.get('/ads/{ad_id:\d+}', get_ad)])
app.cleanup_ctx.append(init_orm)
web.run_app(app, port=8000)
