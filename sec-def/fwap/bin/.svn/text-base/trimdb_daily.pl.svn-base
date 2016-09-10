#!/usr/bin/perl
# 
# trimdb_daily.pl by C.J. Steele <csteele@good-sam.com>
#
# trimdb_daily.pl is a script designed to limit the entries kept in FWAP's fw2.blocked table to those that are not older than 180 days.
#
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
my $mysql = "/usr/bin/mysql"; 
my @mon = ( 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' );
my $dbh = DBI->connect( "dbi:mysql:mysql_socket=/var/lib/mysql/mysql.sock;database=$db_name", $db_user, $db_pass )
	or die "Couldn't connect to database ($DBI::errstr)";



########################################################################
# WORK
########################################################################
my $now = time();
my( $d, $m, $y ) = (localtime( $now - (86400*181) ))[3,4,5]; 
	$d = sprintf( "%02d", $d ); 
	$y+=1900;
my $date = "$mon[$m] $d $y";
my $newTblName = "blocked_$d$mon[$m]$y"; 
if( makeBlockedTbl( $newTblName ) )
{
	my $save_q = "insert into $newTblName select * from blocked where date = '$date'";
	my $save_h = $dbh->prepare( $save_q );
	my $save_r = $save_h->execute();
	my $del_q = "delete from blocked where date = '$date'"; 
	my $del_r = $save_h->execute();
} else {
	print STDERR "Couldn't create the table in fw2!\n";
	exit( -1 );
}
#$dbh->close();

exit( 0 );



########################################################################
# SUBROUTINES
########################################################################
sub makeBlockedTbl
{
	my $tblName = shift;
	my $tmpFile = `/bin/mktemp /tmp/newBlocked.XXXXXX`;
	open( OUT, ">$tmpFile" );
		print OUT "CREATE TABLE $tblName (\n";
		print OUT "  id int(11) NOT NULL auto_increment,\n";
		print OUT "  time varchar(16) NOT NULL default '',\n";
		print OUT "  date varchar(32) NOT NULL default '',\n";
		print OUT "  proto varchar(16) NOT NULL default '',\n";
		print OUT "  src varchar(64) NOT NULL default '',\n";
		print OUT "  srcprt varchar(16) NOT NULL default '',\n";
		print OUT "  dst varchar(64) NOT NULL default '',\n";
		print OUT "  dstprt varchar(16) NOT NULL default '',\n";
		print OUT "  PRIMARY KEY  (id),\n";
		print OUT "  KEY src (src),\n";
		print OUT "  KEY dst (dst),\n";
		print OUT "  KEY date (date)\n";
		print OUT ") TYPE=MyISAM;\n";
	close( OUT );
	`$mysql $db_name < $tmpFile`;
	return 1;
}
