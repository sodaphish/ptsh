<?php
include_once( "config.php" );

$f = $_GET['f'];
if( ! $f ){ $f = $_POST['f']; }
$logger->debug( "f: $f" );

$file = $_GET['file'];
if( ! $file ){ $file = $_POST['file']; }
$logger->debug( "file: $file" );
?>

<html>
<head>
	<title><?php print $siteTitle; ?> - Server Configuration Editor</title>
</head>
<body


<div align="center">
<h1>Under Construction</h1>
<table width=80% border=0>
<tr><td>

<?php

switch( $f )
{
	case 'save':
		break;
	case 'apply':
		#backup running config
		#upload new config
		#broadcast to server that we're restarting with config changes
		#restart server
		#check server status
		break;
	case 'edit':
		$fileQuery = "select serverip, serverftp from servers where servername='$file'"; 
		$fileResult = mysql_query( $fileQuery ) or $logger->error( mysql_error() );
		list( $ip, $ftp ) = mysql_fetch_row( $fileResult );
		preg_match("/ftp:\/\/(.*?):(.*?)@(.*?)(\/.*)/i", $ftp, $options);

		$fileToEdit = "$rootdir/configs/$ip" . "-" . $options[1] . "-config.txt";
		$logger->debug( "fileToEdit: $fileToEdit" );

		if( is_file( $fileToEdit ) )
		{
			print "<form method=post action=$caller>\n<input type=hidden name=f value=save>\n";
			print "<div align=Center>";
			print "<h1>" . stripslashes( $file ) . "</h1>";
			print "<textarea name=config rows=40 cols=50 wrap=soft>";
			print file_get_contents( "$fileToEdit" ); 
			print "</textarea><br/><div align=right>\n";
			print "<input type=submit value=\"Save\"></div></div></form>\n";
		} else {
			$logger->error( "Couldn't find $fileToEdit" );
			print "<h1>Error</h1><p>Couldn't find $fileToEdit</p>";
		}
		break;
	default:
		print "<form method=post action=$caller><input type=hidden name=f value=edit>";
		print "<select name=file>\n";
		$dropDownQuery = "select servername, serverip, serverftp from servers";
		$dropDownResult = mysql_query( $dropDownQuery ) or $logger->error( mysql_error() );
		while( list( $name, $ip, $ftp ) = mysql_fetch_row( $dropDownResult ) )
		{
			preg_match("/ftp:\/\/(.*?):(.*?)@(.*?)(\/.*)/i", $ftp, $options);
			$user = $options[1];
			if( is_file( "$rootdir/configs/$ip-$user-config.txt" ) )
			{
				print "<option value=\"$name\">$name</option>";
			}
		}

		/*
		if( $dh = opendir( "$rootdir/configs" ) )
		{
			while( ( $fn = readdir( $dh ) ) !== false )
			{
				if( ! preg_match( "/^\./", $fn ) )
				{
					print "<option value=$fn>$fn</option>\n";
				}
			}
		}
		*/
		print "</select>\n<input type=submit value=\"Open\"></form>";
		
		break;
}

?>

</td></tr>
</table>
</div>

</body>
</html>

<?php
$logger->debug( "$caller_short __END__" );
?>
