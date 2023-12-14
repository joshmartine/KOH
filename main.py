from collect_tiles import collect_tiles
from search_tiles import search_tiles
from save_tiles import save_tiles

while True:
    collect_tiles()
    print('Searching')
    search_tiles()
    print('Uploading')
    save_tiles()
    print('done')
