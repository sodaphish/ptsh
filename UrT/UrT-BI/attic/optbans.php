<html>
<head>
	<title>|WC| banlist Optimizer</title>
</head>
<body>

<div align=center>
<table width="600" border="0">

<?php
if( is_file( $_FILES['file']['tmp_name'] ) ) 
{

	print "<tr><td><b>Original banlist</b></td><td><b>Optimized banlist</b></td></tr>";
	$string = "./optbans.pl " . $_FILES['file']['tmp_name']; 
	print "<tr><td valign=top><pre>";
	$string2 = "cat " . $_FILES['file']['tmp_name'];
	passthru( "$string2" );
	print "</pre></td><td valign=top><pre>";
	passthru( "$string" );
	print "</pre></td></tr>";

} else {
?>

<tr><td>
<p>Upload an unoptimized banlist.txt file and we'll output the optimized version</p>
<p><b>There's an 8.3MB file-size limit.</b></p>
<form enctype="multipart/form-data" method=post action=optbans.php>
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
