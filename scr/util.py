import requests
import pandas as pd
from os import getenv
from dotenv import load_dotenv
import pprint
import psycopg2


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
)

data_raw = pd.DataFrame(response.json()['response']['items'])

for column in ['likes', 'comments', 'reposts', 'views']:
    data_raw[column + '_count'] = data_raw[column].apply(lambda x: x['count'])

data_raw[['text', 'post_type']] = data_raw[['text', 'post_type']].astype('string')

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

# data.info()
pprint.pprint(data.iloc[:2].to_dict())
print('\n===================================\n')
conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host='db'
)
cur = conn.cursor()
print('GET CONNECTION TO DATABASE!!')

cur.execute("""
    CREATE TABLE IF NOT EXISTS vish_posts_text (
        id SERIAL PRIMARY KEY,
        title TEXT
    )
""")

conn.commit()

cur.close()
conn.close()
