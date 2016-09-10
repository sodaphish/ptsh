#!/usr/bin/php -q
<?php

$username__ = "banBot";
$remote_agent = "127.0.0.1";

include_once( "/var/www/config.php" );
include_once( "$rootdir/libs/rcon.php" );
include_once( "$rootdir/libs/ProcessHandler.php" );


function ban( $ip )
{
	global $logger;
	$serverQuery = "select serverip, serverport, serverrcon from servers";
	$serverQueryResult = mysql_query( $serverQuery ) or $logger->error( mysql_error() );
	while( list( $serverip, $serverport, $serverrcon ) = mysql_fetch_row( $serverQueryResult ) )
	{
		$q = new q3query( $serverip, $serverport );
		if( $q )
		{
			$logger->debug( "connected to $serverip:$serverport successfully" );
			$q->set_rconpassword( $serverrcon );
			$q->rcon( "addip $ip" );
			$logger->info( "banned $ip " . chop( $q->get_response() ) ); 
		} else {
			$logger->error( "Failed to connect to $serverip:$serverport!" );
			return false;
		} #endif
	} #end while
	return true;
} #end ban()

function unban( $ip )
{
	global $logger;
	$serverQuery = "select serverip, serverport, serverrcon from servers";
	$serverQueryResult = mysql_query( $serverQuery ) or $logger->error( mysql_error() );
	while( list( $serverip, $serverport, $serverrcon ) = mysql_fetch_row( $serverQueryResult ) )
	{
		$q = new q3query( $serverip, $serverport );
		if( $q )
		{
			$logger->debug( "connected to $serverip:$serverport successfully" );
			$q->set_rconpassword( $serverrcon );
			$q->rcon( "remove $ip" );
			$logger->info( "unbanned $ip " . chop( $q->get_response() ) ); 
		} else {
			$logger->error( "Failed to connect to $serverip:$serverport!" );
			return false;
		} #endif
	} #end while
	return true;
} #end unban()


function processTemporaryBans()
{
	global $logger;
	$unprocq = "select banid, ip, expires, playerid  from bans where state='unprocessed' and type='tmpban'";
	$unprocr = mysql_query( $unprocq );
	$counter = 0;
	while( list( $bid, $ip, $expires, $playerid ) = mysql_fetch_row( $unprocr ) )
	{
		if( ban( $ip ) )
		{
			$updateQuery = "update bans set state='midway' where banid=$bid";
			$updateResult = mysql_query( $updateQuery ) or $logger->error( mysql_error() );
		} else {
			$logger->error( "ban() failed.  WTH?" );
		}
	} #end while

} #end processTemprorary Bans()


function processUnbans()
{
	global $logger;
	$unbanQuery = "select banid, ip, type from bans where ( ( ( (now() - expires ) > 0 ) and state='midway' ) or ( type='unban' and state='unprocessed' ) )";
	#bans where ( ( state='unprocessed' and type='unban' ) or ( expires=NOW() and type='tmpban' ) )";
	$unbanQueryResult = mysql_query( $unbanQuery ) or $logger->error( mysql_error() );
	while( list( $banid, $ip, $type ) = mysql_fetch_row( $unbanQueryResult ) )
	{
		if( unban( $ip ) )
		{
			#$logEventInsert = "insert into bans ( type, sessionid, ip, playerid, bannedby, reason, notes ) values ( 'unban', '" . $logger->getsession() . "', '$ip', '$playerid', '$username__', 'ban expired', '' )";
			#$logEventResult = mysql_query( $logEventInsert ) or $logger->error( mysql_error() );
			#if( $logEventResult )
			#{
				$updateQuery = "update bans set state='processed' where banid=$banid"; 
				$updateQueryResult = mysql_query( $updateQuery ) or $logger->error( mysql_error() );
				$logger->info( "banBot unbanned $ip" );	
			#} #endif
		} else {
			$logger->error( "processUnbans(): couldn't unban $ip!" );
		} #endif
	} #end while
} #end processUnbans()


function processBans()
{
	global $logger;
	$banQuery = "select banid, ip, type from bans where state='unprocessed' and type='ban'";
	$banQueryResult = mysql_query( $banQuery ) or $logger->error( mysql_error() );
	while( list( $banid, $ip, $type ) = mysql_fetch_row( $banQueryResult ) )
	{
		if( ban( $ip ) )
		{
			# this ugly hack gets us around having to track a third-state for temp bans.
			if( ! preg_match( "/tmpban/", $type ) )
			{
				$updateQuery = "update bans set state='processed' where banid=$banid"; 
				$updateQueryResult = mysql_query( $updateQuery ) or $logger->error( mysql_error() );
			}
		} else {
			$logger->error( "Couldn't ban $ip!" );
		} #endif 
	} #end while
} #end processBans()



if(ProcessHandler::isActive()){
	$logger->error( "banBot already running!" );
}else{
	ProcessHandler::activate();
	processTemporaryBans();
	processBans();
	processUnbans();
} #end if


$logger->debug( "$caller_short __END__" );
?>
