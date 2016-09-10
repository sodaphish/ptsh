<html>
<head>
	<title>FWAP Shun</title>
</head>
<body>

<font face="Verdana, Helvetica, Arial" size=-1>


<?php

$fwappath = "/var/www/html/sec/fwap2"; 

error_reporting( 0 );

$rmtref = getenv( "HTTP_REFERER" );

print $rmtref;
exit; 

if( $query )
{
	//do the work!

	print "<h2>Shun Tool: Shunning $query</h2>"; 
	print "<pre>\n"; 
	$output =  shell_exec( "$fwappath/bin/dpixsh shun $query" );
	print $output; 
	print "</pre>\n"; 

	print "
	<hr>
	<form method=post action=shun.php>
	<input type=text name=query value=\"$query\">
	<input type=submit value=\" >> \">
	<form>
	";

} else {
	//show the form...

	print "
	<H2>Shun Tool</h2><hr>
	<form method=post action=shun.php>
	<input type=text name=query value=\"$query\">
	<input type=submit value=\" >> \">
	<form>
	";
}

?>


</font>

</body>
</html>
