<?php

if( $ip )
{
	$now = time(); 
	$exp = $now + 21600;  //expires in 6 hours.

	$host_i = "insert into trusted_hosts (ip, add_date, exp_date, user, visible ) values ( '$ip', '$now', '$exp', '$g_uid', '1' )"; 

	$host_r = mysql_query( $host_i ); 
	print "<b><font color=#00aa00>$ip added.</font></b>"; 
	include "access/access_default.php"; 

} else {
	print "No IP address specified, use your browser's back button to complete the necessary form.\n"; 
}

?>
