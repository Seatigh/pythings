from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

def get_pokemon_data(limit=15):
    url = f'https://pokeapi.co/api/v2/pokemon?limit={limit}'
    response = requests.get(url)
    pokemon_list = []

    if response.status_code == 200:
        data = response.json()
        for item in data['results']:
            pokemon_data = requests.get(item['url']).json()
            
            types = [t['type']['name'] for t in pokemon_data['types']]
            
            abilities = []
            for ability in pokemon_data['abilities']:
                ability_data = requests.get(ability['ability']['url']).json()
                abilities.append({
                    'name': ability['ability']['name'],
                    'is_hidden': ability['is_hidden'],
                    'description': ability_data['effect_entries'][0]['short_effect']
                })
            
            species_data = requests.get(pokemon_data['species']['url']).json()
            description = ""
            for entry in species_data['flavor_text_entries']:
                if entry['language']['name'] == 'en':
                    description = entry['flavor_text']
                    break
            
            pokemon = {
                'id': pokemon_data['id'],
                'name': pokemon_data['name'].capitalize(),
                'sprite': pokemon_data['sprites']['front_default'],
                'types': types,
                'abilities': abilities,
                'description': description,
                'height': pokemon_data['height'],
                'weight': pokemon_data['weight'],
            }
            pokemon_list.append(pokemon)

    return sorted(pokemon_list, key=lambda x: x['id'])

@app.route('/')
def index():
    today_date = datetime.now().strftime('%Y-%m-%d')
    pokemon_list = get_pokemon_data(limit=15)
    return render_template('index.html', pokemon_list=pokemon_list, today_date=today_date)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
