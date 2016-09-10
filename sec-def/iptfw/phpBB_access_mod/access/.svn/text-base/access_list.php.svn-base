<?php

/* this needs to be secured somehow */
$now = time();

	$trusted_q = "select id, ip, add_date, exp_date, renew_count from trusted_hosts where visible='1'"; 
	#print $trusted_q . "<br>\n"; 
	$trusted_r = mysql_query( $trusted_q );

	$rowct = mysql_affected_rows(); 
	print "<h1>Currently Trusted Hosts</h1><P>If you see your IP address listed here, you do not need to re-add it.</p>"; 
	if( $rowct )
	{
		print "<table width=600 border=1>\n<tr><td><b>IP</b></td><td><b>Added</b></td><td><b>Expires</b></td><td><b>Options</b></td></tr>"; 
		while( list( $id, $ip, $add_date, $exp_date, $renew_count ) = mysql_fetch_row( $trusted_r ) )
		{
			print "<tr><td>$ip</td><td>" . strftime( "%D %R", $add_date ) . "</td><td>" . strftime( "%D %R", $exp_date ) . "</td><td>[ <a href=access.php?func=renew&id=$id>renew</a> | <a href=access.php?func=revoke&id=$id>revoke</a> ]</td></tr>\n"; 
		}
		print "</table>\n";
	} else {
		print "<p>There are no configured hosts, yet.</p>"; 
	}

?>
