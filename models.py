import asyncpg
from dotenv import load_dotenv
import os
load_dotenv()


bot_token = os.getenv('BOT_TOKEN')

conn = None

async def connect():
    global conn
    try:
        conn = await asyncpg.connect(
            database=os.getenv('DATABASE'),
            user = os.getenv('DB_USER'),
            host= os.getenv('HOST'),
            port=os.getenv('PORT'),
            password=os.getenv('DB_PASSWORD'),
        )
        print('Conected sccessfulyu')
    except Exception as e:
        print(e, 'connection failde')

async def craete_table():
    try:
        await conn.execute(""" CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                username VARCHAR(255)  UNIQUE,
                tg_id BIGINT NOT NULL UNIQUE,
                full_name VARCHAR(255),
                phone VARCHAR(17) ,
                address VARCHAR(50),
                created_at TIMESTAMP DEFAULT NOW()
        );


    """)
        print('tales createdb')
    except Exception as e:
        print(e, 'didnt crete tablesa')




async def register(tg_id, username, full_name, phone, address):
    try:
        await conn.execute("""INSERT INTO users(tg_id, username, full_name, phone, address)
                     VALUES($1, $2, $3, $4, $5)
    """,tg_id, username, full_name, phone, address)
        print('u register successfully ')
    except Exception as e:
        print(e, ";DIDNT REGISTERED")

async def get_user(tg_id):
    try:
        user = await conn.fetchrow("""select full_name from users where tg_id = $1
    """,tg_id)
        print('u register successfully ')
        return user
    except Exception as e:
        print(e, ";DIDNT REGISTERED")
