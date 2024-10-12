import requests
import constants_and_parameters

match_id = "EUN1_3659950220"
url_get_match_details_test = f'{constants_and_parameters.api_url_get_match_details}/{match_id}'

headers = {
    'X-Riot-Token': constants_and_parameters.api_key
}

response = requests.get(url_get_match_details_test, headers=headers)
match_data = response.json()

participants = match_data['info']['participants']

for participant in participants:
    print(f"Nume Invocator: {participant['summonerName']}")
    print(f"Campion: {participant['championName']}")
    print(f"Kills: {participant['kills']}")
    print(f"Deaths: {participant['deaths']}")
    print(f"Assists: {participant['assists']}")
    print('-' * 20)