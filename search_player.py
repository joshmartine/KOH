import sys
import argparse
import json

def search_player():
    parser = argparse.ArgumentParser(description="calculate X to the power of Y")    
    parser.add_argument("level_low", type=int, help="description")
    parser.add_argument("level_high", type=int, help="description")
    parser.add_argument("power_low", type=float, help="description")
    parser.add_argument("power_high", type=float, help="description")
    args = parser.parse_args()

    with open('tiles.json', 'r') as f:
        tiles = json.load(f)
        results = []
        for tile in tiles:
            if args.level_low <= tile['level'] <= args.level_high and args.power_low * 1e6 <= tile['size'] <= args.power_high * 1e6:
                results.append(tile)

    for result in results:
        print(f"{result['x']}, {result['y']} - {result['level']} {result['name']} - {round(result['size']/ 1e6)} mil")


search_player()
