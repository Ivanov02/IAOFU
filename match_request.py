import api_connection
import requests

puuid = "VV0jbs4qQVAisFe92OzfBnCjOwqWGdYPukYi6Q2FJ9B4XnmOdOBdvmdvZWRA1jRWG8AamXmtFgDdIQ"
api_key = api_connection.api_key


match_ids_url = f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
params = {'api_key': api_key, 'start': 0, 'count': 20}
response = requests.get(match_ids_url, params=params)
match_ids = response.json()

print(match_ids)