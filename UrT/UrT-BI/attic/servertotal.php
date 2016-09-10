<?php

header("Content-type: image/png");
$im = imagecreate( 25, 15 );

$grey = imagecolorallocate( $im, 38, 38, 38 );
$white = imagecolorallocate( $im, 255, 255, 255 );
$black = imagecolorallocate( $im, 0, 0, 0 );
$grey = imagecolorallocate( $im, 18, 18, 18 );

$string = rtrim( exec( "tail -n 1 playerTrend.log | awk {'print $2'}" ) );

imagestring( $im, 2, 2, 1, $string, $white );
imagepng( $im );
imagedestroy( $im );

?>
