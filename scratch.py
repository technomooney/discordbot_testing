import json
import requests


url = 'https://8ball.delegator.com/magic/JSON/'
question = input('what is a question? ')
response = requests.get(url+question).json()
print(response['magic']['answer'])
print(response)