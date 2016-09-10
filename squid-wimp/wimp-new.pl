#!/usr/bin/perl
#
# WIMP v.1.0.0-dev by C.J. Steele <coreyjsteele@yahoo.com>
#
# wimp.pl [options] ipaddress
# options:
#   -m toaddr		e-mail the excel spreadsheet to 'address'
#   -f fromaddr		e-mail address the report should come from (default user@host)
#   -o outfile		use 'outfile' instead of ipaddress for .xls filename
#   -s smtpserver	smtp server to mail through (default is localhost)
#   -p smtpport		port on smtp server to use (default is 25)
#   -e exfile		file containing regexp patterns to ignore
#   -i inputfiles	quoted, comma-separated list of files to process (default is access.log*)
#
# description:
#	WIMP processes squid access.log files, picks out the times, dates, and 
#	non-garbage URI's (i.e. those that are not pictures, etc.) and dumps 
#	them in to an excel spreadsheet.  Once the spreadsheet is populated, 
#	it is e-mailed a designated recipient.
#
# note:
#   We require a hacked version of Spreadsheet::WriteExcel::Worksheet that 
#   has set_name(), so... find one (e-mail me) or write it in (its trivial)
#   DISCLAIMER: if you use Spreadsheet::WriteExcel for anything to do with 
#   function parsing, set_name() will break all your function implementations
#
use strict;
use Getopt::Std;
use Spreadsheet::WriteExcel::Big;
use Net::SMTP::Multipart;
use English;


########################################################################
#
# variable declarations and default values.
#
my $debug = 0;
my $version = "1.0.0-pre1"; 
my %opt;
my %conf;
	$conf{'mail_from'} = get_default_mailfrom();
	$conf{'mail_srvr'} = "localhost";
	$conf{'mail_port'} = "25";
	$conf{'infiles'} = "access.log*";
	$conf{'exfile'} = "exceptions";
my $workbook; 
my @exceptions; # an array containing regexp things to exclude form the report



########################################################################
#
# parse cli options...
#
getopts( "m:f:o:s:p:e:i:h", \%opt ); 
if( defined $opt{'h'} ){ show_usage(); exit( 1 ); }
if( defined $opt{'o'} ){ $conf{'outfile'} = $opt{'o'}; }
if( defined $opt{'m'} ){ $conf{'mail_rcpt'} = $opt{'m'}; }
if( defined $opt{'f'} ){ $conf{'mail_from'} = $opt{'f'}; }
if( defined $opt{'s'} ){ $conf{'mail_srvr'} = $opt{'s'}; }
if( defined $opt{'p'} ){ $conf{'mail_port'} = $opt{'p'}; }
if( defined $opt{'e'} ){ $conf{'exfile'} = $opt{'e'}; }
if( defined $opt{'i'} ){ $conf{'infiles'} = $opt{'i'}; }
$conf{'ippat'} = $ARGV[$ARGV-1]; #TODO: make ippat an array and support multiple IP patterns at CLI
if( ! defined $conf{'outfile'} ){ $conf{'outfile'} = "$conf{'ippat'}.xls"; }


# show debug info for %conf
foreach( keys %conf ) { print "$_ ", $conf{$_}, "\n" if( $debug ); }


if( $conf{'ippat'} ne "" and $conf{'infiles'} ne "" )
{
	#we've got an ip and some input files, proceed...
	# our load_exceptions routine is shit-canned, we'll worry about it later.
	@exceptions = ( "\.(gif|jpg|png|swf|css|js|jpeg)", "\.good\-sam\.com.*" );
	my @inputfiles = load_input_files( $conf{'infiles'} );
	$workbook = Spreadsheet::WriteExcel::Big->new( $conf{'outfile'} ); 
	process_log( $_ ) foreach ( @inputfiles );
	$workbook->close();

	if( $conf{'mail_rcpt'} )
	{
		eval {
			my $smtp = Net::SMTP::Multipart->new( "$conf{'mail_srvr'}:$conf{'mail_port'}" );
			$smtp->Header( To=>"$conf{'mail_rcpt'}", subj=> "WIMP: Report for $conf{'ippat'}", From=> $conf{'mail_from'} );
			$smtp-Text( "Attached are the results of wimp." );
			$smtp->FileAttach( $conf{'outfile'} ); 
			$smtp->End();
		}; if( $@ ){
			die_violently( "E: couldn't send e-mail. ($@)\n" );
		}
	}
} else {
	show_usage();
}


exit( 0 );


########################################################################
########################################################################
# SUB ROUTINES
########################################################################
########################################################################


########################################################################
#
# process_log()
#
# does the actual work of going through a logfile and writes matching 
# URL's to the spreadsheet.
#
# TODO: set format on date column items so Excel can do date diffs.
# TODO: handle exceptions (see TODO, below.)
#
sub process_log
{
	my $logfile = shift; 
	print "I: processing $logfile...\n" if( $debug );
	my $worksheet = $workbook->addworksheet( "$logfile" );
	my $firstdate; 
	my $lastdate; 
	my $row = 0;
	my $col = 0;

	open( IN, $logfile ) or die_violently( "E: $!" );
	while( my $line = <IN> )
	{
		chomp( $line );
		my @log_entry = clean_parse( $line );
		my $time = parse_time( $log_entry[0] );
		my $insert = 1; 

		$insert = 0 if( $log_entry[2] !~ m/$conf{'ippat'}/ );  # if its not our target, ignore it...
		
		foreach my $pat ( @exceptions )
		{
			#print "I: checking $pat in $log_entry[6]\n" if( $debug );
			$insert = 0 if( $log_entry[6] =~ m/$pat/i );
		}
		
		if( $insert )
		{
			if( $row == 0 ){ $firstdate = $log_entry[0] } else { $lastdate = $log_entry[0]; }
			$worksheet->write( $row, $col, "$time" ); #logged time
			$worksheet->write( $row, $col+1, "$log_entry[2]" ); # logged IP
			$worksheet->write( $row, $col+2, "$log_entry[6]" ); # logged URL
			$row++;
		}
	}
	#set our tab name here...
	# $worksheet->set_name( sheet_name( $firstdate, $lastdate ) );  #this may be dorking out Excel.
	close( IN );
}


########################################################################
#
# sheet_name()
#
# forms a valid worksheet name according to the first and last date 
# entries in the logfile
#
# worksheet names should be "Mon XX - Mon yy"
#
sub sheet_name 
{
	my @months = ( "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" );
	my( $d1, $d2 ) = @_;
	my @date1 = gmtime( $d1 );
	my @date2 = gmtime( $d2 );
	return( "$months[$date1[4]] $date1[3] - $months[$date2[4]] $date2[3]" );
}


########################################################################
#
# load_exceptions()
#
# loads the exceptions file, if one was set. the exceptions file (xf) 
# should have ONE PATTERN PER LINE!!!  We can only check the syntax of 
# the exp, functional equiv. is the authors problem.
#
sub load_exceptions
{
	if ( -e $conf{'exfile'} and -r $conf{'exfile'} )
	{
		#our exception file exists and is readable...
		my $lc = 1; # used to track which line of our exception list we're on.
		open( XF, "$conf{'exfile'}" ) or die_violently( "E: $!" ); 
		while( <XF> )
		{
			chomp( $_ );
			if( check_pattern( $_ ) )
			{
				push( @exceptions, $_ ); #our pattern checked out.
			} else {
				die_violently( "E: there is an error in your pattern file at line $lc" );
			}
			$lc++;
		}
		close( XF );
	} else {
		# there could be a problem with the exception file
		if( -e $conf{'exfile'} and ! -r $conf{'exfile'} )
		{
			# the exception file isn't readable by $EUID
			die_violently( "E: exception file exists but is not readable." );
		} elsif( defined $conf{'exfile'} ){
			# a exception file was specified but not present.
			die_violently( "E: exception file specified but not found." );
		} else {
			# no exception file specified.
			print STDERR "W: no exceptions file specified, filtering is disabled.\n" if( $debug );
		}
	}

	if( scalar( @exceptions ) )
	{ 
		return; # we got some in... hooray!
	} elsif( defined $conf{'exfile'} and scalar( @exceptions ) < 1 ){
		die_violently( "E: pattern file specified, but no patterns found!" );
	}
}


########################################################################
#
# check_pattern()
#
# checks the syntax of a pattern and returns 1 if the eval{} doesn't crap
# itself thoroughly.  returns 1 if the pattern is okay, 0 if it isn't.
#
# TODO: implement pattern checking.  ;-)
#
sub check_pattern
{
	return 1;
}


########################################################################
#
# load_input_files()
#
# returns an array from the user provided cli option -- this option can
# be: a single file, comma-separated list of file, or wild-card (only *)
#
# TODO: we're using `ls`, which isn't very portable, fix that.
#
sub load_input_files
{
	my $in = shift;
	my $out; 
	foreach( split( /\,/, $in ) )
	{
		if( $_ =~ m/\*/g )
		{
			foreach my $f ( `ls -1 $_` )
			{
				chomp( $f );
				$out .= ",$f" if( $f ne "" );
			}
		} else {
			$out .= ",$_"; 	
		}
	}
	$out =~ s/^\,//; 
	return split( /\,/, $out );
}


########################################################################
#
# die_violently()
#
# dies with the message passed it, death throws sent to STDOUT
#
sub die_violently 
{
	my( $msg ) = @_;
	print STDERR "$msg\n";
	exit( 1 );
}


########################################################################
#
# parse_time() 
#
# returns a time string from a squid timestamp, subtracts 21600 seconds 
# to set timezone to GMT-0600
#
# TODO: support timezone CLI option
#
sub parse_time
{
	my( $in_time ) = @_;
	return scalar( gmtime( $in_time - 21600 ) );
}


########################################################################
#
# clean_parse()
#
# parses a squid logfile line into an array and does some cleanup
#
sub clean_parse
{
	my( $entry_line ) = @_;
	my $time = substr( $entry_line, 0, 14 ); 
	my $size = substr( $entry_line, 14, 8 ); $size =~ s/\s//g; 
	my $client_ip = substr( $entry_line, 22 ); my( $client_ip, $entry_line ) = split( /\s/, $client_ip, 2 ); 
	my ( $hit_or_miss, $unknown, $method, $url, $garbage, $ipc, $type ) = split( /\s/, $entry_line ); 
	return( $time, $size, $client_ip, $hit_or_miss, $unknown, $method, $url, $garbage, $ipc, $type );
}


########################################################################
#
# show_usage()
#
# show a message telling people how to use this crazy thing.
# 
# TODO: this needs to be updated.
#
sub show_usage
{
	print "wimp $version - (C) 2002-2005 by Corey J. Steele\n";
	print "usage: wimp.pl [options] ip\n";
	print "options:\n";
	print "   -m toaddr		e-mail the excel spreadsheet to 'address'\n";
	print "   -f fromaddr		e-mail address the report should come from (default user\@host)\n";
	print "   -o outfile		use 'outfile' instead of ipaddress for .xls filename\n";
	print "   -s smtpserver	smtp server to mail through (default is localhost)\n";
	print "   -p smtpport		port on smtp server to use (default is 25)\n";
	print "   -e exfile		file containing regexp patterns to ignore\n";
	print "   -i inputfiles	quoted, comma-separated list of files to process (default is access.log*)\n";
	print "\n\n";
}


########################################################################
#
# get_default_mailfrom()
#
# returns a cobled string of user@host where user is the user running the 
# script and host is the fqdn of localhost
# 
# TODO: this is NOT portable...
#
sub get_default_mailfrom
{
	my $user = $ENV{'USER'};
	my $hostname = `hostname -f`; chomp( $hostname );
	return "$user\@$hostname";
}

