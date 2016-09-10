<?php
include_once( "config.php" );

function image_overlap( $background, $foreground )
{
	$imageWidth = imagesx($background);
	$imageHeight = imagesy($background);
	$insertWidth = imagesx($foreground);
	$insertHeight = imagesy($foreground);

	$overlapX = $imageWidth/2-($insertWidth/2);
	$overlapY = 5;

	imagecolortransparent($foreground, imagecolorat($foreground,0,0));               
	imagecopymerge($background,$foreground, $overlapX,$overlapY,0,0,$insertWidth,$insertHeight,100);   

	return $background;
}

header("Content-type: image/png");
$im = imagecreatetruecolor( 300, 300 );
$insert = imagecreatefrompng("WC-logo.png");
imagecopy( $im, $insert, 75, 0, 0, 0, 150, 150 );

$grey = imagecolorallocate( $im, 38, 38, 38 );
$white = imagecolorallocate( $im, 255, 255, 255 );
$black = imagecolorallocate( $im, 0, 0, 0 );
$grey = imagecolorallocate( $im, 18, 18, 18 );
$red = imagecolorallocate( $im, 255, 0, 0 );

//imagefilledrectangle( $im, 0, 0, 300, 300, $black );
$x1 = 50;
$y1 = 275;
$x2 = $x1+1; 
$y2 = 0;

$maxQuery = "select max( id ) from playerTrend";
$maxResult = mysql_query( $maxQuery ) or $logger->error( mysql_error() );
list( $max ) = mysql_fetch_row( $maxResult );
$window = $max-100;

$trendQuery = "select timestamp, playerCount from playerTrend where id >= $window order by timestamp limit 100"; 
$trendResult = mysql_query( $trendQuery );
while( list( $t, $D ) = mysql_fetch_row( $trendResult ) ) 
{
	imagefilledrectangle( $im, $x1, $y1, $x2, $y1-$D, $red );
	$x1 = $x2+1;
	$x2 = $x1+1;
}

imagestring( $im, 1, 25, 272, "0 -", $white );
imagestring( $im, 1, 20, 262, "10 -", $white );
imagestring( $im, 1, 20, 252, "20 -", $white );
imagestring( $im, 1, 20, 242, "30 -", $white );
imagestring( $im, 1, 20, 232, "40 -", $white );
imagestring( $im, 1, 20, 222, "50 -", $white );
imagestring( $im, 1, 20, 212, "60 -", $white );
imagestring( $im, 1, 20, 202, "70 -", $white );
imagestring( $im, 1, 20, 192, "80 -", $white );
imagestring( $im, 1, 20, 182, "90 -", $white );
imagestring( $im, 1, 15, 172, "100 -", $white );
imagestring( $im, 1, 15, 162, "110 -", $white );
imagestring( $im, 1, 15, 152, "120 -", $white );
imagestring( $im, 1, 15, 142, "130 -", $white );
imagestring( $im, 1, 15, 132, "140 -", $white );
imagestring( $im, 1, 50, 285, "players over the last 8 hours", $white );

imagepng( $im );
imagedestroy( $im );

$logger->debug( "$caller_short __END__" );
?>
