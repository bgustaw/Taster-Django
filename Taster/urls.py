from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('add-recipe', views.add_recipe, name='add_recipe'),
    path('like-post', views.like_post, name='like_post'),
    path('filter-view', views.filter_view, name='filter_view'),
    path('search-view', views.search_view, name='search_view'),
]



