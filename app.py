from aiohttp import web
from aiohttp_session import new_session, get_session
import hashlib
import aiohttp_jinja2
import jinja2
import db
import routes 

# Сначала создаем объект приложения
app = web.Application()

# Настройка Jinja2 для работы с шаблонами
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# Настройка маршрутов
routes.setup_routes(app)

# Настройка событий приложения для работы с базой данных
app.on_startup.append(db.db_connect)
app.on_startup.append(db.init_db)
app.on_cleanup.append(db.close_db)

# Запуск приложения
if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8000)
