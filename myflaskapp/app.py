import os
from flask import Flask, jsonify, render_template, request
import requests
import re
from PIL import Image

app = Flask(__name__)

def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}"

    response = requests.get(url)
    species_response = requests.get(species_url)

    if response.status_code != 200 or species_response.status_code != 200:
        return None

    pokemon = response.json()
    species = species_response.json()

    pokemon_data = {
        'id': pokemon['id'],
        'name': pokemon['name'].capitalize(),
        'sprite': pokemon['sprites']['front_default'],
        'types': [t['type']['name'] for t in pokemon['types']],
        'abilities': [{'name': a['ability']['name'], 'is_hidden': a['is_hidden']} for a in pokemon['abilities']],
        'weight': pokemon['weight'],
        'height': pokemon['height'],
        'description': species['flavor_text_entries'][0]['flavor_text'],
        'locations': []  # We'll add location data later if available.
    }

    # Get locations
    location_area_encounters = requests.get(pokemon['location_area_encounters']).json()
    for location in location_area_encounters:
        location_name = location['location_area']['name']
        pokemon_data['locations'].append(location_name)

    return pokemon_data

def get_regions():
    url = "https://pokeapi.co/api/v2/region/"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    regions = response.json()['results']
    return regions

def get_region_details(region_name):
    url = f"https://pokeapi.co/api/v2/region/{region_name.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    region = response.json()

    pokedexes = []
    seen_pokemon = set()  # Para evitar duplicados

    for pokedex in region['pokedexes']:
        pokedex_data = requests.get(pokedex['url']).json()
        for entry in pokedex_data['pokemon_entries']:
            pokemon_id = int(re.sub('[^0-9]', '', entry['pokemon_species']['url'][-4:-1]))  # Este es el número de la Pokédex nacional

            if pokemon_id not in seen_pokemon:  # Verificamos si el Pokémon ya fue agregado
                seen_pokemon.add(pokemon_id)

                # Obtenemos información adicional del Pokémon
                pokemon_details = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}").json()

                pokedexes.append({
                    'name': entry['pokemon_species']['name'],
                    'id': pokemon_id,
                    'sprite': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png",
                    'types': [t['type']['name'] for t in pokemon_details['types']]
                })

    pokedexes.sort(key=lambda x: x['id'])

    region_data = {
        'name': region['name'].capitalize(),
        'generation': region['main_generation']['name'].capitalize(),
        'map': region['locations'][0]['url'] if region['locations'] else None,  # Mapa de la región
        'pokedexes': pokedexes
    }

    return region_data

def get_type_sprite(type_url):
    response = requests.get(type_url)

    if response.status_code == 200:
        data = response.json()

        sprites = data['sprites']
        last_gen = sprites[list(sprites)[-1]]
        sprite = last_gen[list(last_gen)[-1]]

        return sprite['name_icon']

def get_types():
     # URL de la API para obtener todos los tipos de Pokémon
    url = 'https://pokeapi.co/api/v2/type/'

    # Realizar la solicitud a la API
    response = requests.get(url)

    # Si la solicitud es exitosa (código de estado 200)
    if response.status_code == 200:
        data = response.json()
        types = data['results']

        # Crear un diccionario donde la clave es el nombre del tipo y el valor es la URL
        types_dict = {type_info['name']: type_info['url'] for type_info in types}

        # Ordenar el diccionario por el nombre de los tipos
        sorted_types_dict = dict(sorted(types_dict.items()))

        types_with_path = {}

        for type_name, type_url in sorted_types_dict.items():
            # Obtener el sprite más actualizado para el tipo
            latest_sprite = get_type_sprite(type_url)

            # Agregar el tipo al diccionario con su sprite
            if latest_sprite is not None:
                types_with_path[type_name] = {
                    'url': type_url,
                    'sprite': latest_sprite
                }
        
        return types_with_path

    # En caso de error en la solicitud
    return jsonify({'error': 'Could not fetch types from API'}), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    search_result = None
    regions = get_regions()
    types=get_types()

    print(types)

    if request.method == 'POST':
        pokemon_name = request.form['pokemon_name']
        search_result = get_pokemon_data(pokemon_name)

    return render_template('index.html', search_result=search_result, regions=regions, types=types)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')    

@app.route('/region/<region_name>')
def region(region_name):
    region_details = get_region_details(region_name)
    return render_template('region.html', region=region_details)

if __name__ == '__main__':
    app.run(debug=True)