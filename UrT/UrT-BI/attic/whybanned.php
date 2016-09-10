<html>
<head>
	<title>|ALPHA| Ban Inquiry</title>
</head>
<body>


<p>This is a crude list of the people who have been banned from our servers so that when they inquire as to why they've been banned, we can tell them.</p>

<hr>

<pre>
<?php

passthru( 'cat phpban.txt | grep INF | grep BANNING | awk {\'print $1 " " $2 " " $9 " " $11 " " $12 " " $13 " " $14 " " $15 " " $16\'}' );

?>
</pre>

</body>
</html>
