<?php
/*
 * libs/commonLib.php
 * by C.J. Steele <coreyjsteele@gmail.com>
 * http://sodaphish.com
 * 
 * (C)opyright 2009, Corey J. Steele, all rights reserved.
 * 
 * Created on Oct 20,2009
 * 
 * This is a miscellaneous collection of functions that don't have a home, elsewhere.
 */
 
 include_once( "/var/www/config.php");
 

 /* getParam( $p )
  * this function gets a variable as it is contained in either $_GET or $_POST, while debugging its value to our logger
  */
 function getParam( $p )
{
	global $logger;
	$val = $_GET["$p"];
	if( ! $val ){ $val = $_POST["$p"]; }
	//$valOut = print_r( $val, true );  # TODO: handle arrays so we can intelligently export them, even multi-dimensional arrays.
	$logger->debug( "$p = $val" );
	if( is_array( $val ) )
	{
		return(  $val );
	} 
	return $val;
} //end getParam();




/*
 * isip( $ip )
 * function retruns a bool value based on a preg statement.
 */
function isip( $ip )
{
	global $logger;
  if( preg_match( "/^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]).){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/", $ip ) )
  {
    $logger->debug( "$ip is a valid IP address" );
    return 1;
  }
  $logger->error( "$ip is NOT a valid IP address" );
  return 0;
} //end isip()


//EOF
?>
