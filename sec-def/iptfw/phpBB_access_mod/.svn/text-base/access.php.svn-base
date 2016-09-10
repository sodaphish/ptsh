<?php

// (C)opyright 2003, C.J. Steele <coreyjsteele@yahoo.com>, all rights reserved.
//
// this isn't very refined, because I haven't got much time... yay!

$db_host = "localhost"; 
$db_name = "name"; 
$db_user = "user"; 
$db_pass = "pass"; 

$trst_usr_grp = "31"; 

//setup the database connection...
$link = mysql_connect( "$db_host", "$db_user", "$db_pass" )
	or die( "Couldn't connect to database." );
mysql_select_db( "$db_name" );

//global variables we'll need.
$g_uid; 
$g_gid;

$g_remote_addr = getenv( "REMOTE_ADDR" );



function get_userid( $sid )
{
	$session_query = "select session_user_id from sessions where session_id = '$sid'"; 
	$session_result = mysql_query( $session_query )
		or die( "Couldn't get session data.". mysql_error() ); 
	list( $user ) = mysql_fetch_row( $session_result ); 
	return $user; 
}


function get_groupauth( $uid )
{
	//see if the user is in the trusted_users group...
	// return 1 if they are, 0 if they aren't and -1 for all other cases.
	$grp_q = "select * from user_group where user_id = '$uid' and group_id ='$trst_usr_grp' and user_pending = '0'"; 
	$grp_r = mysql_query( $grp_q )
		or die( mysql_error() );
	$affected_rows = mysql_affected_rows(); 
	
	if( $affected_rows == 1 )
	{
		return 1;
	} else {
		return 0; 
	}
}



// you'll need to mangle the "sodaphish_sid" to whatever the cookie is that gets dumped 
// on your box for your phpBB site...
if( $sodaphish_sid )
{ 
	$g_uid = get_userid( $sodaphish_sid ); 
	$g_gid = get_groupauth( $g_uid ); 
} else { 
	$g_uid = -1; 
	$g_gid = -1;
}



if( $g_uid >= 0 )
{

	if( $g_gid )
	{
		// the user should be logged in!
		// check to see if the user has a character sheet
		// mangle this however you want for your own site...
		print "
		<html>
		<head>
			<title>SodaPhish.COM Trusted Users</title>
		</head>
		<style type=\"text/css\">
		";
		include "templates/aallixSilver/aallix.css"; 
		print "
		</style>
		<body>
		<font face=\"Verdana, Helvetica, Arial\" size=-1>
		<h1>SodaPhish.COM Trusted Users</h1>
		"; 

		//this is where we do the work of the trusted users form...

		if( $func == "add" )
		{
			//trust a new host
			include "access/access_add.php"; 
		} else if( $func == "renew" ){
			//renew trust for a host
			include "access/access_renew.php"; 
		} else if( $func == "revoke" ){
			//revoke trust for a host
			include "access/access_revoke.php"; 
		} else {
			//default view...
			include "access/access_default.php"; 
			print "<hr>"; 
			include "access/access_list.php";
		}

		print "
		</font>
		</body>
		</html>
		";
	} else {

		print "<h1>WARNING: YOU ARE NOT AUTHORIZED.</h1>You are not authorized to access this form; your attempt to access this form has been logged and if further attempts are made, your IP will be banned from the site.";

	}

} else {

	// the user needs to log in first.
	header( "Location: login.php?redirect=access.php" );

}


?>
