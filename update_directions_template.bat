c:\gis\pano_heading\mapillary_tools.exe process --advanced --import_path "%cd%" --user_name trolleway --cutoff_distance 100 --cutoff_time 60 --interpolate_directions --offset_angle 180 --rerun --overwrite_EXIF_direction_tag
%cd%

for /r %%v in (*.JPG) DO (
"c:\gis\pano_heading\exiftool.exe" -overwrite_original -quiet -ProjectionType="equirectangular" -UsePanoramaViewer="True" -"PoseHeadingDegrees<$exif:GPSImgDirection" -"CroppedAreaImageWidthPixels<$ImageWidth" -"CroppedAreaImageHeightPixels<$ImageHeight" -"FullPanoWidthPixels<$ImageWidth" -"FullPanoHeightPixels<$ImageHeight" -CroppedAreaLeftPixels="0" -CroppedAreaTopPixels="0" "%%v
)

"c:\gis\pano_heading\exiftool.exe" upload --import_path "%cd%" --skip_subfolders --number_threads 5 --max_attempts 10 --advanced
rmdir /s/q ".mapillary"

xcopy /s /y %cd% g:\2g\
