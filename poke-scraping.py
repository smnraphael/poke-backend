import os
import json
import requests

def get_pokemon_info(limit=386):
    all_pokemon_info = []
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        for pokemon in data['results']:
            pokemon_data = requests.get(pokemon['url']).json()
            pokemon_info = {
                "id": pokemon_data['id'],
                "name": pokemon_data['species']['name'],
                "image": pokemon_data['sprites']['other']['official-artwork']['front_default'],
                "generation": get_generation(pokemon_data['id']),
                "type": [t['type']['name'] for t in pokemon_data['types']],
                "height": pokemon_data['height'],
                "weight": pokemon_data['weight']
                }
            all_pokemon_info.append(pokemon_info)
        return {"pokemons": all_pokemon_info, "favorite": [], "teams": []}
    else:
        print("Failed to fetch data from", url)
        return None

def get_generation(pokemon_id):
    if 1 <= pokemon_id <= 151:
        return "i"
    elif 152 <= pokemon_id <= 251:
        return "ii"
    elif 252 <= pokemon_id <= 386:
        return "iii"
    else:
        return "Unknown"

def save_to_json(data, filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    pokemon_info = get_pokemon_info()
    if pokemon_info:
        save_to_json(pokemon_info, "db.json")
        print("JSON file successfully generated.")
    else:
        print("Failed to generate JSON file.")
