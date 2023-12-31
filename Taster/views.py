from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from django.contrib.auth.decorators import login_required

from TasterWebApp import settings
from Users.models import CustomUser
from .models import Country, Recipe, StepsFile, FoodImage
import os
from .parsers import time_parser, data_to_db_req

DIETS_DATA = ('Vegan', 'Vegetarian', 'Keto', 'Gluten-free', 'Sugar-free', 'Lactose-free', 'Low carb', 'Low fat',
              'Low calorie', 'High protein', 'Mediterranean')
FILTERS = ('Region', 'Popularity', 'Upload date', 'Portions', 'Diets', 'Time needed')
CONTINENT_DICT = {'AF': 'Africa', 'NA': 'North America', 'OC': 'Oceania', 'AS': 'Asia', 'EU': 'Europe',
                  'SA': 'South America', 'AN': 'Antarctica'}
country_dict = {c.alpha2_code: c.country for c in Country.objects.all()}


def home(request):
    all_recipes = Recipe.objects.order_by('-likes')
    images_path = [(r.images.all()[0].image_file, r.images.all()[1].image_file) for r in all_recipes]
    context = {'recipes': all_recipes, 'images_path': images_path, 'filters': FILTERS, 'diets': DIETS_DATA,
               'country_dict': country_dict, 'continent_dict': CONTINENT_DICT}
    return render(request, 'recipe_view_manager.html', context)


def like_post(request):
    if request.method == 'POST':
        user: CustomUser = request.user
        recipe_id = request.POST['recipe_id']
        liked_recipe = Recipe.objects.get(pk=recipe_id)  # get liked recipe
        if liked_recipe not in user.get_liked_recipes():
            liked_recipe.likes += 1
            liked_recipe.save()
            user.liked_recipes.add(liked_recipe)
        else:
            liked_recipe.likes -= 1
            liked_recipe.save()
            user.liked_recipes.remove(liked_recipe)
        return HttpResponse(liked_recipe.likes)
    else:
        return HttpResponse("Request method is not a POST")


def filter_view(request):
    if request.method == 'POST':
        filter_by_data: QueryDict = request.POST
        values = list(filter_by_data.values())[1:]
        new_queue = data_to_db_req(*values)
        filtered_recipes = eval(new_queue)
        images_path = [(r.images.all()[0].image_file, r.images.all()[1].image_file) for r in filtered_recipes]
        return render(request, 'recipes_content.html', {'recipes': filtered_recipes,
                      'images_path': images_path})


def search_view(request):
    if request.method == 'POST':
        value = request.POST['keyword']
        recipes = Recipe.objects.filter(name__contains=value)
        images_path = [(r.images.all()[0].image_file, r.images.all()[1].image_file) for r in recipes]
        return render(request, 'recipes_content.html', {'recipes': recipes, 'images_path':
                      images_path})


@login_required
def add_recipe(request):
    if request.method == "POST":

        name = request.POST['mealName']
        portions = request.POST['portions']
        diets = request.POST['diets']
        prepare_time = request.POST['parsedPrepTimeDelta']
        cooking_time = request.POST['parsedCookTimeDelta']
        full_time = time_parser(prepare_time, cooking_time)
        nutrition_data = request.POST['parsedNutritionData']
        ingredients = request.POST['parsedIngredients']
        short_description = request.POST['shortDesc']
        steps = request.POST['parsedSteps']
        publisher: CustomUser = request.user
        country = publisher.country

        # create text file
        text_file_name = f"{name}-{publisher.username}-{country}.txt"
        text_file_path = os.path.join(settings.MEDIA_ROOT, 'recipes', text_file_name)
        with open(text_file_path, 'w', encoding='utf-8') as textRecipe:
            step_list = steps.split('&')
            for step in step_list:
                textRecipe.write(f"{step}\n")

        recipe = Recipe(name=name, portions=portions, diets=diets, prepare_time=prepare_time, cooking_time=cooking_time,
                        full_time=full_time, nutrition_data=nutrition_data, ingredients=ingredients, country=country,
                        publisher=publisher, short_description=short_description)
        recipe.save()
        steps_file = StepsFile(filename=text_file_name, text_file='recipes/' + text_file_name, recipeS=recipe,
                               publisher=publisher)
        steps_file.save()
        recipe.steps = steps_file
        recipe.save()

        # get files
        images_objects = request.FILES.getlist('file')
        for file in images_objects:
            image = FoodImage(filename=file, image_file=file, recipe=recipe, publisher=publisher)
            image.save()
            recipe.images.add(image)

        redirect('add_recipe')

    # context data
    sub_site_title = 'Add recipe'
    hours = tuple(h for h in range(24))
    minutes = tuple(m for m in range(0, 60, 5))
    repeat = (1, 2, 3)
    nutrition = ('kcal', 'fat', 'saturates', 'carbs', 'sugars', 'fibre', 'protein', 'salt')
    context = {'hours': hours, 'minutes': minutes, 'repeat': repeat, 'diets': DIETS_DATA, 'nutrition_data': nutrition,
               'sub_site_title': sub_site_title}
    return render(request, 'add_recipe.html', context)
