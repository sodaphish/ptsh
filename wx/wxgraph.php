<?php
/*
 * wxgraph.php by C.J. Steele <coreyjsteele@gmail.com>
 * 
 * draw a graph of the wind strength over time.  use it in conjunction 
 * with the wxpoll.py, which will gather the data that fills the 
 * database which this script reads.
 * 
 * graph weather from -30F - 100F
 * 
 * the observation table contains the following: 
 * date, station, temp, dewpoint, humidity, pressure, windir, windspd 
 * select * from observation order by rowid asc limit 10;
 * 
 */
header( "Content-type: image/png" );

$graph = $_GET["g"];

$im = @imagecreate( 360, 280 );
$white  = imagecolorallocate( $im, 255, 255, 255 );
$black  = imagecolorallocate( $im, 0, 0, 0 );
$red = imagecolorallocate( $im, 255, 0, 0 );
$blue = imagecolorallocate( $im, 0, 0, 255 );
$red32  = imagecolorallocate( $im, 32, 0, 0 );
$red64 = imagecolorallocate( $im, 64, 0, 0 );
$red128 = imagecolorallocate( $im, 128, 0, 0 );
imagefill( $im, 0, 0, $white );

switch( $graph ){
case 'temp': 

/*
	if( $db = sqlite_open( "/home3/hostedby/public_html/mine/files/wx.db", 0666, $sqlite_errorstring ) )
	{
		$max_temp_query = "select max(temp) from observation order by rowid asc limit 12";
		$max_hum_query = "select max(humidity) from observation order by rowid asc limit 12";
		$set_query = "select date, temp , humidity from observation order by rowid asc limit 12";
		$result = sqlite_query( $db, $set_query ); 
		while( list( $date, $temp, $humidity ) = sqlite_fetch_row( $result ) )
		{
			# _||||||||_########__
			# 12345678901234567890
			# x+1, 220 - X+6, 220 - temp * 2
		} #end while
	} else {
		die( $sqlite_errorstring );
	} #end if
*/

	imagestring( $im, 10, 5, 5, 'Temperature/Humidity (12-Hour)', $blue );
	imageline( $im, 40, 280, 40, 25, $black ); # vertical line
	imageline( $im, 40, 220, 295, 220, $black ); # 0F line
	for( $x = 30; $x <= 280; $x += 10 )
	{
		imageline( $im, 35, $x, 40, $x, $black );
	}
	unset( $x );
	$temp = 90;
	for( $x = 32; $x <= 252; $x += 20 )
	{
		if( $temp > 0 )
		{
				imagestring( $im, 6, 10, $x, sprintf( '%2dF', $temp ), $black );
		} elseif( $temp == 0 ){
			imagestring( $im, 6, 10, $x, sprintf( ' %dF', $temp ), $black );
		} else {
			imagestring( $im, 6, 1, $x, sprintf( '%dF', $temp), $black );
		}
		$temp -= 10;
	} 
	unset( $x );
	break;

case 'pres':
	imagestring( $im, 10, 5, 5, 'Atmospheric Pressure (12-Hour)', $blue );
	break;
} #end switch 

imagepng( $im );
imagedestroy( $im );


?>
