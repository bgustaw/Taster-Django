from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('favourites', views.favourites, name="favourites"),
    path('<username>/edit', views.edit_account, name='edit_account'),
    path('<username>/recipes', views.recipes, name='recipes'),
    path('<username>/<recipe_name>', views.recipe, name='recipe_name')
]
