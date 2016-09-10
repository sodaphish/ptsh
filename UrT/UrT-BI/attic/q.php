<html>
<head>
	<title>|WC| player and IP search</title>
</head>
<body>
<div align="center">
<table width="650">
<tr><td>

<?php
include_once( "config.php" );

$q = $_GET["q"]; 
//$q = getenv( "QUERY_STRING" );

if( $q )
{
		if( preg_match( "/[0-9]*.\.[0-9]*.\.[0-9]*.\.[0-9]*/", $q ) )
		{
			include("geoipcity.inc");
			include("geoipregionvars.php");
			$gi = geoip_open( "/home/hostedby/mine/wc/GeoLiteCity.dat", GEOIP_STANDARD);
			echo "<b>Best guess at where this IP is from:</b><br>\n";
			$record = geoip_record_by_addr($gi,"$q");
			print "city: " . $record->city . "<br>\n";
			print "region: " . $GEOIP_REGION_NAME[$record->country_code][$record->region] . "<br>\n";
			print "country: " . $record->country_name . "<br>\n";
			//print "postal code: " . $record->postal_code . "<br>\n";
			//print "latitude: " . $record->latitude . "<br>\n";
			//print "longitude: " . $record->longitude . "<br>\n";
			//print "dma code: " . $record->dma_code . "<br>\n";
			//print "area code: " . $record->area_code . "<br>\n";
			print "<hr><br>\n";
			geoip_close($gi);
		}

	// the user put some crap in.

	$total_talley = 0;
	$displayed_talley = 0;

	$results = array();

	foreach( $databases as $db ) 
	{

		mysql_select_db( "$db" );
		$query = "";  //flush the last query
		if( preg_match( "/[0-9]*.\.[0-9]*.\.[0-9]*.\.[0-9]*/", $q ) )
		{
			// this is an IP address
			$query = "SELECT playerID from vsp_playerdata where dataName = 'ip' and dataValue like '%$q%'";
		} else {

			// this is a username
			$query = "SELECT dataValue from vsp_playerdata where playerID like '%". $q . "%' and dataName = 'ip'"; 
		}
		//print "$db: $query<br>\n";

		print "<h2>$db</h2>\n";
		

		$result = mysql_query( $query ); 
		if( !$result ){ die('Invalid query: ' . mysql_error()); }

		while( list( $value ) = mysql_fetch_row( $result ) )
		{
			// output our results.
			$total_talley++;

			if( preg_match( "/[0-9]*.\.[0-9]*.\.[0-9]*.\.[0-9]*./", $value ) ) 
			{
				$value = preg_replace( "/\:[0-9]*/", "", $value ); 
			}

			if( ! in_array( $value, $results ) )
			{
				if( preg_match( "/[0-9]*.\.[0-9]*.\.[0-9]*.\.[0-9]*./", $value ) ) 
				{
					print "<a href=q.php?q=$value>$value</a><br>\n";
				} else {
					print "<a href=iprpt.php?q=$value>$value</a><br>\n";
				}
				array_push( $results, $value );
				$displayed_talley++;
			}
		}
		

	} //end foreach


	print "<br><br>...displaying $displayed_talley unique resutls out of $total_talley total result(s).\n<hr>";
	print "<form method=get action=q.php><b>Search:</b> <input type=text name=q> <input type=submit value=Go></form>";


} else {

	// show the form.
	print "<form method=get action=q.php><b>Search:</b> <input type=text name=q> <input type=submit value=Go></form>";

}

?>


</td></tr>
</table>
</div>
</body>
</html>
