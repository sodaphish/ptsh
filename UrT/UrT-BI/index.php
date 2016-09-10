<?php
/*
 * index.php
 * by C.J. Steele <coreyjsteele@gmail.com>
 * http://sodaphish.com
 *
 * (C)opyright 2009, Corey J. Steele, all rights reserved.
 *
 * Created September, 2009
 *
 * This is the controller for all pages.  Mostly.
 */
include_once( "config.php" );
?>
<html>
<head>
	<title><?php print $siteTitle; ?></title>
</head>
<frameset rows="135,*,42" border=0>
	<frame name="_top" src="newMenu.php" />
	<frame name="_middle" src="motd.php" />
	<frame name="_bottom" src="bottom.php" />
</frameset>
</html>
<?php
$logger->debug( "$caller_short __END__" ); 
?>