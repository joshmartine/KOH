import requests
import json
import time
import headers

lower_bound = 1868
upper_bound = 6317
step = 20

def collect_tiles():
    data = {
        'segment_ids': [i for i in range(lower_bound, lower_bound+step)]
    }

    tiles = []
    for i in range(0, upper_bound - lower_bound + 1, step):
        req = requests.post(
            'https://api.kingdomsofheckfire.com/game/nonessential/poll_segments_realm_state', headers=headers.HEADERS, data=data)
        json_data = req.json()
        try:
            sites = json_data['world_state']['sites']
            for tile in sites:
                tiles.append(sites[tile])
            data['segment_ids'] = [d + step for d in data['segment_ids']]
            if i % (10 * step) == 0:
                time.sleep(2)
        except Exception as e:
            print('Map error:', e, '\nDumping file..')

    with open('tiles.json', 'w') as f:
        f.write(json.dumps(tiles, indent=4))

