from django.conf import settings

# API URLs
API_URL_GET_PUUID = f"{settings.RIOT_API_URL_BASE}/riot/account/v1/accounts/by-riot-id"
API_URL_GET_MATCHES_IDS = f"{settings.RIOT_API_URL_BASE}/lol/match/v5/matches/by-puuid"
API_URL_GET_MATCH_DETAILS = f"{settings.RIOT_API_URL_BASE}/lol/match/v5/matches"
API_URL_GET_CHAMPION_DETAILS = "https://ddragon.leagueoflegends.com/cdn"

# Versions
PATCH_VERSION = settings.PATCH_VERSION
PATCH_VERSION_DDRAGON = settings.PATCH_VERSION_DDRAGON

# API Key
API_KEY = settings.RIOT_API_KEY
