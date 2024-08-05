insert_query_vish_posts_text = '''
INSERT INTO vish_posts_text (id, text) 
VALUES (%s, %s)
'''

insert_query_vish_posts_stat = '''
INSERT INTO vish_posts_text (id, date, comments_count, likes_count, reposts_count, views_count, post_type) 
VALUES (%s, %s, %s, %s, %s, %s, %s)
'''

# GET some posts
response = requests.get(
    url='https://api.vk.com/method/wall.get',
    params={
        'access_token': TOKEN_USER,
        'owner_id': OWNER_ID,
        'v': VERSION,
        'offset': 0,
        'count': 2,
        'filter': 'owner'
    }
).json()

# Check that response is valid data with posts
try:
    data_raw = pd.DataFrame(response['response']['items'])
except KeyError as error:
    error_info = response['error']
    print(f'{error_info['error_code']=}')
    raise AssertionError(error_info['error_msg'])

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



cur = conn.cursor()
print('GET CONNECTION TO DATABASE!!')

data[['id', 'text']].to_sql('vish_posts_text', con=conn, if_exists='append', index=False)

conn.commit()

cur.close()
conn.close()
