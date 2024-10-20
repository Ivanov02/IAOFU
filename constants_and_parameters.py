from api_connection import api_key

# constants

api_url_get_puuid = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id"
api_url_get_matches_ids = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid"
api_url_get_match_details = "https://europe.api.riotgames.com/lol/match/v5/matches"

# parameters
number_to_start_pulling = 0
number_of_matches_to_pull = 1
user_name = "Vonavi"
user_tag_name = "EUNE"
api_key = api_key
patch_version = "14.20.1"