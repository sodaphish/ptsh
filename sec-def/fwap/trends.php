<?php
/*
 * trends.php v.0.2.0 by C.J. Steele <csteele@good-sam.com>
 *    8 Jul 2003
 * 
 * This script is responsible for determining trneds of port blockings.  The hope is 
 * that by identifying trends, we will better be able to determine security measures.
 * 
 */
?>

<html>
<head>
	<title>F.W.A.P. Trends</title>

<script language=javascript>
<!--
function popupwindow( fileloc, winname, winwidth, winheight ) 
{ 
	windowbits = "height=" + winheight + ",width=" + winwidth + ",channelmode=0,dependent=0,directories=0,fullscreen=0,location=0,menubar=0,resizable=0,scrollbars=1,statusbar=0,toolbar=0"
	window.open( fileloc, winname, windowbits )
}
-->
</script>

<style>
h1 { font-family: Verdana, Helvetica, Arial, sans-serif; font-size: 18px; weight: bold }
h2 { font-family: Verdana, Helvetica, Arial, sans-serif; font-size: 14px; weight: bold }
h3 { font-family: Verdana, Helvetica, Arial, sans-serif; font-size: 12px; weight: bold }
h4 { font-family: Verdana, Helvetica, Arial, sans-serif; font-size: 10px; weight: bold }
td,th,p,b,i,font,a,li,ol { font-family: Verdana, Helvetica, Arial, sans-serif; font-size: 10px }
</style>

</head>
<body>

<font>

<?php

function yesterday(){
	//86400 seconds per day
	$yest = date( "M d Y", time()-86400 );
	return $yest; 
}

function getmicrotime(){ 
    list($usec, $sec) = explode(" ",microtime()); 
    return ( ( (float)$usec/1000 ) + (float)$sec);
} 

$start_time = getmicrotime();

$link = mysql_connect( "localhost", "root", "" );
mysql_select_db( "fw" );

$date = date( "G:i:sO d M Y" );
if( $q == "internal" or $q == "both" )
{
	print "<h2>Internal Attack Trends</h2> <p>as of $date</p>"; 

	// get sum of all reported blocks NOT ORIGINATING FROM THE INSIDE
	$R_q = "select count( dstprt ) from blocked where src like '172.%'"; 
	$R_r = mysql_query( $R_q );
	list( $R ) = mysql_fetch_row( $R_r ); 

	// get sum all all RECENT reported blocks NOT ORIGINATING FROM THE INSIDE
	$yesterday = date( "M d Y", time() - 86400 ); 
	$daybeforelast = date( "M d Y", time() - 172800 ); 
	$r_q = "select count( dstprt ) from blocked where src like '172.%' and ( date like '$yesterday' or date like '$daybeforelast' )"; 
	$r_r = mysql_query( $r_q );
	list( $r ) = mysql_fetch_row( $r_r ); 
	
	// calculate scale ( s=R/r );
	$scale = $R/$r; 
	
	// process trend for each of top 20 blocked ports
	$topblocks_q = "select distinct dstprt, count(dstprt) as blockct, proto from blocked where src like '172.%' group by dstprt order by blockct desc limit 20"; 
	$topblocks_r = mysql_query( $topblocks_q );

	while( list( $port, $count, $proto ) = mysql_fetch_row( $topblocks_r ) )
	{
		// calculate r_p
		$rp_q = "select count( dstprt ) from blocked where dstprt='$port' and src like '172.%' and ( date like '$yesterday' or date like '$daybeforelast' )"; 
		$rp_r = mysql_query( $rp_q ); 
		list( $rp ) = mysql_fetch_row( $rp_r ); 
	
		// calculate R_p
		$Rp_q = "select count( dstprt ) from blocked where dstprt='$port' and src like '172.%'"; 
		$Rp_r = mysql_query( $Rp_q );
		list( $Rp ) = mysql_fetch_row( $Rp_r ); 
				
		// calculate trend
		$trend = log( ($rp/$Rp) * $scale ); 
	
		// calculate trenderr
		error_reporting( 1 );  // disable display of divide-by-zero warnings
		$trenderr = sqrt( ($scale/$rp) + ($scale/$Rp) ); 
	
		$service_guess = getservbyport ( $port, $proto ); 
	
		if( ( $trend -1 > 0 ) )
		{
			print "<img src=images/red_arrow.gif width=11 height=12> $port/$proto "; 
			if( $service_guess ){ print "($service_guess)"; } else { print "(???)"; }
			print " - $rp in last 2 days v. $Rp lifetime<br>\n";
		} else if( ( $trend + 1 < 0 ) ){
			print "<img src=images/green_arrow.gif width=11 height=12> $port/$proto ";
			if( $service_guess ){ print "($service_guess)"; } else { print "(???)"; }
			print " - $rp in last 2 days v. $Rp lifetime<br>\n";
		} else {
			print "<img src=images/black_arrow.gif width=11 height=12> $port/$proto ";
			if( $service_guess ){ print "($service_guess)"; } else { print "(???)"; }
			print " - $rp in last 2 days v. $Rp lifetime<br>\n";
		}
	
	} #end while

} #end initial if 

if( $q == "external" or $q == "both" ) {
	
	print "<h2>External Attack Trends</h2> <p>as of $date</p>"; 

	// get sum of all reported blocks NOT ORIGINATING FROM THE INSIDE
	$R_q = "select count( dstprt ) from blocked where src not like '172.%'"; 
	$R_r = mysql_query( $R_q );
	list( $R ) = mysql_fetch_row( $R_r ); 
	
	// get sum all all RECENT reported blocks NOT ORIGINATING FROM THE INSIDE
	$yesterday = date( "M d Y", time() - 86400 ); 
	$daybeforelast = date( "M d Y", time() - 172800 ); 
	$r_q = "select count( dstprt ) from blocked where src not like '172.%' and ( date like '$yesterday' or date like '$daybeforelast' )"; 
	$r_r = mysql_query( $r_q );
	list( $r ) = mysql_fetch_row( $r_r ); 
	
	// calculate scale ( s=R/r );
	$scale = $R/$r; 
	
	// process trend for each of top 20 blocked ports
	$topblocks_q = "select distinct dstprt, count(dstprt) as blockct, proto from blocked where src not like '172.%' group by dstprt order by blockct desc limit 20"; 
	$topblocks_r = mysql_query( $topblocks_q );

	while( list( $port, $count, $proto ) = mysql_fetch_row( $topblocks_r ) )
	{

		// calculate r_p
		$rp_q = "select count( dstprt ) from blocked where dstprt='$port' and src not like '172.%' and ( date like '$yesterday' or date like '$daybeforelast' )"; 
		$rp_r = mysql_query( $rp_q ); 
		list( $rp ) = mysql_fetch_row( $rp_r ); 
	
		// calculate R_p
		$Rp_q = "select count( dstprt ) from blocked where dstprt='$port' and src not like '172.%'"; 
		$Rp_r = mysql_query( $Rp_q );
		list( $Rp ) = mysql_fetch_row( $Rp_r ); 
				
		// calculate trend
		$trend = log( ($rp/$Rp) * $scale ); 
	
		// calculate trenderr
		error_reporting( 1 );  // disable display of divide-by-zero warnings
		$trenderr = sqrt( ($scale/$rp) + ($scale/$Rp) ); 
	
		$service_guess = getservbyport ( $port, $proto ); 
	
		if( ( $trend -1 > 0 ) )
		{
			print "<img src=images/red_arrow.gif width=11 height=12> $port/$proto "; 
			if( $service_guess ){ print "($service_guess)"; } else { print "(???)"; }
			print " - $rp in last 2 days v. $Rp lifetime<br>\n";
		} else if( ( $trend + 1 < 0 ) ){
			print "<img src=images/green_arrow.gif width=11 height=12> $port/$proto ";
			if( $service_guess ){ print "($service_guess)"; } else { print "(???)"; }
			print " - $rp in last 2 days v. $Rp lifetime<br>\n";
		} else {
			print "<img src=images/black_arrow.gif width=11 height=12> $port/$proto ";
			if( $service_guess ){ print "($service_guess)"; } else { print "(???)"; }
			print " - $rp in last 2 days v. $Rp lifetime<br>\n";
		}
	
	} #end while

} // end if to determine internal or external trending request

$end_time = getmicrotime();

$time = $end_time - $start_time; 
print "<br><i>time to execute: </i> $time<br>\n";

?>

</font>

</body>
</html>
