# Google-Drive-Sync-App
An app that syncs a folder on google drive with a local folder on the system. 
Sync is one-way, from local folder to the sync folder on google drive(Keeping in mind the limited storage on google drive). 
Lets you sync (adds new file in local folder to google drive folder and deletes the file from google drive folder 
that are not present in local folder anymore at once)any number of file and any format file from local folder 
to google drive on a click of a button.

Used Google Drive APIs. Language used to code is Python. 

2 files needed to run the app(personal credentials.json file for authentication that can be downloaded when you enable the Google Drive API and a toke.pickle file which gets autogenerated for staying authenticated after the first time) and the script needed to be converted into a executable to be used as an app ( used PyInstaller /* another option is py2exe*/) otherwise could be run in any Python Editor / IDE.

@kar7ik
