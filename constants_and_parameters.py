from api_connection import api_key
import pandas as pd

# constants

api_url_get_puuid = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id"
api_url_get_matches_ids = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid"
api_url_get_match_details = "https://europe.api.riotgames.com/lol/match/v5/matches"
patch_version = "14.20.1"
api_key = api_key


# parameters

def user_inputs():
    user_name = str(input('Enter the user name: ').strip() or "Vonavi")
    user_tag_name = str(input('Enter the user tag: ').strip() or "EUNE")
    number_of_matches = int(input('Numer of matches to run: ').strip() or '1')

    return user_name, user_tag_name, number_of_matches


user_name, user_tag_name, number_of_matches = user_inputs()
unique_combination = user_name + user_tag_name
last_run = pd.read_csv("last_run.csv", sep=",", index_col=False)

if unique_combination in last_run['unique_combination'].values:
    match_to_pull_from = last_run.last_pulled.iat[-1] + 1
    number_of_matches_to_pull = number_of_matches
    last_pulled = last_run.last_pulled.iat[-1] + number_of_matches
else:
    match_to_pull_from = 0
    number_of_matches_to_pull = number_of_matches
    last_pulled = number_of_matches

