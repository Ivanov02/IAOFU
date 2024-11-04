from get_user_matches_ids import *
from get_league_itemts import *
from get_champions_details import *
import constants_and_parameters
import pandas as pd


def get_match_details():
    items_dict = get_items_dict()
    list_of_match_ids = get_user_mathces_ids(constants_and_parameters.match_to_pull_from,
                                             constants_and_parameters.number_of_matches_to_pull)

    new_row = pd.DataFrame([{
        'summoner_name': constants_and_parameters.user_name,
        'summoner_tag_name': constants_and_parameters.user_tag_name,
        'match_to_pull_from': constants_and_parameters.match_to_pull_from,
        'number_of_matches_to_pull': constants_and_parameters.number_of_matches_to_pull,
        "last_pulled": constants_and_parameters.last_pulled,
        'unique_combination': constants_and_parameters.unique_combination
    }])

    list_of_summoners_detail = []
    for match in list_of_match_ids:
        url_get_match_details = f'{constants_and_parameters.api_url_get_match_details}/{match}?api_key={constants_and_parameters.api_key}'
        response = requests.get(url_get_match_details)
        match_data = response.json()

        teams = match_data['info']['teams']
        winner_dict = {team['teamId']: team['win'] for team in teams}

        participants = match_data['info']['participants']
        for participant in participants:
            items = [items_dict.get(participant[f'item{i}'], 'Unknown Item') for i in range(7)]
            items_formatted = ', '.join(items)
            tags = get_champion_details(participant['championName'])

            team_id = participant['teamId']
            has_won = winner_dict[team_id]

            dataframe_dict = dict(
                summoner_name=f"{participant['summonerName']}",
                champion_name=f"{participant['championName']}",
                tags=tags,
                kills=f"{participant['kills']}",
                deaths=f"{participant['deaths']}",
                assists=f"{participant['assists']}",
                lane=f"{participant.get('teamPosition', 'Unknown Lane')}",
                team_color=f"{team_id}",
                has_won=has_won,
                goldEarned=participant['goldEarned'],
                totalDamageDealtToChampions=participant['totalDamageDealtToChampions'],
                totalMinionsKilled=participant['totalMinionsKilled'],
                neutralMinionsKilled=participant['neutralMinionsKilled'],
                items=f"{items_formatted}"
            )

            list_of_summoners_detail.append(dataframe_dict)

    new_row.to_csv("last_run.csv", sep=",", header=False, index=False, mode="a")
    constants_and_parameters.last_run = pd.concat([constants_and_parameters.last_run, new_row], ignore_index=True)

    return list_of_summoners_detail
