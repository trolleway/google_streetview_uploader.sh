#!/bin/bash

# batch make image darker in ImageMagick (like using Cruves)

mkdir correction


for file in *.JPG
 do
 echo $file
  convert $file -level 0%,100%,0.35 -format jpg correction/$file
 cp $file /home/trolleway/2g/$file

done
