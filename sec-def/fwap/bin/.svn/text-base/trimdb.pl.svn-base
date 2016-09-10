#!/usr/bin/perl
# trimdb.pl by C.J. Steele <csteele@good-sam.com>
#
#**********************************************************************
# this script should not be used on a regular basis!  `trimdb_daily.pl` 
# is the version that should be used on a daily basis.
#**********************************************************************
#
# trimdb.pl is a one-time script that can be used to populate the 
# fw2.blocked table as a result of the fact that it grew beyond 
# Linux's 4gb file-size limit (that may be a limitation of MySQL 3.23 as 
# opposed to Linux and/or ext3, however that is irrelevant as the bigger 
# problem is that MySQL can't handle all the data we're throwing at it.)
# 
use strict;
use POSIX; 
use DBD::mysql;

########################################################################
# VARIABLE DECLARATIONS
########################################################################
my $db_name = "fw2"; 
my $db_user = "root"; 
my $db_pass = ""; 
my @mon = ( 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' );
my $dbh = DBI->connect( "dbi:mysql:mysql_socket=/var/lib/mysql/mysql.sock;database=$db_name", $db_user, $db_pass )
	or die "Couldn't connect to database ($DBI::errstr)";



########################################################################
# WORK
########################################################################
my $now = time();
for( my $f = 0; $f <= 180; $f++ )
{
	my( $d, $m, $y ) = (localtime( $now - (86400*$f) ))[3,4,5]; 
		$d = sprintf( "%02d", $d ); 
		$y+=1900;
	my $date = "$mon[$m] $d $y";
	#my $save_q = "insert into blocked2 select time, date proto, src , srcprt, dst, dstprt from blocked where date = '$date'";
	my $save_q = "insert into blocked select * from blocked2 where date = '$date'";
	my $save_h = $dbh->prepare( $save_q );
	my $save_r = $save_h->execute();
}

$dbh->close();

exit( 0 );
