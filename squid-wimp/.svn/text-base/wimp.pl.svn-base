#!/usr/bin/perl
#
# WIMP v.0.2.0 - by C.J. Steele <csteele@good-sam.com>
#
# description:
#	WIMP processes squid access.log files, picks out the times, dates, and 
#	non-garbage URI's (i.e. those that are not pictures, etc.) and dumps 
#	them in to an excel spreadsheet.  Once the spreadsheet is populated, 
#	it is e-mailed a designated recipient.
#
# todo:
#	* improve command-line option parsing (v.0.2.1)
#	* improve comments (v.0.2.1)
#	* set widths on spreadsheet columns (v.0.2.1)
#	* break out core functions in to subs (v.0.2.2)
#
# changelog:
#	* v.0.2.0 - output to Excel spreadsheet and automatic e-mailing of attachment
#	* v.0.1.0 - output via CSV, e-mailed manually
#
use strict;
use Spreadsheet::WriteExcel;
use Net::SMTP::Multipart;

my %conf; 
	$conf{'input'} = $ARGV[0];
	$conf{'output'} = $ARGV[1]; 
	$conf{'ippat'} = $ARGV[2];
	# by default, send everything to csteele@good-sam.com
	$conf{'recipient'} = "csteele\@good-sam.com"; 
	if( $ARGV[3] ){
		$conf{'recpient'} = $ARGV[3];
	}
	$conf{'verbose'} = 0;
	$conf{'smtpserver'} = "jonas.corp.good-sam.com"; 
	$conf{'smtpport'} = "25000";


if( scalar( @ARGV ) < 3 )
{
	die "usage: $0 <squidlogfile> <outputfile.xls> <ipaddresstofocuson>"; 
}

my @exceptions = ( '.gif', '.jpg', '.png', '.css', '.js');

my $row = 0; 
my $col = 0;

my $g_ss = Spreadsheet::WriteExcel->new( $conf{'output'} ); 
my $g_ss_wks = $g_ss->addworksheet( "websites" );

if( $conf{'input'} and ( -e $conf{'input'} and -r $conf{'input'} ) )
{
	# proceed only if the file is there and we can read it.
	open( IN, $conf{'input'} ) or die_violently( "open failed!" );
	while( my $line = <IN> )
	{
		chomp( $line );
		my @log_entry = clean_parse( $line );
		my @time = parse_time( $log_entry[0] );

		my $insert = 1; 
		foreach ( @exceptions )
		{
			print "II: checking $log_entry[6] for instances of $_...\n" if( $conf{'verbose'} );
			if( $log_entry[6] =~ m/$_/i )
			{
				$insert = 0;
				print "not putting $log_entry[6] in...\n" if( $conf{'verbose'} );
			}
		}


		# this is here just to make sure 
		if( $log_entry[2] !~ m/$conf{'ippat'}/ )
		{
			$insert = 0;
		}

		if( $insert )
		{
			# kick out time to spreadsheet...
			$time[2]-=5; 
			$g_ss_wks->write( $row, $col, "$time[2]:$time[1]:$time[0]" ); 
			# kick out date to spreadsheet...
			$time[4]++; $time[5]+=1900;
			$g_ss_wks->write( $row, $col+1, "$time[4]/$time[3]/$time[5]" );
			# kick out IP to spreadsheet...
			$g_ss_wks->write( $row, $col+2, $log_entry[2] );
			# kick out URL to spreadsheet...
			$g_ss_wks->write( $row, $col+3, $log_entry[6] );
			$row++;
		}
	}
	close( IN );

	$g_ss->close();

	# send the e-mail containing the report spreadsheet.
	my $smtp = Net::SMTP::Multipart->new( $conf{'smtpserver'} );
	$smtp->Header( To => "$conf{'recipient'}", Subj => "WIMP: Report for $conf{'ippat'}", From => "csteele\@good-sam.com" ); 
	$smtp->Text( "Attached are the results of a nightly report designed to observe the web browsing behaviors an employee you have been designated as monitoring.  If you have questions about this report, please e-mail csteele\@good-sam.com." );
	$smtp->FileAttach( "$conf{'output'}" );
	$smtp->End();

} else {

	if( $conf{'input'} ne "" )
	{
		die_violently( "$conf{'input'} not found!" );
	} else {
		show_usage();
		exit( 1 );
	}
}

exit( 0 );



sub parse_time
{
	my( $in_time ) = @_;
	return gmtime( $in_time );
}


sub clean_parse
{
	my( $entry_line ) = @_;
	my $time = substr( $entry_line, 0, 14 ); 
	my $size = substr( $entry_line, 14, 8 ); $size =~ s/\s//g; 
	my $client_ip = substr( $entry_line, 22 ); my( $client_ip, $entry_line ) = split( /\s/, $client_ip, 2 ); 
	my ( $hit_or_miss, $unknown, $method, $url, $garbage, $ipc, $type ) = split( /\s/, $entry_line ); 
	return( $time, $size, $client_ip, $hit_or_miss, $unknown, $method, $url, $garbage, $ipc, $type );
}


sub die_violently 
{
	my( $msg ) = @_;
	print STDERR "$0 > $msg\n";
}


sub show_usage
{
	print "$0 - (C) 2002 by Corey J. Steele\n";
	print "$0 <squid_log>\n\n";
}
