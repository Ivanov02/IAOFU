import requests
from django.conf import settings
from functools import lru_cache

import requests
from django.conf import settings
from functools import lru_cache


@lru_cache(maxsize=1)
def get_items_data():
    """
    Get all item data from Data Dragon, including images.
    Cached to avoid repeated API calls.
    """
    version = settings.PATCH_VERSION_DDRAGON
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
    response = requests.get(url)
    return response.json()


def get_item_details(item_name, items_data=None):
    """Get all details for a specific item."""
    if items_data is None:
        items_data = get_items_data()

    # Debug print
    print(f"Looking for item: {item_name}")

    for item_id, item_info in items_data['data'].items():
        if item_info['name'] == item_name:
            version = settings.PATCH_VERSION_DDRAGON

            # Debug print
            print(f"Found item info: {item_info}")

            return {
                'name': item_info['name'],
                'image_url': f"https://ddragon.leagueoflegends.com/cdn/{version}/img/item/{item_info['image']['full']}",
                'description': item_info.get('description', ''),
                'gold': item_info['gold']['total'],
                'stats': item_info.get('stats', {}),
                'plaintext': item_info.get('plaintext', '')
            }

    print(f"No item found for name: {item_name}")  # Debug print
    return None


def get_item_image_url(item_name, items_data=None):
    """Get the image URL for a specific item."""
    if items_data is None:
        items_data = get_items_data()

    print(f"Looking for item: {item_name}")  # Debug print

    # Find item ID by name
    for item_id, item_info in items_data['data'].items():
        if item_info['name'] == item_name:
            version = settings.PATCH_VERSION_DDRAGON
            image_url = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/item/{item_info['image']['full']}"
            print(f"Found image URL: {image_url}")  # Debug print
            return image_url

    print(f"No image found for item: {item_name}")  # Debug print
    return None  # Return None if item not found


def get_champion_image_url(champion_name, settings=None):
    """Get the champion splash art URL from Data Dragon."""
    # Remove spaces and special characters from champion name
    champion_name = champion_name.replace(" ", "").replace("'", "").replace(".", "")

    # Special cases
    if champion_name == "Wukong":
        champion_name = "MonkeyKing"
    elif champion_name == "Renata":
        champion_name = "RenataGlasc"
    elif champion_name == "Nunu":
        champion_name = "Nunu&Willump"

    # Construct the URL using the settings version
    version = getattr(settings, 'PATCH_VERSION_DDRAGON', '14.23.1')  # Use default if not in settings

    # You can choose between different types of images:
    # 1. Square icon: f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champion_name}.png"
    # 2. Loading screen: f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champion_name}_0.jpg"
    # 3. Splash art: f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion_name}_0.jpg"

    return f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champion_name}.png"