<html>
<head>
	<title>|ALPHA| Game Log Parser - Users</title>
</head>
<body>

<div align=center>
<table width="600" border="0">

<?php
if( is_file( $_FILES['file']['tmp_name'] ) ) 
{

	$string = "./shusers.pl " . $_FILES['file']['tmp_name']; 
	exec( $string, &$output );
	print "<tr><td bgcolor=#aaaaaa><b>Name</b></td><td bgcolor=#aaaaaa><b>IP</b></td><td bgcolor=#aaaaaa><b>GUID</b></td></tr>\n";
	$count = 0;
	foreach( $output as $line )
	{
		list( $name, $ip, $guid ) = preg_split( "/\\\/", $line );
		if( $count % 2 )
		{
			print "<tr><td>$name</td><td>$ip</td><td>$guid</td></tr>\n";
		} else {
			print "<tr><td bgcolor=#cccccc>$name</td><td bgcolor=#cccccc>$ip</td><td bgcolor=#cccccc>$guid</td></tr>\n";
		}
		$count += 1; 
	}

} else {
?>

<tr><td>
<p>Upload a file that you'd like to see the users along with IP's and GUID's.  Typically this is a games.log file.</p>
<p><b>There's an 8.3MB file-size limit.</b></p>
<form enctype="multipart/form-data" method=post action=shusers.php>
	<input type="hidden" name="MAX_FILE_SIZE" value = "8380000">
	<input name="file" type="file"><br /><input type="submit" value="&gt; &gt;">
</form>
</td></tr>

<?php
} //end if
?>

</table>
</div>

</body>
</html>
