from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import new_session, get_session
import hashlib

# Обработчик для главной страницы
@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}

# Обработчик для регистрации
@aiohttp_jinja2.template('register.html')
async def register(request):
    if request.method == 'POST':
        data = await request.post()
        username = data['username']
        password = data['password']
        
        async with request.app['db'].acquire() as connection:
            await connection.execute('INSERT INTO users (username, password) VALUES ($1, $2)', username, password)

        return web.HTTPFound('/login')
    return {}

# Обработчик для входа в систему
@aiohttp_jinja2.template('login.html')
async def login(request):
    if request.method == 'POST':
        data = await request.post()
        username = data['username']
        password = data['password']
        
        async with request.app['db'].acquire() as connection:
            user = await connection.fetchrow('SELECT id FROM users WHERE username = $1 AND password = $2', username, password)
            if user:
                session = await new_session(request)
                session['user_id'] = user['id']
                return web.HTTPFound('/')

        return {'error': 'Неверное имя пользователя или пароль'}
    return {}

# Функция для установки маршрутов
def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/register', register)
    app.router.add_post('/register', register)
    app.router.add_get('/login', login)
    app.router.add_post('/login', login)