<?php
/*
 * config.php
 * by C.J. Steele <coreyjsteele@gmail.com>
 * http://sodaphish.com
 * 
 * (C)opyright 2009, Corey J. Steele, all rights reserved.
 * 
 * Created long long ago in a galaxy not so far away... 
 * 
 * This is a global configuration file for the site; it takes care of setting 
 * up initial bits like the logger and the database connection and some globals.
 */

// some globals 
$siteTitle = "|WC| Ban Interface";
$rootdir = "/var/www"; 
 
//setup PHP ini bits
ini_set( 'safe_mode', '0' );
ini_set( 'display_errors', 1 );
ini_set( "register_globals", "1" );
ini_set( "display_errors", "1" );
ini_set( "safe_mode_exec_dir", "$rootdir/bin" );



//call our includes
include_once( "$rootdir/libs/commonLib.php" );
include_once "$rootdir/libs/Logging.php";

//setup our database connection
$db = mysql_connect( ":/var/run/mysqld/mysqld.sock", "urt-bi", "urt-bi12" );
mysql_select_db( "urt" );


//set some variables.
if( ! $username__ ){ $username__ = $_SERVER['PHP_AUTH_USER']; }
if( ! $remote_addr ){ $remote_addr = getenv( REMOTE_ADDR ); }
$caller = $_SERVER['PHP_SELF'];
$caller_short = basename( $caller, ".php" );

//setup our logger interface
$logger = new Logging( "f", "$rootdir/logs/bi.log" );
//$logger = new Logging( "f", "$rootdir/logs/$caller_short.log" );
$logger->setLevel( "debug" );


//log some info in debug mode.
$logger->debug( "$caller_short __BEGIN__" );
$logger->debug( "user: $username__" );

//establish user priv level from the database
$query = "select privlevel from users where username = '$username__' and privlevel > 0";
$result = mysql_query( $query );
list( $privlevel__ ) = mysql_fetch_row( $result );
$logger->debug( "privlevel: $privlevel__" );


//EOF config.php
?>
