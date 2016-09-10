<?php

/* this needs to be secured somehow */
$now = time();

	$trusted_q = "select id, ip, add_date, exp_date, renew_count from trusted_hosts where user = '$g_uid' and visible='1'"; 
	$trusted_r = mysql_query( $trusted_q );

	$rowct = mysql_affected_rows(); 
	print "<h1>Your Trusted Hosts</h1>"; 
	if( $rowct )
	{
		print "<table width=600 border=1>\n<tr><td><b>IP</b></td><td><b>Added</b></td><td><b>Expires</b></td><td><b>Options</b></td></tr>"; 
		while( list( $id, $ip, $add_date, $exp_date, $renew_count ) = mysql_fetch_row( $trusted_r ) )
		{
			print "<tr><td>$ip</td><td>" . strftime( "%D %R", $add_date ) . "</td><td>" . strftime( "%D %R", $exp_date ) . "</td><td>[ <a href=access.php?func=renew&id=$id>renew</a> | <a href=access.php?func=revoke&id=$id>revoke</a> ]</td></tr>\n"; 
		}
		print "</table>\n";
	} else {
		print "<p>You have no configured hosts, yet.</p>"; 
	}


	print "<h1>Add New Trusted Host</h1>";
	print "<p>Your current IP address is: " . $g_remote_addr . "</p>"; 

	print "
	<form action=access.php method=post>
	<input type=hidden name=func value=add>
	IP Address: <input type=text name=ip value=\"$g_remote_addr\">
	<input type=submit value=\"&gt; &gt;\">
	</form>
	";

?>
