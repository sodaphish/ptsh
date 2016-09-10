<html>
<head>
	<title>|WC| Ban Interface</title>
</head>
<body>

<div align="center">
<table width="600" border="0">
<tr><td>
<!-- body --> 

<?php 

include_once( "config.php" );

$authorized = array();

// populate the authorized users table.
$query = "select username from users where privlevel > 0";
$result = mysql_query( $query );
while( list( $username ) = mysql_fetch_row( $result ) )
{
	array_push( $authorized, $username );
}


$logger->debug( "authorized = $authorized" );
$logger->info( "username = $username__" );
$logger->info( "connection from $remote_addr" );
$completed = $_POST["completed"];
$logger->debug( "completed = $completed" );
$ip = $_GET["ip"]; 
if( ! $ip ){ $ip = $_POST["ip"]; }
$logger->debug( "ip = $ip" );
$reason = $_GET["reason"]; 
if( ! $reason ){ $reason = $_POST["reason"]; }
$logger->debug( "reason = $reason" );
$f = $_GET["f"]; 
if( ! $f ){ $f = $_POST["f"]; }
$logger->debug( "f = $f" );
$expdate = $_GET["expdate"];
if( ! $expdate ){ $expdate = $_POST["expdate"]; }
$notes = $_GET["notes"];
if( ! $notes ){ $notes = $_POST["notes"]; }
$logger->debug( "expdate = $expdate" );
$tempban = $_GET["tempban"];
if( ! $tempban ){ $tempban = $_POST["tempban"]; }
$logger->debug( "tempban = $tempban" );
$playername = $_GET["playername"];
if( ! $playername ){ $playername = $_POST["playername"]; }
$logger->debug( "tempban = $tempban" );




function ban( $ip, $reason )
{
	global $logger;
	$logger->info( "BANNING $ip because: $reason" );
	print "<h1>$ip has been banned!</h1>";
	print "<pre>";
	passthru( "./bin/ban.py $ip" );
	print "</pre>";
	print "<p>The reference code for this transaction is " . $logger->getsession() . "</p>"; 
} //end ban()


function unban( $ip, $reason )
{
	global $logger;
	global $authorized; 
	global $username__;

	if( isin( $username__, $authorized ) )
	{
		$logger->info( "UNBANNING $ip because: $reason" );
		print "<h1>$ip has been un-banned!</h1>";
		print "<pre>";
		passthru( "./bin/ban.py -u $ip" );
		print "</pre>";
		print "<p>The reference code for this transaction is " . $logger->getsession() . "</p>"; 
	} else {
		print "<h1>Sorry mate!</h1> <p>Unbanning is reserved for senior admins.</p>";
	}
} //end unban()


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


function isin( $item, $list ) 
{
	global $logger;
  foreach( $list as $l ) 
  {
    if( $l == $item ){ return 1; }
  }
  return 0;
} //end isin()


#
# TODO: fix it so we can pass a data or use NOW()
function logEvent( $type, $sessionid, $date, $ip, $playername, $bannedby, $reason, $notes )
{
	global $logger;
	$insert = "insert into bans ( type, sessionid, ip, playerid, bannedby, reason, notes ) values ( '$type', '$sessionid', '$ip', '$playername', '$bannedby', '$reason', '$notes' )";
	$logger->debug( "logEvent() insert: $insert" );
	$result = mysql_query( $insert );
	if( ! $result )
	{ 
		$logger->error( mysql_error() );
		return( 0 );
	} elseif( $result ) { 
		return( 1 );
	} else {
		$logger->warn( "wth?  logEvent() encountered something funky, the insert didn't succed or fail?  OH GOD! SOMEONE DIVIDED BY ZERO! RUN!!!!!!!!!!!!!!!!!!" );
		return( -1 );
	}
} //end logEvent()




if( $completed ) 
{
	$type = "ban";
	if( isip( $ip ) and $f and $reason )
	{
		if( $f == "ban" )
		{
			if( isset( $tempban ) )
			{
				$logger->debug( "processing temporary ban" );
				if( strtotime( $expdate ) > strtotime( "now" ) )
				{
					$logger->info( "TEMPBAN:$ip/" . date( "U", strtotime( $expdate ) ) );
					$type = "tmpban"; 
				} else {
					print "<h1>Oops!  Invalid date.</h1><p>You need to specify your date in YYYY-MM-DD form, or it won't work.</p>";
					exit( 0 );
				}
			} // end of tempban bits
			if( file_exists( $_FILES['demo']['tmp_name'] ) )
			{
				$logger->debug( "there is a demo attached." );
				$logger->debug( "uploaded file's tmp name: " . $_FILES['demo']['tmp_name'] );
				$destination = "demos/" . $logger->getsession() . ".dm_68"; 
				$logger->debug( "uploaded file target: $destination" );
				if( ! file_exists( $destination ) )
				{
					if( move_uploaded_file( $_FILES['demo']['tmp_name'], $destination ) )
					{
						$logger->error( "couldn't upload the demo!" );
					} else {
						$logger->info( "uploaded demo to $destination" );
					}
				}
			} else {
				$logger->debug( "no upload provided." );
			}
			$logger->info( "banning $ip because: $reason" );
			if( logEvent( $type, $logger->getsession(), 'NOW()', $ip, $playername, $username__, $reason, $notes ) )
			{	
				ban( $ip, $reason );
			} else {
				$logger->error( "failed ban because event couldn't be logged!" );
			}

		} elseif( $f == "unban" ){
		
			$type = "unban";
			$logger->info( "UNbanning $ip because: $reason" );
			if( logEvent( $type, $logger->getsession(), 'NOW()', $ip, $playername, $username__, $reason, $notes ) )
			{
				unban( $ip, $reason );
			} else {
				$logger->error( "failed to unban because event couldn't be logged!" );
			}

		} else {
?>

<h1>Error</h1>
<p>stop hand-crafting URL's!  This event has been logged and will be investigated.</p>

<?php
			$logger->error( "someone was hand-crafting URL's" );
		} #end if

	} else {
?>

<h1>Error</h1>
<p>You must complete the form before submitting it -- all fields are required.</p>

<?php
	}

} else {
?>

<table>
<form enctype="multipart/form-data" method=post action=ban.php>
<input type="hidden" name="completed" value="1">
<tr><td>IP Address:</td><td><input type="text" name="ip" value="<?php print "$ip"; ?>"></td></tr>
<tr><td>Reason:</td><td><select name="reason"><option value="asshat">ass-hat</option><option value="tker">tk-er</option><option value="hacker">hacker</option></select></td></tr>
<tr><td>Demo:</td><td><input type="file" name="demo"></td></tr>
<tr><td>Player Name:</td><td><input type="text" name="playername"></td></tr>
<tr><td>Notes:</td><td><input type="text" name="notes"></td></tr>
<tr><td>Temporary Ban? <input type="checkbox" name="tempban"></td><td> Expires: <input type="text" name="expdate" value="YYYY-MM-DD"></td></tr>
<tr><td><select name="f"><option value="ban">Ban</option><option value="unban">Unban</option></select></td><td><input type="submit" value="&gt; &gt;"></td></tr>
</form>
</table>

<?php

} //endif

?>

<!-- end body -->
</td></tr>
<tr><td>
<div align="center"><small>for help e-mail <a href="mailto:sodaphish@gmail.com">sodaphish@gmail.com</a></div>
</td></tr>
</table>
</div>

</body>
</html>
