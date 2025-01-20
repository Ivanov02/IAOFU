from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from ..services.recommender import ItemRecommenderService
from ..services.utils import get_items_data, get_item_image_url, get_item_details, get_champion_image_url
from pathlib import Path

# Initialize services
recommender = ItemRecommenderService()


def index(request):
    """Main page with champion selection form."""
    champions = []
    output_path = Path(settings.BASE_DIR) / 'output.csv'

    if output_path.exists():
        recommender.initialize_from_csv(output_path)
        champions = sorted(recommender.champion_to_id.keys()) if recommender.champion_to_id else []

    return render(request, 'recommender/index.html', {'champions': champions})


def get_recommendations(request):
    """API endpoint for getting item recommendations."""
    if request.method == 'POST':
        champion_name = request.POST.get('champion')
        if champion_name:
            try:
                items = recommender.recommend_items_for_champion(champion_name)
                items_data = get_items_data()

                # Debug print
                print(f"Recommending items for {champion_name}:", items)

                # Add full details for each item
                items_with_details = []
                for item_name in items:
                    item_details = get_item_details(item_name, items_data)
                    if item_details:
                        items_with_details.append(item_details)
                        print(f"Added details for {item_name}:", item_details)  # Debug print

                champion_image = get_champion_image_url(champion_name, settings)

                response_data = {
                    'success': True,
                    'items': items_with_details,
                    'champion_image': champion_image,

                }
                print("Sending response:", response_data)  # Debug print

                return JsonResponse(response_data)
            except Exception as e:
                print(f"Error in get_recommendations: {str(e)}")  # Debug print
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
    return JsonResponse({
        'success': False,
        'error': 'Invalid request'
    }, status=400)
