from django.apps import AppConfig

class ItemRecommenderConfig(AppConfig):  # Changed from RecommenderConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'item_recommender'