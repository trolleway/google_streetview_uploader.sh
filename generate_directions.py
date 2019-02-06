
import os
import argparse
import shutil
from tqdm import tqdm
import subprocess

MAPILLARY_TOOLS_PATH = u'c:\gis\pano_heading\mapillary_tools.exe'
EXIFTOOL_PATH = r'c:\gis\pano_heading\exiftool.exe'
MAPILLARY_USERNAME = u'trolleway'

parser = argparse.ArgumentParser()
parser.add_argument("folder")
parser.add_argument("angle", default = 0)
args = parser.parse_args()
FOLDER = os.path.abspath(args.folder)
ANGLE = args.angle

cmd = u'{MAPILLARY_TOOLS_PATH} process --advanced --import_path "{FOLDER}" --user_name {MAPILLARY_USERNAME} --interpolate_directions --offset_angle {ANGLE} --rerun --overwrite_EXIF_direction_tag'
cmd = cmd.format(MAPILLARY_TOOLS_PATH = MAPILLARY_TOOLS_PATH,FOLDER = FOLDER,MAPILLARY_USERNAME = MAPILLARY_USERNAME, ANGLE = str(ANGLE))

#print cmd
#os.system(cmd)

#print 'remove mapillary temporary folder'
if os.path.isdir(os.path.join(FOLDER,'.mapillary')):
    shutil.rmtree(os.path.join(FOLDER,'.mapillary'))

    
pbar = tqdm(total=len(os.listdir(FOLDER)))
    
for filename in os.listdir(FOLDER):
    image_filename = os.path.join(FOLDER, filename)
    cmd = ' "{EXIFTOOL_PATH}" -overwrite_original -quiet -ProjectionType="equirectangular" -UsePanoramaViewer="True" -"PoseHeadingDegrees<$exif:GPSImgDirection" -"CroppedAreaImageWidthPixels<$ImageWidth" -"CroppedAreaImageHeightPixels<$ImageHeight" -"FullPanoWidthPixels<$ImageWidth" -"FullPanoHeightPixels<$ImageHeight" -CroppedAreaLeftPixels="0" -CroppedAreaTopPixels="0" "{image_filename}"'
    cmd = cmd.format(EXIFTOOL_PATH = EXIFTOOL_PATH,image_filename = image_filename)
    print cmd
    os.system(cmd)
    #subprocess.Popen(cmd)
    pbar.update(1)
pbar.close()
