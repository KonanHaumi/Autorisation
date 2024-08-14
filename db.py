import asyncpg
import settings

async def db_connect(app):
    app['db'] = await asyncpg.create_pool(
        database=settings.DB_CONFIG['database'],
        user=settings.DB_CONFIG['user'],
        password=settings.DB_CONFIG['password'],
        host=settings.DB_CONFIG['host'],
        port=settings.DB_CONFIG['port'],
    )

async def init_db(app):
    async with app['db'].acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

async def close_db(app):
    await app['db'].close()