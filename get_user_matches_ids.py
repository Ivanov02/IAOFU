import requests
import constants_and_parameters
from get_user_puuid import get_user_puuid


def get_user_mathces_ids(start_a, count_a):
    user_puuid = get_user_puuid(constants_and_parameters.api_key, constants_and_parameters.user_name,
                                constants_and_parameters.user_tag_name)
    match_ids_url = f'{constants_and_parameters.api_url_get_matches_ids}/{user_puuid}/ids'
    params = {'api_key': constants_and_parameters.api_key, 'start': start_a, 'count': count_a}
    response = requests.get(match_ids_url, params=params)
    match_ids = response.json()

    return match_ids

