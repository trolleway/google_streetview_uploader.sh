#!/usr/bin/env python
# -*- coding: utf-8 -*-


from gooey import Gooey, GooeyParser    

import streetview_upload_module
import sys


arguments_parser = GooeyParser( description='Upload a folder with spherical panoramas to Google Street View Publish API')
arguments_parser.add_argument(
        "path", metavar = "path", help="Path to folder", widget="DirChooser")
        
        
@Gooey(dump_build_config=True, program_name="google-streetview-upload", progress_regex=r"^progress: (\d+)%$")
def main():
    args = arguments_parser.parse_args() 

    sys.argv = [sys.argv[0]]

    uploader = streetview_upload_module.Streetview_uploader()
    uploader.upload(args.path)
    
    
    
if __name__ == '__main__':
    main()   