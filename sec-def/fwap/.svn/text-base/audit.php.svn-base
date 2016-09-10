<html>
<head>
	<title>F.W.A.P. DHCP Query</title>
	<link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>

<div align=center>
<a href=index.php><img src=http://frank.corp.good-sam.com/sec/fwap2/fwap.png border=0></a><br>
<table width=600 border=0>
<tr>
	<td>

<?php

function frmtmac ( $mac )
{
	$mac = strtoupper( $mac ); 
	$newmac = ""; 
	for( $x = 0; $x <= 14; $x+2)
	{
		$char = substr( $x, 2 );
		$newmac .= ":$char"; 
	}
	return $newmac; 
} //end frmtmac()

	if( $query and $ipomac)
	{
		// the user specified a query...
		print "<h2>Auditing $query...</h2>"; 
		print "<i>Entries are listed newest to oldest!</i><br><br>\n"; 
		print "Key: <font color=#0000ff>Granted</font> |
				<font color=#00bb00>Renewed</font> | 
				<font color=#ffff00>Released</font> |
				<font color=#ff0000>Auto Released</font><br><hr>\n"; 


		$conn = mysql_connect( "localhost", "root", "" );
		mysql_select_db( "fw2" );

		$query_q = "select date, type, ip, mac, host from leaseinfo where "; 

		if( $ipomac == "ip" )
		{
			$query_q .= "ip like '$query' "; 
		} else if( $ipomac == "mac" ){
			$query = strtolower( $query ); 
			$query = str_replace( ":", "", $query ); 
			$query_q .= "mac like '$query' "; 
		} else if( $ipomac == "name" ){
			$query_q .= "host like '$query' ";
		}

		$query_q .= " order by date desc"; 

		$query_r = mysql_query( $query_q );
		while( list( $date, $type, $ip, $mac, $host ) = mysql_fetch_row( $query_r ) )
		{
			#$msg = 0 if( $msg =~ "DHCP_GrantLease" );
			#$msg = 1 if( $msg =~ "DHCP_RenewLease" );
			#$msg = 2 if( $msg =~ "DHCP Release" );
			#$msg = 3 if( $msg =~ "DHCP Auto Release" );

			if( $type == 0 )
			{
				$type = "Granted"; 
				$color = "#0000ff"; 
			} else if( $type == 1 ){
				$type = "Renewed"; 
				$color = "#00bb00"; 
			} else if( $type == 2 ){
				$type = "Released"; 
				$color = "#ffff00"; 
			} else {
				$type = "Auto Releaseed"; 
				$color = "#ff0000"; 
			}

			//$mac = frmtmac( $mac ); 

			print "<li><font color=$color>$date $ip $mac $host</font></li>\n"; 
			$color = "#ffffff"; 
		}


	} else {
		// no query, show form...
		print "
			<form method=post action=$this>
			<input type=text name=query value=\"$query\"><br>
			<input type=radio name=ipomac value=ip>IP</input>
			<input type=radio name=ipomac value=mac>MAC</input>
			<input type=radio name=ipomac value=name>Name</input><br>
			<input type=submit>
			</form>
		";

	}


?>


	</td>
</tr>
</table>
</div>

</body>
</html>
