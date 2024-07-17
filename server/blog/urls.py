from django.urls import path
from . import views

urlpatterns = [
    path('search-keyword', views.search_keyword, name='search_keyword'),
    path('save-keyword', views.save_keyword, name='save_keyword'),
    path('get-keyword-clusters', views.get_keywords_clusters, name='get_keywords_clusters'),
    path('generate-keyword-suggestions', views.generate_keyword_suggestions, name='generate_keyword_suggestions'),
    path('get-api-usage-costs', views.get_api_usage_costs, name='get_api_usage_costs'),
    path('add-keyword-to-cluster', views.add_keyword_to_cluster, name='add_keyword_to_cluster'),
    path('create-keyword-cluster', views.create_keyword_cluster, name='create_keyword_cluster'),
    path('delete-keyword-cluster', views.delete_keyword_cluster, name='delete_keyword_cluster'),
]
