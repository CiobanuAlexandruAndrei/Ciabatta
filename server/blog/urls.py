from django.urls import path
from . import views

urlpatterns = [
    path('search-keyword', views.search_keyword, name='search_keyword'),
    path('save-keyword', views.save_keyword, name='save_keyword'),
    path('get-keyword-clusters', views.get_keywords_clusters, name='get_keywords_clusters'),
    path('generate-keyword-suggestions', views.generate_keyword_suggestions, name='generate_keyword_suggestions'),
]
