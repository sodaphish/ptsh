<?php

include "conf.php";

if( $session )
{
	//session was defined, check to see if its active
	if( ! sessionActive( $session ) )
	{
		//ession wasn't active!
		header( "Location: login.php" );
		exit(1);
	}
} else {
	header( "Location: login.php" );
	exit(1);
}

//session was valid, begin doing real work.


//setup pages w/ menus, views, etc.
$menuItems = array();
$subMenuItems = array();

//process each module's configuration -- builds menus and necessary sub-menus
initModules( $modules );

print "
	<html>
	<head><title>FST Billing</title></head>
	<body>
	<table width=100%>
	<tr><td valign=top> <!-- left column -->
";

listBox( "Main Menu", $menuItems );
if( $subMenuItems )
{
	listBox( "Sub Menu", $subMenuItems );
}

print "
	</td><td valign=top align=left> <!-- right column -->
";

if( $f )
{
	include "mod/$f/main.php";
}

print "
	</td></tr>
	</table>
	</body>
	</html>";


?>
