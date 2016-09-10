<html>
<head>
	<title>bobfus - the Binary OBFUScator</title>
</head>
<body>

<div align="center">
<table width="580">

<?php

function mkSerialNumber()
{
	$sn = "";
	for( $x = 0; $x < 16; $x++ )
	{
		$r = rand( 0, 9 );
		if( $x == 0 and $r == 0 )
		{
			$r++;
		}
		$sn .= $r;
	}
	return $sn;
} #end mkSerialNumber()


function scrubEmail( $email )
{
	# adapted from http://phpsec.org/projects/guide/1.html#1.4.3
	$email_pattern = '/^[^@\s<&>]+@([-a-z0-9]+\.)+[a-z]{2,}$/i';
	if( preg_match( $email_pattern, $email ) ) 
	{ 
	    return $email;
	} else {
		return -1;
	}
} #end scrubEmail()


function scrubURL( $url )
{
	# url's need to be limited to those that begin with http:// and ftp://
	$in = strip_tags( $url );
	if( preg_match( "/^(http|ftp)+(:\/\/)+[a-z0-9]+\.[a-z0-9]/", $in ) )
	{
		return $in;
	} else {
		#fails basic check.
		#print "$in\n<br>\n";
		return -1;
	}
} #end scrubURL()


function scrubPasswd( $passwd )
{
	# limit to 16 characters
	if( preg_match( "/^[a-zA-Z0-9!-_]{2,16}$/", $passwd ) )
	{
		# we have just allowed characters
		return $passwd;
	} else {
		#print "$passwd\n<br>\n";
		return -1;
	}
} #end scrubPasswd()


if( $url and $email and $passwd )
{
	#insert the job into the database...
	$link = mysql_connect( "localhost", "root", "ahh-ahs" ) or die( mysql_error() );
	mysql_select_db( "bobfus" ) or die( mysql_error() );
	$now = date( DATE_RFC822 );
	$ip = getenv( 'REMOTE_ADDR' );
	$serialNumber = mkSerialNumber(); 

	$url = scrubURL( $url ); 
	$email = scrubEmail( $email ); 
	$passwd = scrubPasswd( $passwd );

	if( $url and $email and $passwd )
	{
		$ins = "insert into submissions ( reqtime, ipadd, url, email, passwd, sn ) values ( now(), '$ip', '$url', '$email', '$passwd', '$serialNumber' )";
		mysql_query( $ins ) or die( mysql_error() );
		print "
	<tr><td>
	<h1>bobfus</h1>
	<p><b>Success!</b> ...your job has been submitted.  You\'ll get an e-mail when we've completed the download or if we encounter any problems with the process (i.e. file-size limits, excessive submissions, errors like 404\'s, etc.).</p>
	<p>Your transaction number is: #$serialNumber.  You can check the status of your transaction at the <a href=\"status.php\">status page</a>.</p>
	<p>Ciao.</p>
	</td></tr>
		";
	} else {
		print "
	<tr><td>
	<h1>bobfus</h1>
	<p><b>FAILED!</b> ...your submission (originating from $ip) didn't pass our taint checking, apparently.  We will review your submission at our soonest convenience.</p>
	<p>Ciao.</p>
	<pre>
	$url
	$email
	$passwd
	</pre>
	</td></tr>
		";
	}

} else {
?>

<tr><td colspan="2">
<h1>bobfus</h1>
<p><b>bobfus</b> is short for the <b>B</b>inary <B>OBFUS</b>cator; it is a cryptographic obfuscator that uses the Rijndael (AES) algorithm to obscure the true nature of the file being downloaded (primarily to defeat upstream content and antivirus filters.)  To decrypt bobfuscated files you'll need to download `<a href="../files/bobfus.pl">bobfus.pl</a>`.</p>
<p>How this works is relatively simple...<ol><li>Complete the form below (only http and ftp files, alpha-numeric passwords, etc.).</li><li>Wait while we download and bobfuscate your file.</li><li>You'll get an e-mail with the URL to the bobfuscated file.</li><li>You download the bobfuscated file.</li><li>You unbobfuscate the file using `bobfus.pl`.</li><li>We delete your bobfuscated file.</li></ol>


<hr>
</td></tr>

<form action="index.php" method="post">
<tr><td>URL to retrieve:</td><td><input size="60" type="text" value="http://" name="url"></td></tr>
<tr><td>Your e-mail:</td><td><input type="text" size="30" name="email"></td></tr>
<tr><td>Password:</td><td><input type="password" size="8" name="passwd"> (don't forget this!!!)</td></tr>
<tr><td colspan="2" align="right"><input type="submit" value="Do it!"></td></tr>
</form>

<tr><td colspan="2">
<hr>
<small><div align="center">(c)opyright 2005, C.J. Steele, all rights reserved.</div></small>
</td></tr>

</table>
</div>

<?php
} #end if
?>


</body>
</html>

