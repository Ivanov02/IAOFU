import requests


def get_user_puuid(api_url_a, api_key_a, user_name_a, user_tag_line_a):
    api_url = api_url_a
    api_key = api_key_a
    user_name = user_name_a
    user_tag_line = user_tag_line_a

    api_request_link = f"{api_url}/{user_name}/{user_tag_line}?api_key={api_key}"

    response = requests.get(api_request_link)
    output = response.json()

    return output["puuid"]
