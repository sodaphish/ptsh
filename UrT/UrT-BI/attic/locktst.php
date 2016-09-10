#!/usr/bin/php -q
<?
include_once( "/var/www/config.php" );
$lockFile = "$rootdir/etc/banBot.lock";



function lockBanBot( $lock )
{
	if( file_exists( $lock ) )
	{
		return -1;
	} 
	if( is_file( $lock ) and ! is_link( $lock )  and is_writeable( $lock ) )
	{
		$fh = fopen( $lock, "w" );
		if( fwrite( $fh, getmypid() ) )
		{
			fclose( $fh );
			return 1;
		} #end if
	} #end if
	return 0;
} #end lockBanBot()



function unlockBanBot( $lock )
{
	if( ! file_exists( $lock ) )
	{
		return -1;
	}
	$fh = fopen( $lock, "r" );
	$storedPid = fgets( $fh );
	fclose( $fh );

	$mypid = getmypid();
	if( $mypid == $storedPid )
	{
		if( unlink( $lock ) )
		{
			print "here.";
			return 1;
		} #end if
	} #end if
	return 0;
} #end unlockBanBot()

while( 1 )
{
	print "lock: " . lockBanBot( $lockFile ) . "\n";
	print "unlock: " . unlockBanBot( $lockFile ) . "\n";
}


$logger->error( "$caller_short __END__" );
?>
