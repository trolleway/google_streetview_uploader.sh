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
import glob,sys

 

from gooey import Gooey, GooeyParser    



arguments_parser = GooeyParser( description='Upload a folder with spherical panoramas to Google Street View Publish API')
arguments_parser.add_argument(
        "path", metavar = "path", help="Path to folder", widget="DirChooser")

def get_access_token():

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

@Gooey(dump_build_config=True, program_name="google-streetview-upload", progress_regex=r"\w*progress: (\d+)%$")
def main():

    args = arguments_parser.parse_args() 
    path = args.path
    sys.argv = [sys.argv[0]]
    
    token = get_access_token()
    credentials = google.oauth2.credentials.Credentials(token)   
    #path = 'g:/Madv360/Madv360v2/2018-07-19_Sakhalin/'
    files = list()

    for dirpath, dnames, fnames in os.walk(path):
        for f in fnames:
            if f.upper().endswith(".JPG"):
                files.append(os.path.join(dirpath, f))

    print 'Upload all JPG files from '+path
    i = 0
    for infile in files:
        i = i + 1
        print(os.path.basename(infile) + " progress: {}%".format( str(100 / len(files) * i  )))
        sys.stdout.flush()
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

if __name__ == '__main__':
    main()    