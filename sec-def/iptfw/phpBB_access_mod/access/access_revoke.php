<?php

if( $id )
{

	$revoke_u = "update trusted_hosts set visible='0' where id='$id' and user='$g_uid'"; 
	$revoke_r = mysql_query( $revoke_u ); 

	print "<p><font color=#ff0000><b>The host's trust has been revoked.</b></font></p>\n"; 

	include "access/access_default.php"; 

} else {

	print "No host specified, use your browser's back button to properly complete the form.\n"; 

}

?>
