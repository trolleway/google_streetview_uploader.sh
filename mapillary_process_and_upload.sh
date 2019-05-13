#!/bin/bash

mapillary_tools process_and_upload --advanced --import_path "$PWD" --user_name $USERNAME --rerun --overwrite_EXIF_direction_tag  --number_threads 10 --max_attempts 10
