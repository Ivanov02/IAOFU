from get_user_matches_ids import *
from get_league_itemts import *

items_dict = get_items_dict()
# get_user_mathces_ids(constants_and_parameters.number_to_start_pulling, constants_and_parameters.number_of_matches_to_pull)

match_id = "EUN1_3659950220"
url_get_match_details_test = f'{constants_and_parameters.api_url_get_match_details}/{match_id}'

headers = {
    'X-Riot-Token': constants_and_parameters.api_key
}

response = requests.get(url_get_match_details_test, headers=headers)
match_data = response.json()

participants = match_data['info']['participants']

# Bucla actualizată pentru a afișa numele itemelor
for participant in participants:
    print(f"Nume Invocator: {participant['summonerName']}")
    print(f"Campion: {participant['championName']}")
    print(f"Kills: {participant['kills']}")
    print(f"Deaths: {participant['deaths']}")
    print(f"Assists: {participant['assists']}")

    lane = participant.get('teamPosition', 'Unknown Lane')
    print(f"Lane: {lane}")

    # Afișează itemele cu numele lor în loc de coduri
    items = [items_dict.get(participant[f'item{i}'], 'Unknown Item') for i in range(7)]
    print(f"Iteme echipate: {items}")

    print('-' * 20)