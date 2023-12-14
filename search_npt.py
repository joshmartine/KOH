import sys
import argparse
import json

def search_npt():
    parser = argparse.ArgumentParser(description="calculate X to the power of Y")    
    parser.add_argument("name", help="description")
    parser.add_argument("--level", help="description")
    args = parser.parse_args()

    with open('tiles.json', 'r') as f:
        tiles = json.load(f)
        results = []
        for tile in tiles:
            if args.name.lower() in tile['name'].lower():
                if args.level:
                    if args.level in tile['name']:
                        results.append(tile)
                else:
                    results.append(tile)

    for result in results:
        print(f"{result['x']}, {result['y']} - {result['name']}")


search_npt()
