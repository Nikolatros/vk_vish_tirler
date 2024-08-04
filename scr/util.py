import requests
import pandas as pd
from os import getenv
from dotenv import load_dotenv
import psycopg2
import time


# Load secret variables
load_dotenv()
TOKEN_USER = getenv('USER_TOKEN')
OWNER_ID = getenv('OWNER_ID')
VERSION = getenv('VERSION')
POSTGRES_USER = getenv('POSTGRES_USER')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
POSTGRES_DB = getenv('POSTGRES_DB')

# Check that API variables is presence
assert all([TOKEN_USER, OWNER_ID, VERSION])

# GET some posts
response = requests.get(
    url='https://api.vk.com/method/wall.get',
    params={
        'access_token': TOKEN_USER,
        'owner_id': OWNER_ID,
        'v': VERSION,
        'count': 2,
        'filter': 'owner'
    }
).json()
try:
    data_raw = pd.DataFrame(response['response']['items'])
except KeyError:
    print(response['error_code'])
    print(response['error_msg'])
    raise RuntimeError

for column in ['likes', 'comments', 'reposts', 'views']:
    data_raw[column + '_count'] = data_raw[column].apply(lambda x: x['count'])

data_raw[['text', 'post_type']] = (
    data_raw[['text', 'post_type']].astype('string')
)

columns = [
    'id',
    'date',
    'text',
    'comments_count',
    'likes_count',
    'reposts_count',
    'views_count',
    'post_type'
]
data = data_raw[columns]

conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host='db'
)

cur = conn.cursor()
print(time.localtime(), 'GET CONNECTION TO DATABASE!!')

cur.execute("""
    CREATE TABLE IF NOT EXISTS vish_posts_text (
        id SERIAL PRIMARY KEY,
        title TEXT
    )
""")

conn.commit()

cur.close()
conn.close()
