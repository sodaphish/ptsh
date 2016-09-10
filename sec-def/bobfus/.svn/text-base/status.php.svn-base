<html>
<head>
	<title>bobfus - the Binary OBFUScator</title>
</head>
<body>

<div align="center">
<table width="580">

<?php

if( $transaction )
{
	#insert the job into the database...
	$link = mysql_connect( "localhost", "root", "ahh-ahs" ) or die( mysql_error() );
	mysql_select_db( "bobfus" ) or die( mysql_error() );

	$q = "select reqtime, url, email, status from submissions where sn='$transaction'";
	$query_h = mysql_query( $q ) or die( mysql_error() );
	list( $reqtime, $url, $email, $status ) = mysql_fetch_row( $query_h );

	$statusMsg = "";
	# 3 - downloading
	# 2 - downloaded but unprocessed
	# 1 - processed successfully
	# 0 - unchanged since submission
	# -1 - retrieval error
	# -2 - url error, probably an attempt to poison our stuff.
	switch( $status ) 
	{
		case( 3 ):
			$statusMsg = "Your file is downloading.";
			break;
		case( 2 ):
			$statusMsg = "Your file has been downloaded but has not been encrypted.";
			break;
		case( 1 ):
			$statusMsg = "Your file is ready to go, check your e-mail for the pickup URL!";
			break;
		case( 0 ):
			$statusMsg = "Your file has not yet been processed.";
			break;
		case( -1 ):
			$statusMsg = "There was a problem with your URL, we've given up.";
			break;
		case( -2 ):
			$statusMsg = "Your URI/URL was malformed, your submission has been flagged for review -- attempts to abuse the system will be pursued.";
			break;
	}

	print "
	<tr><td>
	<h1>bobfus status</h1>

	<p><strong>Transaction #$transaction:</strong><br><blockquote><strong>Submitted:</strong> $reqtime <br><strong>URL:</strong> $url <br><strong>E-mail:</strong> $email <br><strong>Status:</strong> <i>$statusMsg</i> </blockquote></p>

	</td></tr>
	";

} else {
?>

<tr><td colspan="2">
<h1>bobfus status</h1>
<p>Use this form to check the status of your <b>bobfus</b> transaction.</p>

<hr>
</td></tr>

<form action="status.php" method="post">
<tr><td>Transaction #:</td><td><input size="16" type="text" value="" name="transaction"></td></tr>
<tr><td colspan="2" align="right"><input type="submit" value="Check it!"></td></tr>
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

