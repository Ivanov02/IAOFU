import constants_and_parameters
import requests
def get_champion_details(champion_name):
    url = f"{constants_and_parameters.api_url_get_champion_details}/{constants_and_parameters.patch_version_ddragon}/data/en_US/champion/{champion_name}.json"
    response = requests.get(url)
    champion_data = response.json()
    champion_info = champion_data['data'][champion_name]
    tags = ", ".join(champion_info.get('tags', []))

    return tags