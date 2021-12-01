from aiohttp import web

from main import app, db
from models import User, Ad
import views

if __name__ == '__main__':
    web.run_app(app, port=8000)
