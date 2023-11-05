from django.contrib import admin
from.models import *


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'publisher', 'upload_date', 'diets', 'portions', 'likes')
    ordering = ('upload_date',)
    search_fields = ('name', )


@admin.register(FoodImage)
class FoodImageAdmin(admin.ModelAdmin):
    list_display = ('filename', 'image_file', 'recipe', 'publisher')
    ordering = ('filename', )
    search_fields = ('filename', )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country', 'continent', 'alpha2_code')
    ordering = ('country',)
    search_fields = ('country',)
