USERNAME="trolleway"
ANGLE="180"
#TRACK="track.gpx"

#echo 'georefrencing...'
#exiftool -quiet -quiet -overwrite_original -geotag $TRACK $(pwd)

mapillary_tools process --advanced --import_path "$PWD" --user_name $USERNAME --cutoff_distance 100 --cutoff_time 60 --interpolate_directions --offset_angle $ANGLE --rerun --overwrite_EXIF_direction_tag 2> /dev/null

for file in "$PWD"
do
  exiftool -overwrite_original -quiet -ProjectionType="equirectangular" -UsePanoramaViewer="True" -"PoseHeadingDegrees<$exif:GPSImgDirection" -"CroppedAreaImageWidthPixels<$ImageWidth" -"CroppedAreaImageHeightPixels<$ImageHeight" -"FullPanoWidthPixels<$ImageWidth" -"FullPanoHeightPixels<$ImageHeight" -CroppedAreaLeftPixels="0" -CroppedAreaTopPixels="0" "$file" mapillary_tools process --advanced --import_path "$PWD" --user_name $USERNAME --cutoff_distance 100 --cutoff_time 60 --interpolate_directions --offset_angle $ANGLE --rerun --overwrite_EXIF_direction_tag 2> /dev/null
done

mapillary_tools upload --import_path "$PWD" --skip_subfolders --number_threads 5 --max_attempts 10 --advanced
#empty line required for copy-paste
