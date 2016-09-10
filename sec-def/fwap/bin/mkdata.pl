#!/usr/bin/perl
# mkdata.pl v0.1.0 by C.J. Steele <csteele@good-sam.com>
#	May 2003
#
# This script processes 'yesterday's' blocked packets and creates necessary entries in the stats 
# table to allow the rapid generation of statistical graphs by the $FWAP/stats.php script.  This 
# script ONLY handles blocks, and ONLY generates data used by the $FWAP/stats.php script.
#
use strict;
use POSIX; 
use DBD::mysql;

my $db_name = "fw2"; 
my $db_user = "root"; 
my $db_pass = ""; 


my %mon = { 0 => 'Jan', 1 => 'Feb', 2 => 'Mar', 3 => 'Apr', 4 => 'May', 5 => 'Jun', 6 => 'Jul', 7 => 'Aug', 8 => 'Sep', 9=> 'Oct', 10 => 'Nov', 11 => 'Dec' };
my $dbh = DBI->connect( "dbi:mysql:mysql_socket=/var/lib/mysql/mysql.sock;database=$db_name", $db_user, $db_pass )
	or die "Couldn't connect to database ($DBI::errstr)";

my $date = $ARGV[0];

my( $m, $d, $y ) = split( " ", $date, 3 ) ;
my $period = 0;
my $time1 = mktime( 0, 0, 0, $m, $d, $y );
my $time2 = $time1; 
my @total_data = ();
my @int_data = ();
my @ext_data = ();


while( $time1 < mktime( 0, 0, 0, $m, $d, $y )+86399 )
{

	$time2 += 288; 
		my( $h, $m, $s ) = (gmtime( $time1 ))[2,1,0];
	my $qt1 = sprintf( "%02d:%02d:%02d", $h, $m, $s ); 
		( $h, $m, $s ) = (gmtime( $time2 ))[2,1,0];
	my $qt2 = sprintf( "%02d:%02d:%02d", $h, $m, $s ); 

	my $total_q = "select count( id ) from blocked where date='$date' and ( time >= \"$qt1\" and time < \"$qt2\" )";
	my $total_h = $dbh->prepare( $total_q ); 
	my $total_r = $total_h->execute(); 
	my $ct = 0; 
	while( ( $ct ) = $total_h->fetchrow_array() )
	{
		push( @total_data, $ct );
	}
	
	my $int_q = "select count( id ) from blocked where date='$date' and src like '172.%' and ( time >= \"$qt1\" and time < \"$qt2\" )";
	my $int_h = $dbh->prepare( $int_q ); 
	my $int_r = $int_h->execute(); 
	while( ( $ct ) = $int_h->fetchrow_array() )
	{
		push( @int_data, $ct );
	}

	my $ext_q = "select count( id ) from blocked where date='$date' and src not like '172.%' and ( time >= \"$qt1\" and time < \"$qt2\" )";
	my $ext_h = $dbh->prepare( $ext_q ); 
	my $ext_r = $ext_h->execute(); 
	while( ( $ct ) = $ext_h->fetchrow_array() )
	{
		push( @ext_data, $ct );
	}
	
	$qt1 = $qt2;
	$time1 = $time2; 

} #end while
	

my $total_i = "insert into stats ( date, rpt, data ) VALUES ( '$date', 'total', '"; 
$total_i .= "$_ " foreach( @total_data );
$total_i .= "' )"; 
$dbh->do( $total_i );

my $int_i = "insert into stats ( date, rpt, data ) VALUES ( '$date', 'int', '"; 
$int_i .= "$_ " foreach( @int_data );
$int_i .= "' )"; 
$dbh->do( $int_i );

my $ext_i = "insert into stats ( date, rpt, data ) VALUES ( '$date', 'ext', '"; 
$ext_i .= "$_ " foreach( @ext_data );
$ext_i .= "' )"; 
$dbh->do( $ext_i );

exit( 0 );
