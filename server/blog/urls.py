from django.urls import path
from . import views

urlpatterns = [
    path('search-keyword', views.search_keyword, name='search_keyword'),
    path('save-keyword', views.save_keyword, name='save_keyword'),
    path('get-keywords', views.get_keywords, name='get_keywords'),
]
