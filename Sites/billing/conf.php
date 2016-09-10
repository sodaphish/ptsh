<?php

$debug = 0;

//include libraries of functions we want to use throughout the system
include "lib/auth.php";
include "lib/template.php";
include "lib/modules.php";

//the name of the MASTER file.
$this = "index.php";

//this is a stub variable, once we start writing the authentication
// code, this will need to be fleshed out differently.
$session = "12315213542134"; 

//setup database connection here, this is the ONLY place the database
// connection will need to be setup.
$link = mysql_connect( "localhost", "root", "" )
	or die( "Couldn't connect to database: " . mysql_error() );
//select our "billing" database.
mysql_select_db( "billing" ) 
	or die( "Couldn't select database: " . mysql_error() );

//register modules here in coma-delimited list, like... 
// $modules = array( 'invoice', 'timesheet' );
$modules = array( 'invoice', 'timesheet' );

?>
