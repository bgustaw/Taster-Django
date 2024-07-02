from Taster.models import Recipe


def time_parser(prep_time, cook_time='H'):
    """ Parses and returns full time in minutes required for Recipe """
    if cook_time.startswith('H'):
        cook_time = '0H 0MIN'
    h1, m1, h2, m2 = [int(n) for n in prep_time[:-3].split('H')] + [int(n) for n in cook_time[:-3].split('H')]
    full_time = (h1 + h2) * 60 + (m1 + m2)
    return full_time


def transform_value(key, value):
    """ Transforms given AJAX value and returns a part of a string database query """
    match key:
        case 'continent':
            # filter
            value = value.split(',')
            query_part = f'.filter(country__continent__in={value})'
            return query_part
        case 'country':
            # filter
            value = value.split(',')
            query_part = f'.filter(country__alpha2_code__in={value})'
            return query_part
        case 'most_liked':
            # order
            value = '-likes'
            query_part = f'.order_by("{value}")'
            return query_part
        case 'newest':
            # order
            value = '-upload_date'
            query_part = f'.order_by("{value}")'
            return query_part
        case 'oldest':
            # order
            value = 'upload_date'
            query_part = f'.order_by("{value}")'
            return query_part
        case 'portions':
            # filter
            value = tuple(value.split('|'))
            query_part = f'.filter(portions__range={value})'
            return query_part
        case 'diets':
            # filter
            value = value[:-1].lower().split('|')
            query_part = f'.filter(diets__in={value})'
            return query_part
        case 'full_time':
            # filter
            print('value', value)
            value = time_parser(value)
            query_part = f'.filter(full_time__lte={value})'
            return query_part
        case _:
            raise TypeError(f'Provided {object} does not match any of cases')


def data_to_db_req(*args):
    """ Builds a string database query based on transformed values  """
    query_base = 'Recipe.objects'
    markers = ['continent', 'country', 'most_liked', 'newest', 'oldest', 'portions', 'diets', 'full_time']
    checked_filters = {markers[i]: value for i, value in enumerate(args) if value != '0'}  # sorts out not selected
    if not checked_filters:
        query_base += '.all()'
    else:
        for key in checked_filters:
            query_part = transform_value(key, checked_filters[key])
            query_base += query_part
    return query_base
