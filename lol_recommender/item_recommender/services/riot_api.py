import requests
from typing import List, Dict, Any
from .constants import (
    API_URL_GET_PUUID,
    API_URL_GET_MATCHES_IDS,
    API_URL_GET_MATCH_DETAILS,
    API_URL_GET_CHAMPION_DETAILS,
    PATCH_VERSION,
    PATCH_VERSION_DDRAGON,
    API_KEY
)


class RiotAPIService:
    def __init__(self, api_key: str = API_KEY):
        self.api_key = api_key

    def get_user_puuid(self, username: str, tagline: str) -> str:
        """Get user PUUID from Riot ID."""
        api_request_link = f"{API_URL_GET_PUUID}/{username}/{tagline}?api_key={self.api_key}"
        response = requests.get(api_request_link)
        output = response.json()
        return output["puuid"]

    def get_user_matches_ids(self, username: str, tagline: str, start: int = 0, count: int = 20) -> List[str]:
        """Get list of match IDs for a user."""
        user_puuid = self.get_user_puuid(username, tagline)
        match_ids_url = f'{API_URL_GET_MATCHES_IDS}/{user_puuid}/ids'
        params = {
            'api_key': self.api_key,
            'start': start,
            'count': count
        }
        response = requests.get(match_ids_url, params=params)
        return response.json()

    def get_items_dict(self) -> Dict[int, str]:
        """Get dictionary of item IDs to names."""
        items_url = f"https://ddragon.leagueoflegends.com/cdn/{PATCH_VERSION}/data/en_US/item.json"
        items_data = requests.get(items_url).json()
        return {int(item_id): item_info['name']
                for item_id, item_info in items_data['data'].items()}

    def get_champion_details(self, champion_name: str) -> str:
        """Get champion tags."""
        if champion_name == "FiddleSticks":
            champion_name = "Fiddlesticks"

        url = f"{API_URL_GET_CHAMPION_DETAILS}/{PATCH_VERSION_DDRAGON}/data/en_US/champion/{champion_name}.json"
        response = requests.get(url)
        champion_data = response.json()
        champion_info = champion_data['data'][champion_name]
        return ", ".join(champion_info.get('tags', []))

    def get_match_details(self, match_id: str) -> Dict[str, Any]:
        """Get detailed match information."""
        url = f'{API_URL_GET_MATCH_DETAILS}/{match_id}?api_key={self.api_key}'
        response = requests.get(url)
        return response.json()

    def get_matches_data(self, username: str, tagline: str, start: int = 0, count: int = 20) -> List[Dict[str, Any]]:
        """Get processed match data for a user."""
        items_dict = self.get_items_dict()
        match_ids = self.get_user_matches_ids(username, tagline, start, count)

        matches_data = []
        for match_id in match_ids:
            match_data = self.get_match_details(match_id)

            teams = match_data['info']['teams']
            winner_dict = {team['teamId']: team['win'] for team in teams}

            for participant in match_data['info']['participants']:
                items = [items_dict.get(participant[f'item{i}'], 'Unknown Item')
                         for i in range(7)]
                items_formatted = ', '.join(items)
                tags = self.get_champion_details(participant['championName'])

                matches_data.append({
                    'summoner_name': participant['summonerName'],
                    'champion_name': participant['championName'],
                    'tags': tags,
                    'kills': participant['kills'],
                    'deaths': participant['deaths'],
                    'assists': participant['assists'],
                    'lane': participant.get('teamPosition', 'Unknown Lane'),
                    'team_color': participant['teamId'],
                    'has_won': winner_dict[participant['teamId']],
                    'goldEarned': participant['goldEarned'],
                    'totalDamageDealtToChampions': participant['totalDamageDealtToChampions'],
                    'totalMinionsKilled': participant['totalMinionsKilled'],
                    'neutralMinionsKilled': participant['neutralMinionsKilled'],
                    'items': items_formatted
                })

        return matches_data