# SVG2PNG Folder

This folder contains PNG versions of all SVG files in this repo.
It is used for SEO, as most sites do not like SVGs as images and prefer rasterized
versions of images (like PNGs).

The script to run this conversion can be found as `svg2png.py` in the root folder.
It is run every so often to convert all SVGs to PNGs. Since it can be hard to 
install inkscape, as a contributor you do not need to do anything.

_Why is this not done on netlify?_
I have not found a way to install inkscape on netlify, and it would make builds
a lot slower. This folder is only about 1mb in size anyway, so not a big problem either.
