import requests


raise RuntimeError('UHODY')

# переменные 
TOKEN_USER = #ваш токен
VERSION = #версися api vk
DOMAIN =  #ваш domain

# через api vk вызываем статистику постов
response = requests.get('https://api.vk.com/method/wall.get',
params={'access_token': TOKEN_USER,
        'v': VERSION,
        'domain': DOMAIN,
        'count': 10,
        'filter': str('owner')})

data = response.json()['response']['items']

response = requests.get('https://api.vk.com/method/wall.get',
params={'access_token': TOKEN_USER,
        'v': VERSION,
        'owner_id': # ваш id_owner,
        'post_ids': post_id})


print(requests.get())