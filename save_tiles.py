import dropbox
import os

access = 'yXZgFTkRrCAAAAAAAAAADgi0STFrMwvOyvpLqAu9l-vXyJNs_4bEttRpwbxcK9eo'

def save_tiles():
    dbx = dropbox.Dropbox(access)
    try:
        dbx.files_delete_v2('/Titans')
    except Exception as e:
         print(e)
         pass

    for obj in os.listdir('Titans/'):
        with open(f'Titans/{obj}', 'rb') as f:
            dbx.files_upload(f.read(), f'/Titans/{obj}', mode=dropbox.files.WriteMode.overwrite)

