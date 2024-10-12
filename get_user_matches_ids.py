import requests
from get_user_puuid import get_user_puuid


def get_user_mathces_ids(api_url_match_ids_a, api_key_a, start_a, count_a, api_url_puuid_a, user_name_a,
                         user_tag_line_a):
    user_puuid = get_user_puuid(api_url_puuid_a, api_key_a, user_name_a, user_tag_line_a)
    match_ids_url = f'{api_url_match_ids_a}/{user_puuid}/ids'
    params = {'api_key': api_key_a, 'start': start_a, 'count': count_a}
    response = requests.get(match_ids_url, params=params)
    match_ids = response.json()

    return match_ids
