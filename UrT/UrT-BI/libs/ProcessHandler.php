<?php
if (!defined ('PID') and defined( $rootdir ) )
{
	define( 'PID', "$rootdir/etc/".basename( $argv[0], ".php" ).".lock" );
} 

class ProcessHandler
{
	function isActive ()
	{
		$pid = ProcessHandler::getPID ();
		if ($pid == null)
		{
			$ret = false;
		} else {
			$ret = posix_kill ($pid, 0);
		}
		if ($ret == false)
		{
			ProcessHandler::activate ();
		}
		return $ret;
	}


	function activate ()
	{
		$pidfile = PID;
		$pid = ProcessHandler::getPID ();
		if ($pid != null && $pid == getmypid ())
		{
			return "Already running!\n";
		} else {
			$fp = fopen ($pidfile, "w+");
			if( $fp )
			{
				if (!fwrite ($fp, "<"."?php\n\$pid = ".getmypid ().";\n?".">"))
				{
					die ("Can not create pid file!\n");
				}
				fclose ($fp);
			} else {
				die ("Can not create pid file!\n");
			}
		}
	}

	function getPID ()
	{
		if (file_exists (PID))
		{
			require (PID);
			return $pid;
		} else {
			return null;
		}
	}

} #end ProcessHandler
?>
