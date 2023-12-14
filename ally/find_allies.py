import requests
import json
import argparse
import time
import config
def find_allies():
    parser = argparse.ArgumentParser(description="find allies")    
    parser.add_argument("price_low", type=float, help="description")
    parser.add_argument("price_high", type=float, help="description")
    parser.add_argument("--g", type=float, help="min grass")
    parser.add_argument("--b", type=float, help="min bad")
    parser.add_argument("--s", type=float, help="min swamp")
    parser.add_argument("--sort", help="sorting method")
    parser.add_argument("--mins", type=int, help="Max run time")
    args = parser.parse_args()

    args.price_low = int(args.price_low * 1e6)
    args.price_high = int(args.price_high * 1e6)

    if args.price_low > args.price_high:
        print('Note: swapping price_low and price_high')
        args.price_low, args.price_high = args.price_high, args.price_low
    max_iters = args.mins if args.mins else 30
    total_iters = 0
    iters = 0
    data = {
        'max_cost': int(args.price_high),
        'offset': 0
    }
    allies = []
    grassland = 'biome3_attack_multiplier'
    badland = 'biome4_attack_multiplier'  
    swamp = 'biome5_attack_multiplier'
    ally_file = open("allies.txt")
    while data['max_cost'] > args.price_low and total_iters < max_iters:
        req = requests.post('https://api.kingdomsofheckfire.com/game/ally/search_allies/', headers=config.headers, data=data)
        res = req.json()
        ally_data = res['allies']
        
        for ally in ally_data:
            ally[grassland] /= 100
            ally[badland] /= 100
            ally[swamp] /= 100
            allies.append(ally)

            ally_file.write(json.dumps(ally))
            ally_file.write(",\n")
        if len(ally_data) == 0:
            data['max_cost'] = data['max_cost'] - 1
            data['offset'] = 0
        elif data['max_cost'] == ally_data[-1]['cost']:
            data['offset'] += len(res)          
            if data['offset'] >= 500:
                data['max_cost'] = ally_data[-1]['cost'] - 1  
        else:
            data['max_cost'] = ally_data[-1]['cost'] - 1
            data['offset'] = 0
        
        iters += 1
        print(f'Cost percent: {ally_data[-1]["cost"] / data["max_cost"]}%, Iterations percent: {round(100*(iters/20)/max_iters,1)}%', end='\r')
        if iters % 20 == 0:
            total_iters += 1
            if total_iters == max_iters:
                break
            time.sleep(60)

    g = args.g if args.g else 0
    b = args.b if args.b else 0
    s = args.s if args.s else 0

    meet_requirements = []            

    while len(meet_requirements) == 0:
        for ally in allies:
            if ally[grassland] >= g and ally[badland] >= b and ally[swamp] >= s:
                ally['total'] = ally[grassland] + ally[badland] + ally[swamp]
                ally['best_value'] = ally['total'] / ally['cost'] * 1e7
                meet_requirements.append(ally)
        g *= .9
        b *= .9
        s *= .9

    sort = args.sort if args.sort else 'clydes_method'

    biome = {
        'g': grassland,
        'b': badland,
        's': swamp,
        'grass': grassland,
        'bad': badland,
        'swamp': swamp,
        'grasslands': grassland,
        'badlands': badland,
        'swamplands': swamp,
        'grassland': grassland,
        'badland': badland,
        'swampland': swamp,
    }
    allies = []
    if sort == 'clydes_method':
        allies = sorted(meet_requirements, key=lambda i:i['best_value'], reverse=True)
    elif sort == 't':
        allies = sorted(meet_requirements, key=lambda i:i['total'], reverse=True)  
    else:
        allies = sorted(meet_requirements, key=lambda i:i[biome[sort]], reverse=True)

    for ally in allies:
        print(f'{ally[grassland]}/{ally[badland]}/{ally[swamp]} - {ally["username"]} - {round(ally["cost"]/1e6,2)} mil')


find_allies()
