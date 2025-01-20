from django.urls import path
from .views.views import index, get_recommendations  # Changed from .views import views

urlpatterns = [
    path('', index, name='index'),
    path('get_recommendations/', get_recommendations, name='get_recommendations'),
]

