#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

Upload a folder of spherical photos to Google Street View using Street View Publish API

Uвage: python run_plain.py  
'''

import os, sys
from google.proto.streetview.publish.v1 import resources_pb2
from google.streetview.publish.v1 import street_view_publish_service_client as client
import google.oauth2.credentials
#from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow


import requests
import time
import glob

from tqdm import tqdm

class Streetview_uploader():
        
    def get_list_photos(self):
        url = 'https://streetviewpublish.googleapis.com/v1/photos'
        params = {'key':API_KEY, 'pageSize':10}
        headers = {'authorization': 'Bearer {YOUR_ACCESS_TOKEN}'.format(YOUR_ACCESS_TOKEN=access_token)}
        print url
        print headers
        r = requests.get(url,  headers=headers, params = params)
        print r.json()

    def get_access_token(self):

        CLIENT_SECRETS_FILE = None
        mask = 'client_secret*.json'
        for CLIENT_SECRETS_FILE in glob.glob(mask):
            pass
        
        if CLIENT_SECRETS_FILE is None:
            print 'Please obtain client_secret.json from Google API Console, and save it into ' + os.path.dirname(os.path.realpath(__file__))
            print 'It will be searched in this folder with mask: ' + mask
            quit()


      
        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                 scope='https://www.googleapis.com/auth/streetviewpublish',
                                 redirect_uri='http://example.com/auth_return') 
        storage = Storage('creds.data')
        # Open a web browser to ask the user for credentials.
        credentials = run_flow(flow, storage)
        assert credentials.access_token is not None
        return credentials.access_token    


    def upload(self,path):
        
        token = self.get_access_token()
        credentials = google.oauth2.credentials.Credentials(token)   
        #path = 'g:/Madv360/Madv360v2/2018-07-28_lefortovo/pack7/'
        #path = 'g:/Madv360/Madv360v2/2018-07-19_Sakhalin/'
        files = list()
        for dirpath, dnames, fnames in os.walk(path):
            for f in fnames:
                if f.upper().endswith(".JPG"):
                    files.append(os.path.join(dirpath, f))

        print 'Upload all JPG files from '+path
        pbar = tqdm(total=len(files))
        for infile in files:
            pbar.set_description(os.path.basename(infile))
            pbar.update(1)
            #print infile
            if 1 != 2:
                try:
                    filename = infile              
                    path = os.path.normpath(filename)

                    # Create a client and request an Upload URL.
                    streetview_client = client.StreetViewPublishServiceClient(credentials=credentials)
                    upload_ref = streetview_client.start_upload()
                    #print("Created upload url: " + str(upload_ref))

                    # Upload the photo bytes to the Upload URL.
                    with open(path, "rb") as f:
                      #print("Uploading file: " + f.name)
                      raw_data = f.read()
                      headers = {
                          "Authorization": "Bearer " + token,
                          "Content-Type": "image/jpeg",
                          "X-Goog-Upload-Protocol": "raw",
                          "X-Goog-Upload-Content-Length": str(len(raw_data)),
                      }
                      r = requests.post(upload_ref.upload_url, data=raw_data, headers=headers)
                      if r.status_code <> 200:
                          print("Upload response: " + str(r))

                    # Upload the metadata of the photo.
                    photo = resources_pb2.Photo()
                    photo.upload_reference.upload_url = upload_ref.upload_url
                    #from API refrence:
                    #Currently, the only way to set heading, pitch, and roll in photo.create is through the Photo Sphere XMP metadata in the photo bytes.
                    create_photo_response = streetview_client.create_photo(photo)
                    #print("Create photo response: " + str(create_photo_response))
                   

                except IOError:
                    print "IOError for", infile    
        pbar.close()

if __name__ == '__main__':
    main()    