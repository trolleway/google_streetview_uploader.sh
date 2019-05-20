# google-streetview-upload
Upload a folder of spherical photos to Google Street View using Street View Publish API

# Installation

1. Clone or download repository
```
git clone https://github.com/trolleway/google-streetview-upload.git
cd google-streetview-upload
pip install -r requirements.txt
```

2. Compile a wxpython for Ubuntu 18.04 (~20 minutes). Use TAB button for accept EULA.
```
sudo apt install make gcc libgtk-3-dev libwebkitgtk-dev libwebkitgtk-3.0-dev libgstreamer-gl1.0-0 freeglut3 freeglut3-dev python-gst-1.0 python3-gst-1.0 libglib2.0-dev ubuntu-restricted-extras libgstreamer-plugins-base1.0-dev
sudo time pip install wxpython
pip install -r requirements.txt
```

2. Create a project in the Google Developers Console and obtain authorization credentials so you can submit API requests. Download client secret JSON file, and save it to script folder.
For details see https://developers.google.com/streetview/publish/first-app

3. Double click at __main__.py

4. Update of authorisation keys is not implemented, so script will stop over 1 hour. You should click "Restat" button.

# Update direction

For cameras withouth compass (Xiaomi Mijia Mi 360):

1. Keep camera in one direction while shooting. Example: side with LEDs should keep backward for 180 gegrees value.
2. Set in bat file correct pathes to utilites
3. Copy .bat file to image folder and run, or use command from .sh file for Unix-like system
