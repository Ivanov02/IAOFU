from get_user_matches_ids import *
from get_league_itemts import *


def get_match_details():
    items_dict = get_items_dict()
    list_of_match_ids = get_user_mathces_ids(constants_and_parameters.number_to_start_pulling,
                                             constants_and_parameters.number_of_matches_to_pull)

    for match in list_of_match_ids:
        url_get_match_details = f'{constants_and_parameters.api_url_get_match_details}/{match}?api_key={constants_and_parameters.api_key}'
        response = requests.get(url_get_match_details)
        match_data = response.json()

        participants = match_data['info']['participants']

        list_of_summoners_detail = []
        for participant in participants:
            items = [items_dict.get(participant[f'item{i}'], 'Unknown Item') for i in range(7)]
            items_formatted = ', '.join(items)

            dataframe_dict = dict(
                summoner_name=f"{participant['summonerName']}",
                champion_name=f"{participant['championName']}",
                kills=f"{participant['kills']}",
                deaths=f"{participant['deaths']}",
                assists=f"{participant['assists']}",
                lane=f"{participant.get('teamPosition', 'Unknown Lane')}",
                team_color=f"{participant['teamId']}",
                items = f"{items_formatted}"

            )

            list_of_summoners_detail.append(dataframe_dict)

        return list_of_summoners_detail
