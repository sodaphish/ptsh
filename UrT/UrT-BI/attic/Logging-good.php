<?php 
/*
Logging.php - by C.J. Steele <coreyjsteele@yahoo.com>
	(C)opyright 2006, C.J. Steele, all rights reserved.

This is a simple, unified logging interface class for PHP.

Sample usage: 
$logger = new Logging( "f", "testing.log" );
$logger->setLevel( "warn" );
$logger->debug( "This is a debug message" );
$logger->info( "This is an info message" );
$logger->warn( "This is a warn message" );
$logger->error( "This is an error message" );
$logger->critical( "This is a critical message" );

Which will produce the following entries in /path/to/filename:
2006-02-11 06:14:59 - WRN - This is a warning message
2006-02-11 06:14:59 - ERR - This is an error message
2006-02-11 06:14:59 - CRT - This is a critical message

*/

class Logging {

	private $session = "";
	private $level = 0;
	private $type = "file"; 
	private $filename = "";
	private $filedescripter = "";
	private $entryCount = 0;

	function __construct()
	{
		for( $x = 0; $x < 5; $x++ )
		{
			$this->session .= chr( rand( 65, 90 ) );
		}
		switch( func_get_arg(0) )
		{
			case 'f':
				//TODO: verify our descripter is good!!!
				$type="file"; 
				$this->filename = func_get_arg( 1 );
				if( ! $this->filedescripter = fopen( $this->filename, "a" ) )
				{
					print "E: couldn't open $this->filename for writing!\n";
					exit( 1 );
				}
				break;
			case 's':
				$type="stream";
				break;
		} //end switch

	} //end __construct()

	function __destruct ()
	{
		if( $this->type == "file" )
		{
			// close our filehandle if one is open.
			fclose( $this->filedescripter );
		} 
	} //end __destruct()

	function setLevel( $level )
	{
		$level = strtolower( $level ); 
		switch( $level )
		{
			case 'debug':
				$this->level=0; 
				break;
			case 'info':
				$this->level=1; 
				break;
			case 'warn':
				$this->level=2; 
				break;
			case 'error':
				$this->level=3; 
				break;
			case 'critical':
				$this->level=4; 
				break;
			default:
				$this->level=0; 
		} //end switch
	} //end setLevel()

	protected function outputHandler( $lvl, $text )
	{
		$output = sprintf( "%s - %s - %s - %s\n", strftime( "%G-%m-%d %H:%M:%S", time() ), $this->session, $lvl, $text ); 
		if( $this->type == "file" )
		{
			fwrite( $this->filedescripter, "$output" );
		} else {
			print "$output"; 
		}
		$this->entryCount++;
	} //end outputHandler()

	public function debug( $message )
	{
		if( $this->level <= 0 )
		{
			$this->outputHandler( "DBG", $message );
		}
	} //end debug() 

	public function info( $message )
	{
		if( $this->level <= 1  )
		{
			$this->outputHandler( "INF", $message );
		}
	} //end info()

	public function warn( $message )
	{
		if( $this->level <= 2 )
		{
			$this->outputHandler( "WRN", $message );
		}
	} //end warn()

	public function error( $message )
	{
		if( $this->level <= 3 )
		{
			$this->outputHandler( "ERR", $message );
		}
	} //end error()

	public function critical( $message )
	{
		if( $this->level <= 4 )
		{
			$this->outputHandler( "CRT", $message );
		}
	} //end critical()

	public function getsession()
	{
		return $this->session;
	} //end getsession()

} //end Logging class

?>
