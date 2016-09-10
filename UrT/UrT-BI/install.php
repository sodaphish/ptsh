<?php
/*
 * install.php
 * by C.J. Steele <coreyjsteele@gmail.com>
 * http://sodaphish.com
 * 
 * (C)opyright 2009, Corey J. Steele, all rights reserved.
 * 
 * Created on Oct 21,2009
 * 
 * This is the web-based installer for the BI
 * 
 * 
 * This script needs to:
 * gather the information about the installer:
 * 		- DB information
 * 		- HTTP user/directory owner
 * 		- initial user/admin
 * 		- logo
 * check dependancies
 * copy the files to their directories
 * set permissions on files and directories
 */
 
//$directories = array( "logs", "gamelogs", "rconlogs", "" );


/*
 * checkDependancies()
 * this function returns a boolean value indicating whether or not all the various dependencies are met for the install to proceed.
 */
function checkDependancies()
{
	//check the directories we need writeable.
	foreach( $directories as $d )
	{
		if( ! is_writeable( $d ) )
		{
			return false;
		} //end if
	} //end foreach
	//TODO: check file permissions
} //end checkDependancies()


/*
 * createDatabases()
 */
function createDatabase()
{
	
} //end createDatabase()



/*
 * wizardStep1()
 */
function wizardStep1()
{
	
} //end wizardStep1()


/*
 * wizardStep2()
 */
function wizardStep2()
{
	
} //end wizardStep2()


?>
<html>
<head>
	<title>SodaPhish's Ban Interface Installer</title>
</head>
<body>
 
<?php
?>

</body>
</html>