<?php
/*
 * libs/rcon.php
 * 
 * TODO: find out where this came from, I know I tweaked it, but I cant remember where it came from
 */
/*
$q = new q3query('1.2.3.4', 27960);
$q->set_rconpassword('hello');
$q->rcon('addbot sarge 5');
print $q->get_response();
$q->rcon('status');
print $q->get_response();
$q->rcon('kick sarge');
print $q->get_response();
$q->rcon('status');
print $q->get_response();
*/

class q3query {
	private $rconpassword;
	private $fp;
	private $cmd;
	private $lastcmd;

	public function __construct($address, $port) {
		$this->cmd = str_repeat(chr(255), 4);
		$this->fp = fsockopen("udp://$address", $port, $errno, $errstr, 7);
		if (!$this->fp) die("$errstr ($errno)<br />\n");
	} //end __construct

	public function set_rconpassword($p) {
		$this->rconpassword = $p;
	} //end set_rconpassword()

	public function rcon($s) {
		sleep(1);
			$this->send('rcon '.$this->rconpassword.' '.$s);
	} //end rcon

	public function get_response($timeout=5) 
	{
		$s = '';
		$bang = time() + $timeout;
		while (!strlen($s) and time() < $bang) 
		{
			$s = $this->recv();
		} //end while
		if( substr( $s, 0, 4) != $this->cmd ) 
		{
		}
		return substr($s, 4);
	} //end get_response()

	private function send($string) {
		fwrite($this->fp, $this->cmd . $string . "\n");
	} //end send()

	private function recv() {
		return fread($this->fp, 9999);
	} //end recv()

} //end q3query

//EOF rcon.php
?>
