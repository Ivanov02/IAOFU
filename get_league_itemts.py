import constants_and_parameters
import requests


def get_items_dict():
    items_url = f"https://ddragon.leagueoflegends.com/cdn/{constants_and_parameters.patch_version}/data/en_US/item.json"
    items_data = requests.get(items_url).json()
    items_dict = {int(item_id): item_info['name'] for item_id, item_info in items_data['data'].items()}

    return items_dict

