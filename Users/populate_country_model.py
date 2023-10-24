import pandas as pd
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TasterWebApp.settings")
import django

django.setup()
from Taster.models import Country

# read csv columns
df = pd.read_csv("../static/country-codes_csv.csv",
                 usecols=['ISO3166-1-Alpha-2', 'Continent', 'CLDR display name'])
continent_names_df = pd.read_csv('../static/continent-codes_csv.csv')

continent_mapping = dict(zip(continent_names_df['Code'], continent_names_df['Name']))
# replace short versions with full names
df['Continent'] = df['Continent'].replace(continent_mapping)

# sort alphabetical
df = df.sort_values(by='CLDR display name')

for index in range(len(df)):
    row = df.iloc[index]  # Access the row at the current index
    country = row['CLDR display name']
    continent = row['Continent']
    alpha2_code = row['ISO3166-1-Alpha-2']
    if isinstance(alpha2_code, float):
        alpha2_code = 'RR'
    else:
        alpha2_code = alpha2_code.lower()

    instance = Country(country=country, continent=continent, alpha2_code=alpha2_code)
    instance.save()
