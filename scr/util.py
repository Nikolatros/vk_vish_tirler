import requests
import psycopg2
import time
import pandas as pd
from os import getenv
from dotenv import load_dotenv


# Load secret variables
load_dotenv()
TOKEN_USER = getenv('USER_TOKEN')
OWNER_ID = getenv('OWNER_ID')
VERSION = getenv('VERSION')
POSTGRES_USER = getenv('POSTGRES_USER')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
POSTGRES_DB = getenv('POSTGRES_DB')

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

# Check that response is valid data with posts
try:
    data_raw = pd.DataFrame(response['response']['items'])
except KeyError as error:
    error_info = response['error']
    print(f'{error=}')
    print(f'{error_info['error_code']=}')
    print(f'{error_info['error_msg']=}')
    exit()

# Unpack dicts in columns
for column in ['likes', 'comments', 'reposts', 'views']:
    data_raw[column + '_count'] = data_raw[column].apply(lambda x: x['count'])

# Convert unix-date to datetime
data_raw['date'] = pd.to_datetime(data_raw['date'], unit='s')

# Set datatype to columns with text
data_raw[['text', 'post_type']] = (
    data_raw[['text', 'post_type']].astype('string')
)

# Columns that will be written to database
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

conn.commit()

cur.close()
conn.close()
