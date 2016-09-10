#!/bin/sh
#
# this is a re-write of a leeched script from Doug Jennewein (http://www.usd.edu/~djennewe)
#

HOME=/shared
MOGRIFY=/usr/X11R6/bin/mogrify
JPEG_DIR=$HOME/www/photos/jpgs
THUMB_DIR=$HOME/www/photos/thumbs

cp $JPEG_DIR/*.JPG $THUMB_DIR
cd $THUMB_DIR
$MOGRIFY -scale 80x100 $THUMB_DIR/*.JPG

