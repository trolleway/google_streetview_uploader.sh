# google-streetview-upload
Upload a folder of spherical photos to Google Street View using Street View Publish API

# Installation

1. Clone or download repository
```
git clone https://github.com/trolleway/google_streetview_uploader.sh
cd google_streetview_uploader.sh
sudo apt install -y jq exiftool curl
```

2. Create a project in the Google Developers Console and obtain authorization credentials so you can submit API requests. Download client secret JSON file, and copy it to script folder as **client_secret.json** .
For details see https://developers.google.com/streetview/publish/first-app

Navigate to https://console.developers.google.com/apis/credentials, download client_secret.json, and put this file into script folder
3. 

```
./gsvu.sh /home/user/imagedir

```
