# google-streetview-upload
Upload a folder of spherical photos to Google Street View using Street View Publish API

# Installation

1. Clone or download repository
```
git clone https://github.com/trolleway/google-streetview-upload.git
cd google-streetview-upload
pip install -r requirements.txt
```
2. Create a project in the Google Developers Console and obtain authorization credentials so you can submit API requests. Download client secret JSON file, and save it to script folder.
For details see https://developers.google.com/streetview/publish/first-app

3. Double click at __main__.py

4. Update of authorisation keys is not implemented, so script will stop over 1 hour. You should delete uploaded files and click "Restat" button

# Update direction

For cameras withouth compass (like Xiaomi Mijia Mi 360):

1. Keep camera in one direction while shooting. Example: side with LEDs should keep backward for 180 gegrees value.
2. Set in bat file correct pathes to utilites
3. Copy .bat file to image folder and run
