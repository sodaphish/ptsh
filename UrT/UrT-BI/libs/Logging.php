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
 * NOTE: the following example isn't exactly correct.
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
	private $backTrace = array();


	/*
	 * __construct()
	 * the Logger class constructor
	 */
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
			//TODO: add a case for 'd' that writes to a dtatabase so we don't have to log to a file.
			case 's':
				$type="stream";
				break;
		} //end switch
	} //end __construct()


	/*
	 * __destruct()
	 * the class destructor
	 */
	function __destruct ()
	{
		if( $this->type == "file" )
		{
			// close our filehandle if one is open.
			fclose( $this->filedescripter );
		} 
	} //end __destruct()


	/*
	 * setLevel()
	 * is a public function that sets the Log level.
	 */
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


	/*
	 * outputHandler()
	 * this is the function that does the actual work of getting the log written to whatever output stream its supposed to be at.
	 */
	protected function outputHandler( $lvl, $text )
	{
		$output = sprintf( "%s - %s - %s - %s\n", strftime( "%G-%m-%d %H:%M:%S", time() ), $this->session, $lvl, $text );
		array_push( $this->backTrace, $output );
		if( $this->type == "file" )
		{
			fwrite( $this->filedescripter, "$output" );
		} elseif( $this->type == "mysql" ){
			//TODO: write this.
		} else {
			//write to STDOUT
			print "$output"; 
		}
		$this->entryCount++;
	} //end outputHandler()


	/*
	 * debug()
	 * makes a debug log entry to the outputHandler()
	 */
	public function debug( $message )
	{
		$bt = debug_backtrace(); $path = $bt[1]['file'] . "(" . $bt[1]['line'] . "):" . $bt[1]['function'] . " - "; 
		if( $this->level <= 0 )
		{
			$this->outputHandler( "DBG", "$path $message" );
		}
	} //end debug() 


	/*
	 * info()
	 * makes a info log entry to the outputHandler()
	 */
	public function info( $message )
	{
		$bt = debug_backtrace(); $path = $bt[1]['file'] . "(" . $bt[1]['line'] . "):" . $bt[1]['function'] . " - "; 
		if( $this->level <= 1  )
		{
			$this->outputHandler( "INF", "$path $message" );
		}
	} //end info()


	/*
	 * warn()
	 * makes a warning log entry to the outputHandler()
	 */
	public function warn( $message )
	{
		$bt = debug_backtrace(); $path = $bt[1]['file'] . "(" . $bt[1]['line'] . "):" . $bt[1]['function'] . " - "; 
		if( $this->level <= 2 )
		{
			$this->outputHandler( "WRN", "$path $message" );
		}
	} //end warn()


	/*
	 * error()
	 * makes a standard log entry to the outputHandler()
	 */
	public function error( $message )
	{
		$bt = debug_backtrace(); $path = $bt[1]['file'] . "(" . $bt[1]['line'] . "):" . $bt[1]['function'] . " - "; 
		if( $this->level <= 3 )
		{
			$this->outputHandler( "ERR", "$path $message" );
		}
	} //end error()


	/*
	 * critical()
	 * makes a critical log entry to the outputHandler()
	 */
	public function critical( $message )
	{
		$bt = debug_backtrace(); $path = $bt[1]['file'] . "(" . $bt[1]['line'] . "):" . $bt[1]['function'] . " - "; 
		if( $this->level <= 4 )
		{
			$this->outputHandler( "CRT", "$path $message" );
		}
	} //end critical()


	/*
	 * getsession()
	 * returns the value of $this->session
	 */
	public function getsession()
	{
		return $this->session;
	} //end getsession()
	
	
	
	/*
	 * getBacktrace()
	 * returns the value of the private array $backTrace
	 */
	public function getBacktrace()
	{
		return( $this->backTrace );
	} //end getBacktrace()
	
	
	/*
	 * showBacktrace()
	 * prints to STDOUT the value of the private array $backTrace
	 * 
	 * Takes one argument, that defins the format, there are three:
	 * 	- plain (default) -- just prints the output straight
	 *  - html -- prints formatted HTML
	 *  - xml -- prints each line as an attribute of an xml file.
	 */
	 public function showBacktrace( $format = "plain" )
	 {
	 	if( preg_match( '/html/i', $format ) )
	 	{
	 		// TODO: this is an HTML output request, print the necessary headers
	 	} elseif( preg_match( '/xml/i', $format ) ){
	 		// TODO: this is an XML output request, print the necessary headers
	 	} //end if
	 	
	 	
	 	foreach( $this->backTrace as $bt )
	 	{
		 	if( preg_match( '/html/i', $format ) )
		 	{
		 		// TODO: print the output for the log entry in HTML
				print "$bt<br/>\n";
		 	} elseif( preg_match( '/xml/i', $format ) ){
		 		// TODO: print the output for the log entry in XML
		 	} else {
		 		print "$bt\n";
		 	}//end if	 		
	 	} //end foreach
	 	
	 	
	 	if( preg_match( '/html/i', $format ) )
	 	{
	 		// TODO: this is an HTML output request, print the necessary footers
	 	} elseif( preg_match( '/xml/i', $format ) ){
	 		// TODO: this is an XML output request, print the necessary footers
	 	} //end if
	 } //end showBacktrace()

} //end Logging class

//EOF Logging.php
?>
