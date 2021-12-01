from aiohttp import web
from gino import Gino

PG_DSN = f'postgres://postgres:super@127.0.0.1:5432/aiohttp_test'

app = web.Application()
db = Gino()


async def init_orm(app):
    await db.set_bind(PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


app.cleanup_ctx.append(init_orm)
