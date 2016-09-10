#!/usr/bin/php -q
<?php

$total = 0;
$date = date( "U" );
$logpath = "/home/hostedby/www/mine/wc";

$db = mysql_connect( "localhost", "hostedby_soda", "alpha01" );
mysql_select_db( "hostedby_alpha" );

$q = "select serverip, serverport from servers";
$r = mysql_query( $q );

while( list( $ip, $port ) = mysql_fetch_row( $r ) )
{
	$server = "$ip:$port";
	$servertotal=`/home/hostedby/www/mine/wc/qstat -R -P -cn -tsw -q3s $server -raw ' ' | grep -v ^game | grep -v ^Q3S | wc -l`;
	$total = $total + $servertotal;
}

$fh = fopen( "$logpath/playerTrend.log", "a" ); 
fwrite( $fh, "$date $total\n" );
fclose( $fh );

?>
