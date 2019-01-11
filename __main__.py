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
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run_flow


import requests
import time

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]
        
    return None
    
def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon_direction(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None
    direction = None

    if "GPSInfo" in exif_data:      
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')


        PoseHeadingDegrees = _get_if_exist(gps_info, 'GPano:PoseHeadingDegrees')
        GPSImgDirection = _get_if_exist(gps_info, 'GPSImgDirection')
        if PoseHeadingDegrees is None:
            if GPSImgDirection is None:
                direction = 0
            else:
                direction = GPSImgDirection[0]
        else:
            direction = PoseHeadingDegrees

        
        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon
                
    else:
        print exif_data
        assert "GPSInfo" in exif_data

    return lat, lon, direction



    


def get_list_photos():
    url = 'https://streetviewpublish.googleapis.com/v1/photos'
    params = {'key':API_KEY, 'pageSize':10}
    headers = {'authorization': 'Bearer {YOUR_ACCESS_TOKEN}'.format(YOUR_ACCESS_TOKEN=access_token)}
    print url
    print headers
    r = requests.get(url,  headers=headers, params = params)
    print r.json()

def get_access_token():
  client_id = ''
  client_secret = ''

  flow = OAuth2WebServerFlow(client_id=client_id,
                             client_secret=client_secret,
                             scope='https://www.googleapis.com/auth/streetviewpublish',
                             redirect_uri='http://example.com/auth_return')
  storage = Storage('creds.data')
  # Open a web browser to ask the user for credentials.
  credentials = run_flow(flow, storage)
  assert credentials.access_token is not None
  return credentials.access_token    

if __name__ == '__main__':

    token = get_access_token()
    credentials = google.oauth2.credentials.Credentials(token)   
    
    
    

    path = 'g:/Madv360/Madv360v2/2018-07-28_lefortovo/pack1/'
    files = list()
    for dirpath, dnames, fnames in os.walk(path):
        for f in fnames:
            if f.upper().endswith(".JPG"):
                files.append(os.path.join(dirpath, f))


    for infile in files:
        print infile
        if 1 != 2:
            try:
                filename = infile
                image = Image.open(filename)
                exif_data = get_exif_data(image)
                lat, lon, direction = get_lat_lon_direction(exif_data)
                if direction is None:
                    direction = 1

                print lat, lon, direction
                
                path = os.path.normpath(filename)
                heading = direction

                # Create a client and request an Upload URL.
                streetview_client = client.StreetViewPublishServiceClient(credentials=credentials)
                upload_ref = streetview_client.start_upload()
                print("Created upload url: " + str(upload_ref))

                # Upload the photo bytes to the Upload URL.
                with open(path, "rb") as f:
                  print("Uploading file: " + f.name)
                  raw_data = f.read()
                  headers = {
                      "Authorization": "Bearer " + token,
                      "Content-Type": "image/jpeg",
                      "X-Goog-Upload-Protocol": "raw",
                      "X-Goog-Upload-Content-Length": str(len(raw_data)),
                  }
                  r = requests.post(upload_ref.upload_url, data=raw_data, headers=headers)
                  print("Upload response: " + str(r))

                # Upload the metadata of the photo.
                photo = resources_pb2.Photo()
                photo.upload_reference.upload_url = upload_ref.upload_url
                photo.capture_time.seconds = int(time.time())
                photo.pose.heading = heading
                photo.pose.lat_lng_pair.latitude = lat
                photo.pose.lat_lng_pair.longitude = lon
                create_photo_response = streetview_client.create_photo(photo)
                print("Create photo response: " + str(create_photo_response))
               

            except IOError:
                print "cannot create thumbnail for", infile    
