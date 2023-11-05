import os
import sys

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from ipware import get_client_ip

from Taster.models import Recipe
from TasterWebApp import settings
from .forms import RegisterUserForm, ChangePasswordForm, EditUserForm
from Taster.views import country_dict
from .models import CustomUser


def login_user(request):
    global tup_path, next_path
    if request.method == 'GET':
        next_path = request.GET.get('next')
        tup_path = (next_path,)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if tup_path[0]:
                return redirect(tup_path[0])
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login_user')
    else:
        return render(request, 'login.html', {'sub_site_title': 'Login'})


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account successfully created')
            return redirect('home')
        else:
            server_errors = form.errors.values()
            message = ''
            for error in server_errors:
                message += error
            messages.error(request, message)

            return redirect('register')
    else:
        form = RegisterUserForm()
    client_ip, is_routable = get_client_ip(request)
    g = GeoIP2()
    if client_ip == '127.0.0.1':
        country = 'pl'
    else:
        country = f'{g.country_code(client_ip).lower()}'
    fields_labels = ['E-mail', 'Username', 'Password', 'Password confirmation']
    form_fields = ("email", "username", "password1", "password2",)
    context = {'form': form, 'country_dict': country_dict, 'labels': fields_labels, 'fields': form_fields,
               'suggested_country': country, 'sub_site_title': 'Register'}
    return render(request, 'register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required
def edit_account(request, username):
    if request.method == "POST":
        if 'old_password' in request.POST:
            form1 = ChangePasswordForm(request.user, request.POST)
            if form1.is_valid():
                user = form1.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password successfully updated')
            else:
                server_errors = form1.errors.values()
                message = ''
                for error in server_errors:
                    message += error
                messages.error(request, message)
            return redirect('edit_account', username)
        else:
            form2 = EditUserForm(request.POST, instance=request.user)
            if form2.is_valid():
                messages.success(request, 'Username and email successfully updated')
                user = form2.save()
                username = user.username
            else:
                server_errors = form2.errors.values()
                message = ''
                for error in server_errors:
                    message += error
                messages.error(request, message)
            return redirect('edit_account', username)
    user = request.user
    if username != user.username:
        messages.error(request, 'Forbidden request - navigate with top menu')
        return redirect('home')
    edit_user_form = EditUserForm(instance=user)
    password_change_form = ChangePasswordForm(user=user)
    context = {'user': user, 'e_form': edit_user_form, 'p_form': password_change_form, 'sub_site_title': 'Edit account'}
    return render(request, 'edit_account.html', context)


def recipes(request, username):
    user = CustomUser.objects.get(username=username)
    user_recipes = Recipe.objects.filter(publisher=user)
    context = {'recipes': user_recipes}
    if request.user.pk == user.pk:
        context['sub_site_title'] = 'My recipes'
    else:
        context['sub_site_title'] = f"{username}'s recipes"
    return render(request, 'recipe_view_manager.html', context)


def favourites(request):
    user: CustomUser = request.user
    user_favourites = user.get_liked_recipes()
    context = {'user': user, 'recipes': user_favourites, 'sub_site_title': 'Favourites'}
    return render(request, "recipe_view_manager.html", context)


def recipe(request, username, recipe_name):
    try:
        context = {}
        recipe_cls = Recipe.objects.get(name=recipe_name)
        if len(recipe_cls.diets) != 0:
            diets = recipe_cls.diets.split(',')
            context['diets'] = diets
        if len(recipe_cls.nutrition_data) != 0:
            nutrition = recipe_cls.nutrition_data.split(' | ')
            context['nutrition_per'] = nutrition[0]
            nutrition.pop(0)
            nutrition_names = ('kcal', 'fat', 'saturates', 'carbs', 'sugars', 'fibre', 'protein', 'salt')
            nutrition = {nutrition_names[i]: nutrition[i] for i in range(len(nutrition_names))}
            context.update({'nutrition': nutrition})

        ingredients = recipe_cls.ingredients.split(' | ')
        all_images_paths = [img.image_file.url for img in recipe_cls.images.all()]

        steps_list = recipe_cls.steps.split('&')
        context['steps_list'] = steps_list

        context2 = {'recipe': recipe_cls, 'all_images_paths': all_images_paths, 'username': username,
                    'ingredients': ingredients}
        context.update(context2)
    except Exception:
        return render(request, 'error.html')

    return render(request, 'recipe.html', context=context)


def admin_ajax_request(request):
    if request.method == "GET":
        action = request.GET['action']
        if action == 'resetLikes':
            all_recipes = Recipe.objects.all()
            for r in all_recipes:
                r.likes = 0
                r.save()
            return HttpResponse('Users liked recipes successfully reset')
        elif action == 'resetUsersLiked':
            all_users = CustomUser.objects.all()
            for u in all_users:
                u.liked_recipes.clear()
                u.save()
            return HttpResponse('Users liked recipes successfully reset')
        else:
            return HttpResponse('Something went wrong')
