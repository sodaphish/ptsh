<html>
<head>
	<title>geoIP analysis</title>
</head>
<body>
<div align="center">
<table width="650">
<tr><td>


<table border="1">
<?php

include("geoipcity.inc");
include("geoipregionvars.php");

$IPs[] = "";

$fh = fopen( "access.log", "r" );
$gi = geoip_open( "GeoLiteCity.dat", GEOIP_STANDARD);
while( !feof( $fh ) ) 
{
	$line = fgets( $fh );
	$e = preg_split( "/\s/", $line, 2 );
	//print "$e[0]<br/>\n";
	
	if( ! isin( $e[0], $IPs ) )
	{
		print "<tr><td valign=\"top\">$e[0]</td><td valign=\"top\">";
		$record = geoip_record_by_addr($gi,"$e[0]");
		print "city: " . $record->city . "<br>\n";
		print "region: " . $GEOIP_REGION_NAME[$record->country_code][$record->region] . "<br>\n";
		print "country: " . $record->country_name . "<br>\n";
		print "</td></tr>\n";

		array_push( $IPs, "$e[0]" );
	}
}
geoip_close($gi);
fclose( $fh );


function isin( $i, $l )
{
	foreach( $l as $item )
	{
		if( $item == $i )
		{
			return 1;
		}
	}
	return 0;
} //end isin()

?>
</table>


</td></tr>
</table>
</div>
</body>
</html>
