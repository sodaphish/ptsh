<?php

function loadModConf( $modName ) 
{
	global $debug;
	include "mod/$modName/conf.php";
	
	if( $debug )
	{
		print "loadModConf( $modName )<br>\n";
	}
}


function initModules( $modules )
{
	global $debug; 

	foreach( $modules as $mod )
	{
		loadModConf( $mod );
	}

	if( $debug )
	{
		print "loadModConf( $modName )<br>\n";
	}
}

?>
