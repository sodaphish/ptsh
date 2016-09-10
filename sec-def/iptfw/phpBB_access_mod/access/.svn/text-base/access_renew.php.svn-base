<?php

if( $id ) 
{
	$newexp = time() + 21600; 

	$host_u = "update trusted_hosts set exp_date='$newexp' where id='$id' and user='$g_uid'"; 
	$host_r = mysql_query( $host_u );

	$renewct_q = "select renew_count from trusted_hosts where id='$id' and user='$g_uid'"; 
	$renewct_r = mysql_query( $renewct_q ); 
	list( $renewct ) = mysql_fetch_row( $renewct_r ); 

	$renewct++;

	$renewct_u = "update trusted_hosts set renew_count='$renewct' where id='$id' and user='$g_uid'"; 
	$renewct_r = mysql_query( $renewct_u );

	print "<p><b><font color=#00aa00>Your trusted host will expire on " . strftime( "%D %R", $newexp ) . ".</font></b></p>\n"; 

	include "access/access_default.php"; 

} else {
	print "No host specified, use your browser's back button to complete the form properly."; 
}

?>
