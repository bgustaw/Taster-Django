from django.db import models
from django.utils import timezone
from TasterWebApp import settings
from cloudinary.models import CloudinaryField


class FoodImage(models.Model):
    filename = models.CharField(max_length=100)
    image_file = CloudinaryField('image')
    recipe = models.ForeignKey('Recipe', blank=False, null=True, on_delete=models.CASCADE)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.filename


class Country(models.Model):
    country = models.CharField(max_length=60)
    continent = models.CharField(max_length=50)
    alpha2_code = models.CharField(max_length=3)

    def __str__(self):
        return f'{self.country}'


class Recipe(models.Model):
    name = models.CharField(max_length=30, null=True)
    portions = models.IntegerField(null=True)
    diets = models.CharField(max_length=70, blank=True, null=True)
    prepare_time = models.CharField(max_length=15)
    cooking_time = models.CharField(max_length=15, null=True)
    full_time = models.PositiveIntegerField(null=True)
    nutrition_data = models.CharField(max_length=150, blank=True, null=True)
    images = models.ManyToManyField(FoodImage, blank=False, related_name='recipes')
    ingredients = models.TextField(blank=False, null=True)
    short_description = models.TextField(blank=True, null=True)
    steps = models.TextField(blank=False, null=True)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.SET_NULL)
    upload_date = models.DateTimeField(default=timezone.now)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=True, on_delete=models.SET_NULL)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} || {self.publisher}'
