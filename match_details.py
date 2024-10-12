import requests
import api_connection

api_key = api_connection.api_key
matches_data = []
match_ids = ['EUN1_3659950220', 'EUN1_3659915732', 'EUN1_3659584809', 'EUN1_3659586310', 'EUN1_3659554477',
             'EUN1_3659539345', 'EUN1_3659301326', 'EUN1_3659275876', 'EUN1_3659242647', 'EUN1_3659223808',
             'EUN1_3658942751', 'EUN1_3658945074', 'EUN1_3658775623', 'EUN1_3631784954', 'EUN1_3631750117',
             'EUN1_3547471467', 'EUN1_3547441927', 'EUN1_3547426904', 'EUN1_3547412508', 'EUN1_3547332544']

# for match_id in matches_data:
#     match_detail_url = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}'
#     response = requests.get(match_detail_url, params={'api_key': api_key})
#     print(response)
#     match_data = response.json()
#     matches_data.append(match_data)


response_2 = requests.get(f'https://europe.api.riotgames.com/lol/match/v5/matches/EUN1_3659950220',
                          params={'api_key': api_key})
print(response_2)

match_data = response_2.json()
print(matches_data)
