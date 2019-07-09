USERNAME="trolleway"
mapillary_tools process --advanced --import_path "$PWD" --user_name $USERNAME --cutoff_distance 100 --cutoff_time 60 --interpolate_directions --offset_angle 180 --rerun --overwrite_EXIF_direction_tag

for file in "$PWD"
do
  exiftool -overwrite_original -quiet -ProjectionType="equirectangular" -UsePanoramaViewer="True" -"PoseHeadingDegrees<$exif:GPSImgDirection" -"CroppedAreaImageWidthPixels<$ImageWidth" -"CroppedAreaImageHeightPixels<$ImageHeight" -"FullPanoWidthPixels<$ImageWidth" -"FullPanoHeightPixels<$ImageHeight" -CroppedAreaLeftPixels="0" -CroppedAreaTopPixels="0" "$file"
done

mapillary_tools upload --import_path "$PWD" --skip_subfolders --number_threads 5 --max_attempts 10 --advanced
