import requests
import api_connection

api_url = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id"
api_key = api_connection.api_key
user_tag_line = "EUNE"
game_name = "Vonavi"

api_access_url = f"{api_url}/{game_name}/{user_tag_line}?api_key={api_key}"

response = requests.get(api_access_url)
output = response.json()

print(output)