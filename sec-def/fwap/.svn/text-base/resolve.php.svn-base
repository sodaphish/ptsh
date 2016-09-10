<html>
<head>
	<title>FWAP DNS Resolution</title>
</head>
<body>

<font face="Verdana, Helvetica, Arial" size=-1>


<?php

error_reporting( 0 );

if( $query )
{
	//do the work!

	print "<h2>Results for $query</h2><hr>"; 
	print "<pre>\n"; 
	$resolve = gethostbyaddr( $query ); 
	if( ! $resolve ) 
	{
		$resolve = gethostbyname( $query );
	}

	if( $resolve )
	{ 
		print "$query => ". $resolve;
	} else {
		print "<b>Error, no records found for $query.</b>\n";
	}

	print "</pre>\n"; 

	print "
	<form method=post action=resolve.php>
	<input type=text name=query value=\"$query\">
	<input type=submit value=\" >> \">
	<form>
	";

} else {
	//show the form...

	print "
	<H2>DNS Query Tool</h2><hr>
	<form method=post action=resolve.php>
	<input type=text name=query value=\"$query\">
	<input type=submit value=\" >> \">
	<form>
	";
}

?>


</font>

</body>
</html>
