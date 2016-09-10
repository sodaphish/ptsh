<?php
/*
 * rchron.php
 * by C.J. Steele <coreyjsteele@gmail.com>
 * http://sodaphish.com
 * 
 * (C)opyright 2009, Corey J. Steele, all rights reserved.
 * 
 * Created on Oct 20,2009
 * 
 * This is the web front-end for the rchron, it allows you to add, pause, unpause, etc., 
 */
include_once( "config.php" );
include_once( "libs/commonLib.php" );
?>
<html>
<head>
	<title><?php print $siteTitle; ?> - RCON Command Scheduler</title>
</head>
<body>

<div align="center">
<table width=800 border=0>
<tr><td>

<?php

$dbg_ = getParam( "dbg_" );
$f = getParam( "f" );
$completed = getParam( "completed" );
$serverid = getParam( "serverid" );
$job = getParam( "job" );
$int = getParam( "int" );
$mult = getParam( "mult" );
$email = getParam( "email" );
$servers = getParam( "servers" );


// this hack is here to debug some issues we're having
// TODO: remove this once we've either got rchron working or have the getParam function doing this intelligently
$c = 0;
foreach( $servers as $s )
{
	$logger->debug( "s[$c]: $s");
	$c++;
}


function listJobs()
{
	global $logger;
# output rcon job id, job owner, command to run, interval of execution (including multiplier), which servers it runs on, and who to notify
print <<<EOA
<h2>Current Jobs</h2>
<table width=100% border=0>
<tr>
	<td bgcolor=#888888 valign=top align=left>
		<b>Job ID</b>
	</td>
	<td bgcolor=#888888 valign=top align=left>
		<b>Job Owner</b>
	</td>
	<td bgcolor=#888888 valign=top align=left>
		<b>Command</b>
	</td>
	<td bgcolor=#888888 valign=top align=left>
		<b>Schedule</b>
	</td>
	<td bgcolor=#888888 valign=top align=left>
		<b>Servers</b>
	</td>
	<td bgcolor=#888888 valign=top align=left>
		<b>Notify</b>
	</td>
</tr>
EOA;
	$jobSelectQuery = "select `jobid`, `owner`, `cmd`, `interval`, `multiplier`, `notify` from rchronJobs where `enabled`='y'"; 
	$jobSelectResult = mysql_query( $jobSelectQuery ) or $logger->error( mysql_error() );
	if( $jobSelectResult )
	{
		$bgcolor = ""; 
		$count = 0;
		while( list( $jobid, $owner, $cmd, $interval, $multiplier, $notify ) = mysql_fetch_row( $jobSelectResult ) )
		{
			$logger->debug( "jobid: $jobid" );
			$logger->debug( "owner: $owner" );
			$logger->debug( "cmd: $cmd" );
			$logger->debug( "interval: $interval" );
			$logger->debug( "multiplier: $multiplier" );
			$logger->debug( "notify: $notify" );

			if( $count % 2 ){ $bgcolor = "#ffffff"; } else { $bgcolor="#eeeeee"; }

			print "
			<tr>
			<td bgcolor=$bgcolor valign=top align=left>$jobid</td>
			<td bgcolor=$bgcolor valign=top align=left>$owner</td>
			<td bgcolor=$bgcolor valign=top align=left>rcon $cmd</td>
			<td bgcolor=$bgcolor valign=top align=left>every $interval $multiplier</td>
			<td bgcolor=$bgcolor valign=top align=left>
			";
			$jobServerQuery = "select serverid from rchronServers where jobid=$jobid";
			$logger->debug( "jobServerQuery: $jobServerQuery" );
			$jobServerResult = mysql_query( $jobServerQuery ) or $logger->error( mysql_error() ); 
			if( $jobServerResult )
			{
				while( list( $srvr ) = mysql_fetch_row( $jobServerResult ) )
				{
					$logger->debug( "srvr: $srvr" );
					$srvrDetailQuery = "select servername from servers where sid=$srvr"; 
					$logger->debug( "srvrDetailQuery: $srvrDetailQuery" );
					$srvrDetailResult = mysql_query( $srvrDetailQuery ) or $logger->error( mysql_error() ); 
					if( ! $srvrDetailResult ) 
					{
						print "<p>\"$srvrDetailQuery\" failed.</p>\n";
					} else {
						list( $serverName ) = mysql_fetch_row( $srvrDetailResult ) or $logger->error( mysql_error() );
						print "$serverName<br/>\n";
					}
				} #end while
			}
			print "
			</td>
			<td bgcolor=$bgcolor valign=top align=left>$notify</td>
			";
			$count++;
		} #end while
	} #end if
	print "</table>\n";
} #end listJobs()



function showAdd()
{
	print <<<EOO
<h2>Job Wizard</h2>
<p>Jobs are executed base off of the system clock.  Jobs run every 5 minutes will execute at 5, 10, 15...etc. every hour of every day.  Jobs set to run every x hours will run at the top of the hour.  Jobs set to run only once a day will run at midnight of that day.</p>
<form method=$caller action=post>
<input type=hidden name=f value=add>
<input type=hidden name=completed value=1>
<table width=100% border=0>
<tr>
	<td valign=top align=left>
		<b>1. The RCON command to run</b><br/>
		<i>Type the command in here as you would from the console, <b>WITHOUT THE 'rcon'</b>.</i>
	</td>
	<td valign=top align=left>
		<input type=text size=40 name=job> 
	</td>
</tr>
<tr>
	<td valign=top align=left>
		<b>2. Run this command every</b><br/>
		<i>Type in how often you want it to run, remember there are 60 minutes in an hour, 24 hours in a day, etc.</i>
	</td>
	<td valign=top align=left>
		<nobr><input type=text name=int size=3 value="">
		<select name=mult>
			<option value=min>minutes</option>
			<option value=hr>hours</option>
			<option value=day>days</option>
		</select></nobr>
	</td>
</tr>
<tr>
	<td valign=top align=left>
		<b>3. Select the servers to run this command on</b>
		<i>You can select multiple servers by holding CTRL as you click the name.</i>
	</td>
	<td valign=top align=left>
EOO;

print "<select name=servers[] multiple size=7>\n";
$query = "select sid, servername from servers";
$result = mysql_query( $query );
while( list( $id, $name ) = mysql_fetch_row( $result ) )
{
print "<option value=\"$id\">$name</option>\n";
}
print "</select><br/><br/>\n";

print <<<EOH2
	</td>
</tr>
<tr>
	<td valign=top align=left>
		<b>4. Notify someone with this command's output?</b>
		<i>If you fill in an email address, that person will get an email every time the job runs. I'm debating whether this is necessary or not, but I'm including it for completness.</i>
	</td>
	<td valign=top align=left>
		<INPUT type=text name=email value="">
	</td>
</tr>
<tr>
	<td valign=top align=left>
		<b>5. Review and commit</b>
		<i>Please look over what you've typed in and make sure its correct.</i>
	</td>
	<td valign=top align=left>
		<INPUT type=submit value=Add>
	</td>
</tr>
</table>
</form>
EOH2;
} #end showAdd()


function showPauseUnpause( $cmd )
{
	global $logger;
	$enabled = "n";
	if( preg_match( '/^(p|P)ause/', $cmd ) ){ $enabled = 'y'; }
	$pauseQuery = "select jobid, cmd from rchronJobs where enabled = '$enabled'";
	$pauseResult = mysql_query( $pauseQuery ) or $logger->error( mysql_error() );
	print "<h2>$cmd A Job</h2>\n";
	print "
		<form method=$caller action=post>
		<input type=hidden name=f value=$cmd>
		<input type=hidden name=completed value=1>
		<select name=job>
	";
	while( list( $jobid, $cmd ) = mysql_fetch_row( $pauseResult ) ) {
		$serverJobDetailQuery = "select serverid from rchronServers where jobid=$jobid";
		$serverJobDetailResult = mysql_query( $serverJobDetailQuery ) or $logger->error( mysql_error() );
		$serverString = "";
		while( list( $serverid ) = mysql_fetch_row( $serverJobDetailResult ) )
		{
			$serverDetailQuery = "select servername from servers where sid=$serverid";
			$serverDetailResult = mysql_query( $serverDetailQuery ) or $logger->error( mysql_error() );
			if( $serverDetailResult )
			{
				while( list( $servername ) = mysql_fetch_row( $serverDetailResult ) )
				{
					$serverString = $serverString . "\"$servername\" "; //this should be a .= but we've expanded it to make sure we're getting the right thing.
				} #end while
			} else {
				print "<p>\"$serverDetailQuery\" failed.</p>\n";
			}
		} #end while
		print "<option value=$jobid>Job #$jobid ('rcon $cmd' on $serverString  )</option>\n";
	} #end while
	print "
		</select>
		<input type=submit value=$cmd>
		</form>
	";
} #end showPauseUnpause()



function addJob( $owner, $cmd, $int, $mult, $servers, $notify ) 
{
	global $logger;

	$logger->debug( "owner: $owner" );
	$logger->debug( "cmd: $cmd" );
	$logger->debug( "int: $int" );
	$logger->debug( "mult: $mult" );
	$logger->debug( "servers: $servers" );
	$logger->debug( "notify: $notify" );

	if( $notify )
	{
		$jobAddInsert = "insert into rchronJobs ( owner, cmd, `interval`, multiplier, notify ) values ( '$owner', '$cmd', $int, '$mult', '$notify' )";
	} else {
		$jobAddInsert = "insert into rchronJobs ( owner, cmd, `interval`, multiplier ) values ( '$owner', '$cmd', $int, '$mult' )";
	}
	$jobAddResult = mysql_query( $jobAddInsert ) or $logger->error( mysql_error() );
	if( ! $jobAddResult ) 
	{
		print "<p>\"$jobAddInsert\" failed. (" . mysql_error() . ")</p>\n";
	}
	$jobID = mysql_insert_id();
	foreach( $servers as $s )
	{
		$jobAddServerInsert = "insert into rchronServers ( jobid, serverid ) values ( '$jobID', '$s' )";
		$jobAddServerResult = mysql_query( $jobAddServerInsert ) or $logger->error( mysql_error() );
		if( ! $jobAddServerResult )
		{
			print "<p>\"$jobAddServerInsert\" failed. (" . mysql_error() . ")</p>\n";
		}
	}
	if( ! $jobID ) 
	{
		print "<p>\"$jobAddInsert\" failed. (" . mysql_error() . ")</p>\n";
	}
	print "<p><b>Job $jobID added!</b></p><br/>\n";
} #end addJob()



function pauseUnpause( $cmd, $jobid )
{
	global $logger;
	$enabled = "n";
	if( preg_match( '/^(p|P)ause/', $cmd ) ){ $enabled = 'y'; }
	$pauseJobUpdate = "update rchronJobs set enabled='$enabled' where jobid=$jobid";
	$pauseJobResult = mysql_query( $pauseJobUpdate ) or $logger->error( mysql_error() );
	print "<p><b>Job $jobid $cmd" . "ed</b></p><br/>\n";
} #end pauseUnpause()



switch( $f )
{
	case 'add':
		if( $completed )
		{
			addJob( "$username__", "$job", "$int", "$mult", $servers, "$email" );
		} else {
			showAdd();
		}
		break;
	case 'Pause':
		if( $completed )
		{
			pauseUnpause( 'Pause', "$job" );
		} else {
			showPauseUnpause( 'Pause' );
		}
		break;
	case 'Unpause':
		if( $completed )
		{
			pauseUnpause( 'Unpause', "$job" );
		} else {
			showPauseUnpause( 'Unpause' );
		}
		break;
	default:
		listJobs();
		print "<hr/>\n";
		showPauseUnpause( 'Pause' );
		print "<hr/>\n";
		showPauseUnpause( 'Unpause' );
		print "<hr>";
		showAdd();
}

?>


</td></tr>
</table>
</div>


<?php
if( $dbg_ )
{
	$logger->showBacktrace("html");
} //end if
?>

</body>
</html>

<?php
$logger->debug( "$caller_short __END__" );

//EOF rchron.php
?>
