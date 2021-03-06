<?php

$link = mysql_connect( "localhost", "root", "" );
mysql_select_db( "fw" );

$myname = "graphfw"; 
$myver = "0.2.0";


function get_data( $type, $date )
// return a sequential array of blocked packets matching the type
{
	$pdata = array();
	list( $m, $d, $y ) = explode( " ", $date ) ;
	$period = 0;
	$time1 = mktime( 0, 0, 0, $m, $d, $y );
	while( $time1 < mktime( 0, 0, 0, $m, $d, $y )+86399 )
	{
		$time2 = $time1+288; 
		$qt1 = date( "H:i:s", $time1 ); 
		$qt2 = date( "H:i:s", $time2 ); 
	
		$ct_q = ""; 

		switch( $type )
		{
			case "total": 
				$ct_q = "select count( id ) from blocked where date='$date' and ( time >= \"$qt1\" and time < \"$qt2\" )";
				break;
			case "int":
				$ct_q = "select count( id ) from blocked where date='$date' and src like '172.%' and ( time >= \"$qt1\" and time < \"$qt2\" )";
				break;
			case "ext":
				$ct_q = "select count( id ) from blocked where date='$date' and src not like '172.%' and ( time >= \"$qt1\" and time < \"$qt2\" )";
				break;
		}

		if( ! sizeof( $ct_q ) ){ die( "Couldn't set query!" ); }
		$ct_r = mysql_query( $ct_q ) or die( "couldn't query!" ); 
		list( $ct ) = mysql_fetch_row( $ct_r ); 
		$pdata[$period] = $ct; 
		$time1 = $time2; 
		$period++;
	} //end while

	/*
	$pdata = array(); 
	for( $a = 0; $a < 300;  $a++ )
	{
		$pdata[$a] = intval( rand( 0, 40 ) ); 
	}
	*/

	return $pdata; 
} //end get_data();


function mkgraph( $type, $date, $pdata )
{
	$pic = imagecreate( 400, 250 ); 
	$white = imagecolorallocate( $pic, 255, 255, 255 );
	$black = imagecolorallocate( $pic, 0, 0, 0 );
	$red = imagecolorallocate( $pic, 255, 0, 0 );
	$blue = imagecolorallocate( $pic, 0, 0, 255 );
	$green = imagecolorallocate( $pic, 0, 255, 0 );
	$grey = imagecolorallocate( $pic, 220, 220, 220 );

	ImageFilledRectangle( $pic, 0, 0, 400, 250, $black );
	ImageFilledRectangle( $pic, 1, 1, 398, 248, $white );
	switch( $type )
	{
		case "total":
			imagestring( $pic, 3, 7, 3, "Total Firewall Violations for $date", $blue ); 
			break;
		case "int":
			imagestring( $pic, 3, 7, 3, "Internal Firewall Violations for $date", $blue ); 
			break;
		case "ext": 
			imagestring( $pic, 3, 7, 3, "External Firewall Violations for $date", $blue ); 
			break; 
		default:
			imagestring( $pic, 3, 7, 3, "$date", $blue ); 
	}


	ImageFilledRectangle( $pic, 49, 19, 351, 196, $black );
	ImageFilledRectangle( $pic, 50, 20, 350, 195, $green );


	$maxval = 0;
	for( $i = 0; $i < sizeof( $pdata ); $i++ )
	{
		if( $pdata[$i] > $maxval )
		{
			$maxval = $pdata[$i]; 
		}
	}
	if( $maxval > 175 )
	{
		$scale = $maxval / 175; 
	} else {
		$scale = $maxval / 175; 
	}
	$x = 0;  //or whatever my offset is.
	for( $p = 0; $p <= 300; $p++ ) //sizeof( $pdata ); $p++ )
	{
		if( $pdata[$p] )
		{
			$size = 175 - intval( $pdata[$p] / $scale ); 
		} else {
			$size = 175; 
		}
		ImageFilledRectangle( $pic, $x+50, 20, $x+50, 20+$size, $white ); 
		$x++; 
	}


	// violation scale
	imagedashedline( $pic, 48, 63, 352, 63, $black ); 
	imagedashedline( $pic, 48, 107, 352, 107, $black ); 
	imagedashedline( $pic, 48, 150, 352, 150, $black ); 
	$fmtscale = sprintf( "%3.2f", $scale ); 
	imagestringup( $pic, 2, 7, 160, "violations (1:$fmtscale)", $black );
	imagestring( $pic, 2, 33, 56, "75", $black ); 
	imagestring( $pic, 2, 33, 100, "50", $black ); 
	imagestring( $pic, 2, 33, 143, "25", $black ); 


	//timeline scale
	imagestring( $pic, 2, 150, 215, "timeline", $black ); 
	//midnight
	  imageline( $pic, 50, 196, 50, 198, $black );
	  imagestring( $pic, 1, 38, 202, "00:00", $black ); 

	  imageline( $pic, 85, 196, 85, 198, $black );
	  imagestring( $pic, 1, 73, 202, "03:00", $black ); 

	  imageline( $pic, 125, 196, 125, 198, $black );
	  imagestring( $pic, 1, 113, 202, "06:00", $black ); 

	  imageline( $pic, 160, 196, 160, 198, $black );
	  imagestring( $pic, 1, 148, 202, "09:00", $black ); 

	//noon
	  imageline( $pic, 200, 196, 200, 198, $black );
	  imagestring( $pic, 1, 188, 202, "12:00", $black ); 

	  imageline( $pic, 235, 196, 235, 198, $black );
	  imagestring( $pic, 1, 223, 202, "15:00", $black ); 

	  imageline( $pic, 275, 196, 275, 198, $black );
	  imagestring( $pic, 1, 263, 202, "18:00", $black ); 

	  imageline( $pic, 310, 196, 310, 198, $black );
	  imagestring( $pic, 1, 298, 202, "21:00", $black ); 

	//midnight, again
	  imageline( $pic, 350, 196, 350, 198, $black );
	  imagestring( $pic, 1, 338, 202, "00:00", $black ); 

	global $myname, $myver;
	imagestring( $pic, 1, 300, 230, "$myname $myver", $grey ); 
	header( "content-type: image/jpeg" );
	imagejpeg( $pic ); 

} //end mkpic

if( $type and $date )
{
	$pdata = get_data( $type, $date ); 
	mkgraph( $type, $date, $pdata ); 

} else {
	print "
	<form method=post action=stats.php>
	<select name=date>
	";
	$date_q = mysql_query( "select distinct date from blocked" ); 
	while( list( $d ) = mysql_fetch_row( $date_q ) )
	{
		print "<option val=\"$d\">$d</option>\n";
	}
	print" 
	</select>

	<select name=type>
	<option value=\"total\">Total</option>
	<option value=\"int\">Internal</option>
	<option value=\"ext\">External</option>
	</select>

	<input type=submit value=\"Submit\">

	</form>
	";
}

