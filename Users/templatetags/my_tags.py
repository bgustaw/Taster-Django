from django import template
from django.template import context
from Taster.models import Country

register = template.Library()


@register.filter
def get_continent(self):
    continent = Country.objects.get(alpha2_code=self).continent
    return continent


@register.filter
def get_image(self, i):
    return self.images.all()[i].image_file.url


@register.filter
def get(self, i):
    return self[i]


@register.filter
def get_key(self, i):
    if isinstance(self, dict):
        return list(self.keys())[i]
    else:
        raise TypeError(f'{type(self)} must be a dict')


@register.filter
def get_value(self, i):
    if isinstance(self, dict):
        return list(self.values())[i]
    else:
        raise TypeError(f'{type(self)} must be a dict')
