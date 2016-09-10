<?php
/*
 * q.php
 * by C.J. Steele <coreyjsteele@gmail.com>
 * http://sodaphish.com
 * 
 * (C)opyright 2009, Corey J. Steele, all rights reserved.
 * 
 * Created a long long time ago.
 * 
 * This script queries the player database.
 */
include_once( "config.php" );
include_once( "$rootdir/libs/commonLib.php" );
?>
<html>
<head>
	<title><?php print( $siteTitle ); ?> - player IP report</title>
</head>
<body>
<div align="center">
<table width="650">
<tr><td>

<?php

$results = array();

$q = $_GET["q"]; 

if( $q )
{
	print "<h2>Matches for ''$q''</h2>\n"; 
}

if( $q )
{
	$query = "";
	if( ! isip( $q ) )
	{
		$query = "SELECT ip, name, guid from ips where ( name like '%$q%' or guid like '%$q%' )";
	} elseif( isip( $q ) ){
		include("geoipcity.inc");
		include("geoipregionvars.php");
		$gi = geoip_open( "$rootdir/GeoLiteCity.dat", GEOIP_STANDARD);
		echo "<b>Best guess at where this IP is from:</b><br>\n";
		$record = geoip_record_by_addr($gi,"$q");
		print "city: " . $record->city . "<br>\n";
		print "region: " . $GEOIP_REGION_NAME[$record->country_code][$record->region] . "<br>\n";
		print "country: " . $record->country_name . "<br>\n";
		print "<hr><br>\n";
		geoip_close($gi);
		$query = "SELECT ip, name, guid from ips where ip like '%". $q . "%'";
	} #endif 
	
	$logger->debug( "query: $query" );

	if( $query ) 
	{
		$result = mysql_query( $query ); 
		if( ! $result )
		{ 
			$logger->error( "Couldn't execute query: $query" ); 
		} else {
			$logger->debug( "query executed successfully" );
			while( list( $i, $n, $g ) = mysql_fetch_row( $result ) )
			{
				if( ! isset( $results[$g] ) )
				{
					$results[$g] = array( $i, $n );
				}
			} #end while
		} #endif
	} #endif


	foreach( array_keys( $results ) as $r )
	{
		list( $i, $n ) = $results["$r"];
		if( isip( $q ) )
		{
			print "<a href=q.php?q=$n>$n</a> GUID:$r<br />\n";
		} else {
			print "<a href=q.php?q=$i>$i</a> GUID:$r<br />\n";
		}
	} //end while

}#endif
?>

</td></tr>
<tr><td>
<div align="center">
<form method="get" action="<?php print $caller; ?>">
<?php
	if( $q )
	{
		print "<input type=\"text\" name=\"q\" value=\"$q\">";
	} else {
		print "<input type=\"text\" name=\"q\" value=\"name, GUID or IP\">";
	}
?>
<input type="submit" value="Go!">
</form>

</div>
</td></tr>
</table>
</div>
</body>
</html>

<?php $logger->debug( "$caller_short __END__" ); ?>
