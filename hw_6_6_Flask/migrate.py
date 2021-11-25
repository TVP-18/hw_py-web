# модуль для миграции БД
# Чтобы выполнить миграции, надо
# FLASK_APP=migrate:application flask db init
# FLASK_APP=migrate:application flask db migrate -m 'first migration'
# FLASK_APP=migrate:application flask db upgrade

import app

from flask_migrate import Migrate

application = app.app
migrate = Migrate(application, app.db)
