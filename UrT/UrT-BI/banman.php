<?php 
include_once( "config.php" );
if( ! $privlevel__ ){ header( "location: fail.php" ); }
?>
<html>
<head>
	<title><?php print $siteTitle; ?> - Backend Management</title>
</head>
<body>

<?php

$module = $_GET{'module'};
if( ! $module ){ $module = $_POST{'module'}; }
$logger->debug( "module: $module" );
$function = $_GET{'function'};
if( ! $function ){ $function = $_POST{'function'}; }
$logger->debug( "function: $function" );

$motdBody = $_GET{'motdBody'};
if( ! $motdBody ){ $motdBody = $_POST{'motdBody'}; }
$logger->debug( "motdBody: $motdBody" );

switch( $module ){
	case "motd":
		$logger->debug( "in the motd module" );
		if( $motdBody )
		{
			$motdQuery = "insert into motd ( motdAuthor, motdBody ) values ( '$username__', '$motdBody' )";
			$logger->debug( "$motdQuery" );
			$motdQueryResult = mysql_query( $motdQuery ) or $logger->error( mysql_error() );
			print "<strong>MOTD entry added.</strong>\n";
		} else {
			$logger->error( "$username__ is a retard because they posted a MOTD without any MOTD." );
		}
		break;	
	case "srvr":
		if( $function == "delete" ){
			$sid = $_GET{'sid'};
			if( ! $sid ){ $srvrname = $_POST{'sid'}; }
			$query = "delete from servers where sid = $sid";
			$result = mysql_query( $query );
			if( $result )
			{
				print "<strong>Server deleted</strong>\n";
			} else {
				print mysql_error();
				print "<strong>Oops!  Something went wrong.</strong>\n";
			}
		} elseif( $function == "add" ){
			//add-specific get/post variables
			$srvrname = $_GET{'srvrname'};
			if( ! $srvrname ){ $srvrname = $_POST{'srvrname'}; }
			$srvrip = $_GET{'srvrip'};
			if( ! $srvrip ){ $srvrip = $_POST{'srvrip'}; }
			$srvrport = $_GET{'srvrport'};
			if( ! $srvrport ){ $srvrport = $_POST{'srvrport'}; }
			$srvrrcon = $_GET{'srvrrcon'};
			if( ! $srvrrcon ){ $srvrrcon = $_POST{'srvrrcon'}; }
			$srvrftp = $_GET{'srvrftp'};
			if( ! $srvrftp ){ $srvrftp = $_POST{'srvrftp'}; }
			$srvrlog = $_GET{'srvrlog'};
			if( ! $srvrlog ){ $srvrlog = $_POST{'srvrlog'}; }

			if( $srvrname and $srvrip and $srvrport and $srvrrcon and $srvrftp and $srvrlog )
			{
				$insert = "insert into servers ( servername, serverip, serverport, serverrcon, serverftp, serverlog ) values ( '$srvrname', '$srvrip', '$srvrport', '$srvrrcon', '$srvrftp', '$srvrlog' )";
				$result = mysql_query( "$insert" );
				$sid = mysql_insert_id();
				if( $sid ){  
					print "<strong>Added server</strong>\n";
				} else {
					print "<strong>Oops! Something went wrong.</strong>\n";
				}
			} else {
				print "add server error: not all parameters completed.";
			}
		} else {
			print "Unknown function"; 
		}
		break;
	case "usrs":
		/*
hbc(~/mine/wc)# htpasswd
Usage:
        htpasswd [-cmdpsD] passwordfile username
        htpasswd -b[cmdpsD] passwordfile username password

        htpasswd -n[mdps] username
        htpasswd -nb[mdps] username password
 -c  Create a new file.
 -n  Don't update file; display results on stdout.
 -m  Force MD5 encryption of the password.
 -d  Force CRYPT encryption of the password (default).
 -p  Do not encrypt the password (plaintext).
 -s  Force SHA encryption of the password.
 -b  Use the password from the command line rather than prompting for it.
 -D  Delete the specified user.
On Windows, NetWare and TPF systems the '-m' flag is used by default.
On all other systems, the '-p' flag will probably not work.
		*/
		if( $function == "add" ){
			$username = $_GET{'username'};
			if( ! $username ){ $username = $_POST{'username'}; }
			$password = $_GET{'password'};
			if( ! $password ){ $password = $_POST{'password'}; }
			if( $username and $password )
			{
				$insert = "insert into users ( username, password ) values ( '$username', '$password' )";
				$result = mysql_query( $insert );
				$id = mysql_insert_id();
				if( $id )
				{
					echo shell_exec( "/usr/bin/htpasswd -b $rootdir/.pass $username $password" );
					#echo exec( "/usr/bin/htpasswd /var/www/.pass -b $username $password" );
					print "<strong>Added user: $username</strong>";
				} else {
					print mysql_error();
				}
			} else {
				print "add user error: not all parameters provided.";
			}
		} elseif( $function == "delete" ){
			$uid = $_GET{'uid'};
			if( ! $uid ){ $uid = $_POST{'uid'}; }
			$query = "select username from users where uid = $uid";
			$result = mysql_query( $query ); 
			list( $username ) = mysql_fetch_row( $result );
			
			$delete = "delete from users where uid = $uid";
			$result = mysql_query( $delete );
			if( $result )
			{
				echo shell_exec( "/usr/bin/htpasswd -D $rootdir/.pass $username" );
				print "<strong>User deleted</strong>";
			} else {
				print mysql_error();
			}
		} elseif( $function == "promote" ){
			if( $privlevel__ > 1 )
			{
				$uid = $_GET{'uid'};
				if( ! $uid ){ $uid = $_POST{'uid'}; }
				$query = "select privlevel from users where uid = $uid";
				$result = mysql_query( $query );
				list( $privlevel ) = mysql_fetch_row( $result );
				$privlevel++;
				$update = "update users set privlevel=$privlevel where uid = $uid";
				$result = mysql_query( $update );
				if( $result )
				{
					print "<strong>Privilege level set.</strong>\n";
				} else {
					print mysql_error();
				}
			} else {
				print "<strong>Sorry mate, you're not authorized to promote users...</strong>\n";
			}

		} elseif( $function == "demote" ){
			if( $privlevel__ > 1 )
			{
				$uid = $_GET{'uid'};
				if( ! $uid ){ $uid = $_POST{'uid'}; }
				$query = "select privlevel from users where uid = $uid";
				$result = mysql_query( $query );
				list( $privlevel ) = mysql_fetch_row( $result );
				$privlevel--;
				$update = "update users set privlevel=$privlevel where uid = $uid";
				$result = mysql_query( $update );
				if( $result )
				{
					print "<strong>Privilege level set.</strong>\n";
				} else {
					print mysql_error();
				}
			} else {
				print "<strong>Sorry mate, you're not authorized to promote users...</strong>\n";
			}

		} else {
			print "Unkown function";
		}
		break;
}
?>

<div align="center">
<table width="80%" border="1">
<tr><td colspan=2>

<h2>MOTD Announcement</h2>
<div align=Center>
<form method=get action=<?php print $caller; ?>>
<input type=hidden name=module value="motd">
<textarea name=motdBody wrap=soft rows=10 cols=80></textarea><br/>
</div>
<div align=right>
<input type=submit>
</div>
</form>

</td></tr>
<tr>
<td valign="top" width="75%%">
	<h2>Servers</h2>
	<blockquote>
	<?php
		$query = "select sid, servername, serverip, serverport, serverrcon, serverftp, serverlog from servers";
		$result = mysql_query( $query ); 
		while( list( $id, $name, $ip, $port, $rcon, $ftp, $log ) = mysql_fetch_row( $result ) )
		{
			if( $privlevel__ > 1 )
			{
				print "<li><strong>$name</strong> ($ip:$port)<br/><a href=\"$ftp/$log\">$ftp/$log</a><br/><strong>rcon:</strong> $rcon<br/></li>";
			} else {
				print "<li><strong>$name</strong> ($ip:$port)<br/><strong>rcon:</strong> $rcon<br/></li>";
			}
		}
	?>
	</blockquote>
</td>

<td valign="top" width="25%">
	<h2>Users</h2>
	<blockquote>
	<?php
		$query = "select username, privlevel from users order by username";
		$result = mysql_query( $query );
		if( $result )
		{
			while( list( $u, $p ) = mysql_fetch_row( $result ) )
			{
				if( $p == 1)
				{ 
					print "<li>$u (super)</li>\n";
				} elseif( $p > 1 ){
					print "<li>$u (admin)</li>\n";
				} else {
					print "<li>$u</li>\n";
				}
			}
		} else {
			print mysql_error();
		}
	?>
	</blockquote>
</td>

</tr>
<tr><td colspan="2">

<div align="center">
<strong><big>DELETE A SERVER</big></strong><br/>
<form action="banman.php" method="get">
<input type="hidden" name="module" value="srvr">
<input type="hidden" name="function" value="delete">
<select name="sid">
	<?php
		$query = "select sid, servername from servers";
		$result = mysql_query( $query );
		while( list( $id, $name ) = mysql_fetch_row( $result ) )
		{
			print "<option value=\"$id\">$name</option>\n";
		}
	?>
</select>
<input type="submit" value="&gt; &gt;">
</form>
</div>

<hr>

<div align="center">
<strong><big>ADD A SERVER</big></strong><br/>
<form action="banman.php" method="post">
<input type="hidden" name="module" value="srvr">
<input type="hidden" name="function" value="add">
<table border="0">
<tr><td align="right"><strong>Server Name</strong></td><td><input type="text" name="srvrname"></td></tr>
<tr><td align="right"><strong>IP</strong></td><td><input type="text" name="srvrip"></td></tr>
<tr><td align="right"><strong>Port</strong></td><td><input type="text" value="27960" name="srvrport"></td></tr>
<tr><td align="right"><strong>RCON Password</strong></td><td><input type="text" name="srvrrcon"></td></tr>
<tr><td align="right"><strong>FTP URL</strong></td><td><input size="45" type="text" name="srvrftp" value="ftp://user:password@host/directory/to/config/directory"></td></tr>
<tr><td align="right"><strong>Games Log file</strong></td><td><input size="45" type="text" name="srvrlog" value="games.log"></td></tr>
<tr><td colspan="2"><input type="submit" value="&gt; &gt;"></td></tr>
</table>
</form>
</div>

<hr>

<div align="center">
<strong><big>DELETE A USER</big></strong><br/>
<form action="banman.php" method="post">
<input type="hidden" name="module" value="usrs">
<input type="hidden" name="function" value="delete">
<select name="uid">
	<?php
		$query = "select uid, username, privlevel from users order by username";
		$result = mysql_query( $query );
		while( list( $id, $name, $priv ) = mysql_fetch_row( $result ) )
		{
			if( $priv )
			{
				print "<option value=\"$id\">$name (super)</option>\n";
			} else {
				print "<option value=\"$id\">$name</option>\n";
			}
		}
	?>
</select>
<input type="submit" value="&gt; &gt;">
</form>
</div>

<hr>

<div align="center">
<strong><big>PROMOTE A USER</big></strong><br/>
<form action="banman.php" method="post">
<input type="hidden" name="module" value="usrs">
<input type="hidden" name="function" value="promote">
<select name="uid">
	<?php
		$query = "select uid, username, privlevel from users order by username";
		$result = mysql_query( $query );
		while( list( $id, $name, $priv ) = mysql_fetch_row( $result ) )
		{
			if( $priv == 1 )
			{
				print "<option value=\"$id\">$name (super)</option>\n";
			} elseif( $priv > 1 ){
				print "<option value=\"$id\">$name (admin)</option>\n";
			} else {
				print "<option value=\"$id\">$name</option>\n";
			}
		}
	?>
</select>
<input type="submit" value="&gt; &gt;">
</form>

<strong><big>DEMOTE A USER</big></strong><br/>
<form action="banman.php" method="post">
<input type="hidden" name="module" value="usrs">
<input type="hidden" name="function" value="demote">
<select name="uid">
	<?php
		$query = "select uid, username, privlevel from users order by username";
		$result = mysql_query( $query );
		while( list( $id, $name, $priv ) = mysql_fetch_row( $result ) )
		{
			if( $priv == 1 )
			{
				print "<option value=\"$id\">$name (super)</option>\n";
			} elseif( $priv > 1 ){
				print "<option value=\"$id\">$name (admin)</option>\n";
			} else {
				print "<option value=\"$id\">$name</option>\n";
			}
		}
	?>
</select>
<input type="submit" value="&gt; &gt;">
</form>
</div>
<hr>

<div align="center">
<strong><big>ADD A USER</big></strong><br/>
<form action="banman.php" method="post">
<input type="hidden" name="module" value="usrs">
<input type="hidden" name="function" value="add">
<table border="0">
<tr><td><strong>Username</strong></td><td><input type="text" name="username"></td></tr>
<tr><td><strong>Password</strong></td><td><input type="text" name="password"></td></tr>
<tr><td colspan="2"><input type="submit" value="&gt; &gt;"></td></tr>
</table>
</form>
</div>

</td></tr>
</table>
</div>

</body>
</html>

<?php $logger->debug( "$caller_short __END__" ); ?>
