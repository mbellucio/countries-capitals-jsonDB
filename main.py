import requests
from translate import Translator 
import json
from country_filter import COUNTRIES_DESIRED


response = requests.get(url='https://restcountries.com/v2/all')
print(response.raise_for_status())

json_data = response.json()


europe = []
south_america = []
north_america = []
asia = []
oceania = []
africa = []

south_america_countries = ['Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela']
languages_to_translate = ['pt-BR', 'es-ES', 'fr-FR']

for country in json_data:
    if country['name'] not in COUNTRIES_DESIRED:
        continue
    else:
        try:
            region = country['region']
            translator = Translator(to_lang='pt-BR')
            country_name = translator.translate(country['name'])

            if region == 'Americas':
                if country['name'] in south_america_countries:
                    region = 'South America'
                else:
                    region = 'North America'

            capital_in_mtpl_langs = [country['capital']]

            for lang in languages_to_translate:
                translator = Translator(to_lang=lang)
                translation = translator.translate(country['capital'])
                capital_in_mtpl_langs.append(translation)

            current_country = {
                        'Country': country_name,
                        'Capital': capital_in_mtpl_langs
                    }

            match region:
                case 'Asia':
                    asia.append(current_country)

                case 'Europe':
                    europe.append(current_country)

                case 'Africa':
                    africa.append(current_country)

                case 'Oceania':
                    oceania.append(current_country)

                case 'South America':
                    south_america.append(current_country)

                case 'North America':
                    north_america.append(current_country)

        except KeyError:
            continue


data = {
    'Europa': europe,
    'América do Sul': north_america,
    'América do Norte': south_america,
    'Ásia': asia,
    'Oceania': oceania,
    'África': africa
}


with open("countries.json", 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False)




