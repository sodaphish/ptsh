#!/usr/bin/php -q
<?php

include_once( "/var/www/config.php" );

$d = dir( "$rootdir/gamelogs/" );
while( $de = $d->read() )
{
	if( preg_match( "/\.log$/", $de ) )
	{
		processFile( "$rootdir/gamelogs/$de" );
	}
}


$logger->debug( "$caller_short __END__" );


function processFile( $logfile )
{
	global $logger;

	if( file_exists( $logfile ) )
	{
		$logger->debug( "$logfile exists" );
	}
	
	$results = array();
	$f = fopen( $logfile, "r" );
	if( $f )
	{
		$logger->info( "$logfile successfully opened." );
	}
	while( $line = fgets( $f ) )
	{
		$line = chop( $line );
		$line = trim( $line );
	
		list( $time, $command, $slot, $bits ) = preg_split( "/\ /", $line, 4 );
	
		if( preg_match( "/ClientUserinfo\:/", $command ) )
		{
	
			$key = "";
			$in = 1;
			$options = array();
	
			foreach( preg_split( "/\\\/", $bits ) as $v )
			{
				if( $in )
				{
					$options["$key"] = $v;
					$in = 0;
				} else {
					$key = $v;
					$in = 1;
				} #end if
			} 
	
			# strip spaces in player names
			$options["name"] = preg_replace( "/\s/", "", $options["name"] );
			$options["ip"] = preg_replace( "/\:.[0-9]*/", "", $options["ip"] );
	
			array_push( $results, $options["name"] . " " . $options["ip"] . " " . $options["cl_guid"] );
		} #end if
	} #end while
	fclose( $f ); 
	
	$logger->debug( "there are " . count( $results ) . " entries in the file before pruning" );
	$new_results = array_unique( $results );
	$logger->debug( "there are " . count( $new_results ) . " entries in the file AFTER pruning" );
	
	foreach( $new_results as $line )
	{
		list( $name, $ip, $guid ) = preg_split( "/\ /", $line, 3 );
		#$query = "SELECT guid FROM `ips` WHERE ip = '$ip' AND name = '$name'"
		#print "variabels: $name, $ip, $guid\n";
		$qq = "select guid from ips where ip = '$ip' and name = '$name'"; 
		#$logger->debug( "guid query: $qq" ); 
		$res = mysql_query( $qq );
		list( $g ) = mysql_fetch_row( $res );
		if( $g == $guid ) 
		{
			#skip this one
			$logger->debug( "skipping $name $ip $guid" );
		} else {
			#inser this one
			$insert = "insert into ips ( ip, name, guid ) values ( '$ip', '$name', '$guid' )";
			$result = mysql_query( $insert );
			if( $result and mysql_insert_id() )
			{
				$logger->debug( "inserting $name $ip $guid" );
			} else {
				$logger->error( "failed to insert $name $ip $guid (" . mysql_error() . ")" );
			}
		} #end if
	} #end foreach
} #end processFile()
	

?>
