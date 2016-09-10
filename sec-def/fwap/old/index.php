<?php
/* 
 * index.php v.1.0.0 by C.J. Steele <csteele@good-sam.com>
 * 
 */
?>

<html>
<head>
	<title>F.W.A.P.</title>
	<link rel="stylesheet" type="text/css" href="style.css" />
</head>
<script language=javascript>
<!--
function popupwindow( fileloc, winname, winwidth, winheight ) 
{ 
	windowbits = "height=" + winheight + ",width=" + winwidth + ",channelmode=0,dependent=0,directories=0,fullscreen=0,location=0,menubar=0,resizable=0,scrollbars=1,statusbar=0,toolbar=0"
	window.open( fileloc, winname, windowbits )
}
-->
</script>
<noscript>
	<h1>Error!</h1><p>This site requires JavaScript 2.0 or later.  If you have disabled JavaScript, please re-enable it and reload this page.  If your browser does not support JavaScript, please hit yourself with a blunt object.</P>
</noscript>
<body>

<?php

function yesterday(){
	//86400 seconds per day
	$yest = date( "M d Y", time()-86400 );
	return $yest; 
}

function getmicrotime(){ 
    list($usec, $sec) = explode(" ",microtime()); 
    return ( ( (float)$usec/1000 ) + (float)$sec);
} 

$url = "http://frank.corp.good-sam.com/sec/fwap2/old"; 
$this = "index.php";

$version = "2.0.0-beta"; 

$start_time = getmicrotime();

$query_count = 0;

$link = mysql_connect( "localhost", "root", "" );
mysql_select_db( "fw2" );

switch( $f ){

	case 'hdrill':
		if( $q )
		{

			print "<div align=center><a href=index.php><img src=$url/fwap.png border=0></a><br><table width=600 border=0><tr><td><h3>Host Drill-down - $q</h3>\n"; 

			$ct_q = "select count( id ) from blocked where src like '$q'"; 
			$ct_r = mysql_query( $ct_q ); 
			$query_count++;
			list( $ct ) = mysql_fetch_row( $ct_r ); 
			print "<b>$ct results displayed</b><br><br>\n";

			$host_q = "select time, date, proto, src, srcprt, dst, dstprt from blocked where src like '$q' order by date asc, time asc"; 
			$host_r = mysql_query( $host_q );
			$query_count++;
			while( list( $time, $date, $proto, $src, $srcprt, $dst, $dstprt ) = mysql_fetch_row( $host_r ) )
			{
				print "<li>$date $time $src $srcprt/$proto -> $dst $dstprt/$proto</li>\n";
			}

			print "</td></tr></table></div>\n";

		} else {
			print "<h3>Error!</h3><p>You need to specify a host to query!</p>"; 
		}
		
		break;
	case 'odrill':
		print "<div align=center><a href=index.php><img src=$url/fwap.png border=0></a><br><table width=600 border=0><tr><td><h3>Misc. Error Message Drilldown</h3>\n";

		if( $d )
		{
			$ct_q = "select count( id ) from others where message like '%$p%'";
			$ct_r = mysql_query( $ct_q );
			$query_count++;
			list( $ct ) = mysql_fetch_row( $ct_r );
			print "<p>$ct messages displayed.<p>"; 
			$odd_q = "select time, date, pixerror, message from others where message like '%$p%'"; 
			$odd_r = mysql_query( $odd_q );
			$query_count++;
			while( list( $t, $d, $e, $m ) = mysql_fetch_row( $odd_r ) )
			{
				print "$t $d $d $m<br>\n";
			}
		} else {
			// this is the date narrowing dialog...
			print "<p>Select a specific date to view from the dates available below.</p>\n";
			$dates_q = "select date from dddates"; 
			$dates_r = mysql_query( $dates_q );
			$query_count++;
			print "<form method=get action=$this><input type=hidden name=f value=odrill><input type=hidden name=p value=\"$p\">
				Show Date: <select name=d>";
			while( list( $dt ) = mysql_fetch_row( $dates_r ) )
			{
				print "<option value=\"$dt\">$dt</option>\n";
			}
			print "</select><input type=submit value=\"&gt; &gt;\"></form><hr>";
		}
		print "</td></tr></table></div>\n";
		break;

	case 'top10':
		print "<div align=center><a href=index.php><img src=$url/fwap.png border=0></a><br><table width=600 border=0><tr><td><h1>Top 10</h1>\n";

		print "<h2>All-time Top 10 Internal Offenders</h2>\n<ol>";
		$top10_int_q = "select distinct src, count(dst) as victims from blocked where src like '172.%' group by src order by victims desc limit 10"; 
		$top10_int_r = mysql_query( $top10_int_q ); 
			$query_count++;
		while( list( $ip, $ct ) = mysql_fetch_row( $top10_int_r ) )
		{
			print "<li><a href=$url/$this?f=drilldown&q=$ip>$ip</a> ($ct)</li>\n";
		}
		print "</ol>"; 

		print "<h2>All-time Top 10 External Offenders</h2>\n<ol>"; 
		$top10_ext_q = "select distinct src, count(dst) as victims from blocked where src not like '172.%' group by src order by victims desc limit 10"; 
		$top10_ext_r = mysql_query( $top10_ext_q ); 
			$query_count++;
		while( list( $ip, $ct ) = mysql_fetch_row( $top10_ext_r ) )
		{
			print "<li><a href=$url/$this?f=drilldown&q=$ip>$ip</a> ($ct)</li>\n";
		}
		print "</ol>"; 

		print "<h2>All-time Top 10 External Ports Attacked</h2>\n<ol>";
		$top10_attprt_q = "select distinct dstprt, proto, count( dstprt ) as attack_count from blocked where dst like '207.140.250.%' group by dstprt order by attack_count desc limit 10"; 
		$top10_attprt_r = mysql_query( $top10_attprt_q );
			$query_count++;
		while( list( $dstprt, $proto, $dstprt_ct ) = mysql_fetch_row( $top10_attprt_r ) )
		{
			print "<li>$dstprt/$proto ($dstprt_ct)</li>\n";
		}
		print "</ol>";

		print "<h2>All-time Top 10 Internal Ports Blocked</h2>\n<ol>";
		$top10_attprt_q = "select distinct dstprt, proto, count( dstprt ) as attack_count from blocked where src like '172.%' group by dstprt order by attack_count desc limit 10"; 
		$top10_attprt_r = mysql_query( $top10_attprt_q );
			$query_count++;
		while( list( $dstprt, $proto, $dstprt_ct ) = mysql_fetch_row( $top10_attprt_r ) )
		{
			print "<li>$dstprt/$proto ($dstprt_ct)</li>\n";
		}
		print "</ol>";
		print "</td></tr></table></div>\n";
		break;

	case 'drilldown':
		print "<div align=center><a href=index.php><img src=$url/fwap.png border=0></a><br><table width=600 border=0><tr><td>\n"; 
		if( $q ){

			print "<h3>$q - $d</h3>\n";

			$dates_q = "select date from dddates"; 
			$dates_r = mysql_query( $dates_q );
			$query_count++;
			print "<form method=get action=$this><input type=hidden name=f value=drilldown><input type=hidden name=q value=\"$q\">
				Show Date: <select name=d>";
			while( list( $dt ) = mysql_fetch_row( $dates_r ) )
			{
				print "<option value=\"$dt\">$dt</option>\n";
			}
			print "</select><input type=submit value=\"&gt; &gt;\"></form><hr>";

			$q_ct_q = "select count( dst ) from blocked where src='$q' and date like '$d'"; 
			$q_ct_r = mysql_query( $q_ct_q ); 
			$query_count++;
			list( $q_ct ) = mysql_fetch_row( $q_ct_r );

			print "<h4>$q_ct results shown</h4>"; 

			$dd_q = "select time, date, proto, src, srcprt, dst, dstprt from blocked where src='$q' and date like '$d'"; 
			$dd_r = mysql_query( $dd_q );
			$query_count++;

			while( list( $time, $date, $proto, $src, $srcprt, $dst, $dstprt ) = mysql_fetch_row( $dd_r ) )
			{
				print "<li>$date ($time): $src $proto/$srcprt -> $dst $proto/$dstprt</li>\n";
			}

		} else {

			print "<h3>Error -- you need to specify an IP, click back and try again.</h3>\n"; 

		}
		print "</td></tr></table></div>\n";
		break;

	// drill down a view on a specific port
	case 'pdrill':

		print "<div align=center><a href=index.php><img src=$url/fwap.png border=0></a><br><table width=600 border=0><tr><td>\n"; 
		print "<h3>$q/$proto - $d</h3>\n";
		
		$dates_q = "select date from dddates";
		$dates_r = mysql_query( $dates_q );
			$query_count++;
		print "<form method=get action=$this><input type=hidden name=f value=pdrill><input type=hidden name=q value=\"$q\"><input type=hidden name=proto value=\"$proto\"><input type=hidden name=src value=\"$src\">
			Show Date: <select name=d>";

		while( list( $dt ) = mysql_fetch_row( $dates_r ) )
		{
			print "<option value=\"$dt\">$dt</option>\n";
		}
		print "</select><input type=submit value=\"&gt; &gt;\"></form><hr>";

		if( $src == "int" )
		{
			$p_ct_q = "select count( dstprt ) from blocked where proto='$proto' and dstprt='$q' and date like '$d' and src like '172.%'"; 
		} else {
			$p_ct_q = "select count( dstprt ) from blocked where proto='$proto' and dstprt='$q' and date like '$d' and src not like '172.%'"; 
		}

		$p_ct_r = mysql_query( $p_ct_q );
			$query_count++;
		list( $p_ct ) = mysql_fetch_row( $p_ct_r ); 
		print "<h4>$p_ct results shown</h4>"; 

		if( $src == "int" )
		{
			$dd_q = "select src, dst, count( dst ) as total from blocked where proto='$proto' and dstprt='$q' and date like '$d' and src like '172.%' group by dst order by total desc"; 
		} else {
			$dd_q = "select src, dst, count( dst ) as total from blocked where proto='$proto' and dstprt='$q' and date like '$d' and src not like '172.%' group by dst order by total desc"; 
		}

		$dd_r = mysql_query( $dd_q ); 
			$query_count++;
		print "<table width=40% border=0><tr><td>Source</td><td>Destination</td><td>Total</td></tr>"; 
		while( list( $src, $dst, $total ) = mysql_fetch_row( $dd_r ) )
		{
			print "<tr><td>$src</td><td>$dst</td><td>$total</td></tr>\n";
		}
		print "</table>";
		print "</td></tr></table></div>\n";
		break;

	// view a specific day 
	case 'viewday':
		if( $q ){

			print "
				<div align=center>
					<a href=$this><img src=$url/fwap.png border=0></a><br>
					<h1>F.W.A.P. Report for $q</h1>
				<table width=600>
				<tr>
					<td colspan=2 valign=top>
						<div align=center>
							<a href=$url/stats.php><img src=\"$url/stats.php?date=$q&type=total\" border=0></a>
						</div>
						<br><br><hr>
					</td>
				</tr>
				<tr>
					<td valign=top>
			"; 

			print "<h3>Top Internal Ports Blocked</h3>\n<ol>";
			$top10_attprt_q = "select distinct dstprt, proto, count( dstprt ) as attack_count from blocked where src like '172.%' and date like '$q' group by dstprt order by attack_count desc limit 10"; 
			$top10_attprt_r = mysql_query( $top10_attprt_q );
			$query_count++;
			while( list( $dstprt, $proto, $dstprt_ct ) = mysql_fetch_row( $top10_attprt_r ) )
			{
				$service_guess = getservbyport ( $dstprt, $proto ); 
				if( $service_guess == "" ){ $service_guess = "<a target=new href=\"http://www.google.com/search?q=$dstprt+$proto\">???</a>"; }
				print "<li><a href=\"$url$this?f=pdrill&q=$dstprt&proto=$proto&d=$q&src=int\">$dstprt/$proto</a> ($service_guess) - $dstprt_ct</li>\n";
			}
			print "</ol>\n</td><td valign=top>";

			print "<h3>Top Ext. Ports Attacked</h3>\n<ol>";
			$top10_attprt_q = "select distinct dstprt, proto, count( dstprt ) as attack_count from blocked where dst like '65.125.46.%' and date like '$q' group by dstprt order by attack_count desc limit 10"; 
			$top10_attprt_r = mysql_query( $top10_attprt_q );
			$query_count++;
			while( list( $dstprt, $proto, $dstprt_ct ) = mysql_fetch_row( $top10_attprt_r ) )
			{
				$service_guess = getservbyport ( $dstprt, $proto ); 
				if( $service_guess == "" ){ $service_guess = "<a target=new href=\"http://www.google.com/search?q=$dstprt+$proto\">???</a>"; }
				print "<li><a href=\"$url/$this?f=pdrill&q=$dstprt&proto=$proto&d=$q&src=ext\">$dstprt/$proto</a> ($service_guess) - $dstprt_ct</li>\n";
			}
			print "</ol>";

			print "</td></tr><tr><td colspan=2><hr></td></tr><tr><td valign=top>";
			print "<h3>Top Internal Offenders</h3>\n"; 
			$ict_q = "select count( distinct src ) from blocked where date='$q' and src like '172.%'"; 
			$ict_r = mysql_query( $ict_q ); 
			$query_count++;
			list( $ict ) = mysql_fetch_row( $ict_r ); 
			if( $ict > 20 )
			{
				print "<i>Showing first 20 of $ict.</i><br>\n";
			}
			print "<ol>"; 
			$int_q = "select distinct src, count( dst ) as victims from blocked where date='$q' and src like '172.%' group by src order by victims desc limit 20"; 
			$int_r = mysql_query( $int_q );
			$query_count++;
			
			while( list( $int_ip, $int_ct ) = mysql_fetch_row( $int_r ) )
			{
				$audit_q = "select count( id ) from leaseinfo where ip like '$int_ip'"; 
				$audit_r = mysql_query( $audit_q );
				$query_count++;
				list( $audit_ct ) = mysql_fetch_row( $audit_r );

				if( $audit_ct )
				{
					print "<li><a href=\"$url/$this?f=drilldown&q=$int_ip&d=$q\">$int_ip</a> [<a href=\"javascript:onclick=popupwindow('$url/resolve.php?query=$int_ip', 'dns', '425', '400' )\">dns</a> | <a href=\"javascript:onclick=popupwindow('$url/audit.php?query=$int_ip&ipomac=ip', 'dhcp', '475', '400' )\">dhcp</a> | <a href=\"javascript:onclick=popupwindow('$url/portscan.php?query=$int_ip', 'scan', '425', '400' )\">scan</a>] &nbsp;($int_ct)</li>\n";
				} else {
					print "<li><a href=\"$url/$this?f=drilldown&q=$int_ip&d=$q\">$int_ip</a> [<a href=\"javascript:onclick=popupwindow('$url/resolve.php?query=$int_ip', 'dns', '425', '400' )\">dns</a> | <a href=\"javascript:onclick=popupwindow('$url/portscan.php?query=$int_ip', 'scan', '425', '400' )\">scan</a>] ($int_ct)</li>\n";
				}
			}
			print "</ol></td><td valign=top>"; 

			print "<h3>Top External Offenders</h3>\n"; 
			$ect_q = "select count( distinct src ) from blocked where date='$q' and src not like '172.%'"; 
			$ect_r = mysql_query( $ect_q ); 
			$query_count++;
			list( $ect ) = mysql_fetch_row( $ect_r ); 
			if( $ect > 20 )
			{
				print "<i>Showing first 20 of $ect.</i><br>\n";
			}
			print "<ol>"; 
			$ext_q = "select distinct src, count( dst ) as victims from blocked where date='$q' and src not like '172.%' group by src order by victims desc limit 20";
			$ext_r = mysql_query( $ext_q );
			$query_count++;
			
			while( list( $ext_ip, $ext_ct ) = mysql_fetch_row( $ext_r ) )
			{
				print "<li><a href=\"$url/$this?f=drilldown&q=$ext_ip&d=$q\">$ext_ip</a> [<a href=\"javascript:onclick=popupwindow('$url/resolve.php?query=$ext_ip', 'dns', '425', '400' )\">dns</a> | <a href=\"javascript:onclick=popupwindow('$url/portscan.php?query=$ext_ip', 'scan', '425', '400' )\">scan</a> ] ($ext_ct)</li>\n";
			}
			print "</ol></td></tr><tr><td colspan=2><hr></td></tr><tr><td colspan=2>";
			print "<h3>Misc. Error Messages To Examine</h3>\n";
			$odd_q = "select distinct message from others where date like '$q'"; 
			$odd_r = mysql_query( $odd_q );
			$query_count++;
			while( list( $m ) = mysql_fetch_row( $odd_r ) )
			{
				print "<li><a href=\"javascript:onclick=popupwindow('$url/$this?f=odrill&p=$m', 'odrill', '750', '400' )\">details</a> $m</li>\n";
			}
			print "</td></tr></table></div>"; 
		} else {

			print "<h3>No date specified, click <a href=$url/$this>here</a>.</h3>\n";

		}
		break;

	// the user is submitting an SQL query to be executed.
	case 'sqlquery':
		if( $q )
		{
			str_replace( '\\', '', $q ); 
			print "<h2>$q</h2>\n";
			$query_r = mysql_query( $q )
				or die( mysql_error() );
			$query_count++;
			while( $row = mysql_fetch_row( $query_r ) )
			{
				for( $i = 0; $i <= $row; $i++ )
				{
					print "| $row[$i]";
				}
				print "|<br>\n";
			}
		} else {

			print "
			<form method=post action=$this>
			<input type=hidden name=f value=sqlquery>
			SQL Query: <input type=text name=q value=\"$q\"> <input type=submit value=\"&gt; &gt;\">
			</form>
			";

		}
		break;

	default:

		$date_q = "select date from dddates"; 
		$date_r = mysql_query( $date_q );
		$query_count++;

		print "
			<div align=center>
			<table width=600 border=0 cellspacing=0 cellpadding=0>
			<tr>
				<td><img src=fwaplogo_isaac_top.png></td>
				<td><img src=fwaplogo_banner_top.png></td>
			</tr>
			<tr>
				<td valign=top>
					<img src=fwaplogo_isaac_bottom.png><br>
					<!-- START SIDEBAR-->
					<!-- END SIDEBAR -->
				</td>
				<td>
					<!-- START MAIN -->

					<br>
					<div align=center>
					<table width=100% border=0 cellpadding=3 cellspacing=3>
					<tr>
						<td bgcolor=#7289aa colspan=2>
							<div align=center>
							<h2>Available Daily Reports</h2>
							<form method=post action=$this>
							<input type=hidden name=f value=\"viewday\">
							Report Date: <select name=q>
		"; 

		while( list( $date ) = mysql_fetch_row( $date_r ) )
		{
			if( $date == yesterday() )
			{
				print "<option value=\"$date\" selected>$date</option>\n"; 	
			} else {
				print "<option value=\"$date\">$date</option>\n"; 	
			}
		}

		print "
							</select> 
							<input type=submit value=\"&gt; &gt;\">
							</form>
							</div>
							<P>Select the desired date for which you would like to see the F.W.A.P. report.  The reports can take up to two minutes to completely load.  Please be patient.</p>
						</td>
					</tr>
					<tr>
						<td width=50% valign=top bgcolor=99b1d5>
							<h2>Source Host Query</h2>
							<form method=post action=$this>
							<input type=hidden name=f value=hdrill>
							IP Address:<br><input type=text name=q value=\"\"> <input type=submit value=\"&gt; &gt;\">
							</form>
							<p>The Source Host Query will retrieve the total history of blocked packets for a given host address.  It should be understood that a single host address could have been owned by several different people over history and as such a DHCP Lease Query should also be made on the host address.</p>
						</td>
						<td width=50% valign=top bgcolor=99b1d5>
							<h2>DHCP Lease Query</h2>
							<form method=post action=audit.php>
							<input type=radio name=ipomac value=ip>IP
							<input type=radio name=ipomac value=mac>MAC<br>
							<input type=text name=query value=\"$query\"> <input type=submit value=\"&gt; &gt;\">
							</form>
							<p>The DHCP Lease Query allows you to search for information about a specific machine based on its IP address or MAC address.  The reports will also offer a machine-name, which frequently can be associated to an individual or area.</p>
						</td>
					</tr>
					<tr>
						<td bgcolor=#e0ebfc colspan=2>
							<div align=center>
							<h2>Trending</h2>
							<a href=\"javascript:onclick=popupwindow('$url/trends.php?q=both', 'bothtrends', '400', '400' )\">All Attack Trends</a> | 
							<a href=\"javascript:onclick=popupwindow('$url/trends.php?q=internal', 'inttrends', '400', '400' )\">Internal Attack Trends</a> | 
							<a href=\"javascript:onclick=popupwindow('$url/trends.php?q=external', 'exttrends', '400', '400' )\">External Attack Trends</a>
							</div>
							<p><b>WARNING!</b> These trending reports require several minutes to complete.  Seriously.</p>
							<br>
						</td>
					</tr>
					</table>

					<!-- END MAIN -->
				</td>
			</tr>
			<tr>
				<td colspan=2>
					<div align=center>
						<hr width=100%>
						<div class=\"footer\">(C)opyright 2003, The Evangelical Lutheran Good Samaritan Society, all rights reserved.</div>
					</div>
				</td>	
			</tr>
			</table>
			</div>
		"; 

}

$end_time = getmicrotime();

$time = $end_time - $start_time; 
print "<br><br><br><div class=\"footer\">$query_count queries executed in $time seconds</div><br>F.W.A.P. v$version\n";

?>


</body>
</html>
