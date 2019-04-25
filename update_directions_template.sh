USERNAME="trolleway"

mapillary_tools process --advanced --import_path "$PWD" --user_name $USERNAME --interpolate_directions --offset_angle 180 --rerun --overwrite_EXIF_direction_tag


for file in "$PWD"
do
  "c:\gis\pano_heading\exiftool.exe" -overwrite_original -quiet -ProjectionType="equirectangular" -UsePanoramaViewer="True" -"PoseHeadingDegrees<$exif:GPSImgDirection" -"CroppedAreaImageWidthPixels<$ImageWidth" -"CroppedAreaImageHeightPixels<$ImageHeight" -"FullPanoWidthPixels<$ImageWidth" -"FullPanoHeightPixels<$ImageHeight" -CroppedAreaLeftPixels="0" -CroppedAreaTopPixels="0" $file
done
