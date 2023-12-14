import json
import os

searches = [
    'Swamp Titan [Lv1]', 'Swamp Titan [Lv2]',
    'Badlands Titan [Lv1]', 'Badlands Titan [Lv2]',
    'Grasslands Titan [Lv1]', 'Grasslands Titan [Lv2]',
    'Grassland Altar [Lv1]', 'Grassland Altar [Lv2]', 'Grassland Altar [Lv3]', 'Grassland Altar [Lv4]',
    'Badlands Altar [Lv1]', 'Badlands Altar [Lv2]', 'Badlands Altar [Lv3]', 'Badlands Altar [Lv4]',
    'Swamp Altar [Lv1]', 'Swamp Altar [Lv2]', 'Swamp Altar [Lv3]', 'Swamp Altar [Lv4]',

]


def search_tiles():
    results = {}

    for name in os.listdir('Titans'):
        os.remove(f'Titans/{name}')

    with open('tiles.json', 'r') as f:
        tiles = json.load(f)
        
        for search in searches:
            for tile in tiles:
                if tile['name'] == search:
                    if search in results:
                        results[search].append(tile)
                    else:
                        results[search] = [tile]
    
    for search in searches:
        if search in results:
            name = search.replace('[', '').replace(']', '').replace(' ', '')
            with open("Titans/" + name + ".txt", 'w') as f:
                if search in results:
                    for titan in results[search]:
                         f.write(f"{titan['x']}, {titan['y']} - {titan['name']}\n")

search_tiles()
