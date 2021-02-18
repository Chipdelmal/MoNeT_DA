#!/bin/bash

# argv1: Folder
# argv2: Prefix
# argv3: Extension

# echo "${1}/${2}_%03d${3}"
ffmpeg -start_number 1 -r 24 -f image2 -s 3840x2160 -i "${1}/${2}_%03d${3}" -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -preset veryslow -crf 15 -pix_fmt yuv420p "${1}/Trailer.mp4"