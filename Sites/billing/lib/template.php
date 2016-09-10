<?php

function internalError( $headline, $body )
{
	print "<hr><h1>$headline</h1> <p>$body</P><hr>\n";
}

function listBox( $title, $inArray )
{
	print "
		<table border=1>
		<tr>
			<td align=center bgcolor=#ababab>
			<b>$title</b>
			</td>
		</tr>
		<tr>
			<td align=center>
	";

	foreach( $inArray as $a )
	{
		print "$a<br>\n";
	}

	print "
			</td>
		</tr>
		</table>
		<br>
	";
}

?>
