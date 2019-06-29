from __future__ import print_function

import os
import glob

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file as oauth2file, client, tools


SCOPES = 'https://www.googleapis.com/auth/drive'
CREDENTIAL_FILE = './client_secret_credentials.json'
TOKEN_FILE = './token.pickle'

updated_drive_filenames={}
drive_filenames = {}

def sync_folder(gdrive_folder_name):
    store = oauth2file.Storage(TOKEN_FILE)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CREDENTIAL_FILE, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))


    file_metadata = {
        'name': gdrive_folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API to check sync folder
    results = service.files().list(q="name='{name}' and mimeType='{mimeType}'"\
              .format(name=file_metadata['name'], mimeType=file_metadata['mimeType'])).execute()
    items = results.get('files', [])
    print('\n \n_______________GDrive Status of Synced Folder_______________\n')
    print('Getting the info...\n')
    if not items:
         print("'{0}' not found on GDrive, creating a new folder.\n".format(file_metadata['name'])) #create a new folder if not found on drive
         file = service.files().create(body=file_metadata,fields='id').execute()
    else:
         print("'{0}' folder on GDrive\n".format(file_metadata['name'])) #folder found and listing the files and id info
         file = items[0]

    folder_id = file.get('id')
    print("FolderId='{0}'\n".format(folder_id))



     # check files/folder with q query on gdrive
    response = service.files().list(q="'{folderId}' in parents".format(folderId=folder_id)).execute()
   
    print("Existing files in the folder:\n")
    for index,_file in enumerate(response.get('files', []),start=1):
        drive_filenames[_file.get('name')] = _file.get('id')
        print("{0}. {1}".format(index,_file['name']))

    print("\nCount: {0} files in '{1}' folder".format(len(drive_filenames),file_metadata['name']))
    print('\n __________________________________________________________\n')



    # uploading new files only
    print('\n ______________________Upload Activity______________________\n')
    os.chdir("C:/Users/kartik/Documents/DSync") #Replace the path in "" with your actual path of the local folder
    print('Inspecting the files to be uploaded from local folder...\n')
    for index,_file in enumerate(glob.glob('*.*'),start=1):

        filename = os.path.basename(_file)
        if filename not in drive_filenames:
            print("{0}. New File: {1}".format(index,filename))

            file_metadata = {
                'name': filename,
                'parents': [folder_id],
            }
            media = MediaFileUpload(_file, mimetype='application/octet-stream')
            file = service.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id,name').execute()

            print("\tUploaded: '{0}'".format(file.get('name')))
            continue

        else:

            print("{0}. Existing file on GDrive: {1}.Not uploaded!".format(index,filename))
            continue
    print('\n __________________________________________________________\n')

    # deleting files not present in local folder
    print('\n ______________________Delete Activity______________________\n')
    for index,(itemk,itemv) in enumerate(drive_filenames.items(),start=1):
        if itemk not in glob.glob('*.*'):
            print(" File deleted: {0}. '{1}'".format(index,itemk))
            service.files().delete(fileId=itemv).execute()
    print('\n __________________________________________________________\n')



    # updated files status in drive folder
    print('\n \n___________GDrive Updated Status of Synced Folder___________\n')
    print('Getting the info...\n')
    print("'{0}' folder on GDrive\n".format(file_metadata['name']))
    print("FolderId='{0}'\n".format(folder_id))
    updated_response = service.files().list(q="'{folderId}' in parents".format(folderId=folder_id)).execute()
    
    print("Updated files in the folder:\n")
    for index,_file in enumerate(updated_response.get('files', []),start=1):
        updated_drive_filenames[_file.get('name')] = _file.get('id')
        print("{0}. {1}".format(index,_file['name']))

    print("\nCount: {0} files in '{1}' folder".format(len(updated_drive_filenames),file_metadata['name']))
    
    print('\n __________________________________________________________\n')
    
    
    




if __name__ == '__main__':
    sync_folder('FromLocal_DSync')
    if len(glob.glob('*.*')) == len(updated_drive_filenames):
        print('\n************************************************************')
        print('\n \t \t \t   Synced')
        print('\n************************************************************')
    else:
        print('\n************************************************************')
        print('\n \t \t \tNot Synced')
        print('\n************************************************************')
