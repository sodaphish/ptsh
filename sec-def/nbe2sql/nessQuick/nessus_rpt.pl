# Nessus Report Script v3.0
# 
# This sorts the data in order of risk (highest to lowest), description, and host

#!/usr/local/bin/perl

use DBI;


# Connect To Database
#
$database = "nessus";
$hostname = "localhost";
$username = "user";
$password = "pass";
$dbh = DBI->connect("DBI:mysql:$database:$hostname", $username, $password);
die "Cannot log into database.  Please try again later.\n" unless $dbh;


# Name of report file
#
#print "Enter desired report filename: ";
#$outfile = <STDIN>;
#chomp $outfile;


#open the output file 
#open(REPORT, ">$outfile") || die("Couldn't open report file"); 


# Select statement to produce desired report
#
$sth = $dbh->prepare("SELECT * 
			FROM results 
			ORDER by risk, msg, host")
	or die "Can't prepare: $dbh->errstr\n";

# Execute query
#
$rv = $sth->execute
	or die "can't execute the query: $sth->errstr";

# Initialize test variable
#
$lastmsg = " ";

# "while" loop to produce report
#
while (@array = $sth->fetchrow_array)
	{
	($id, $domain, $host, $service, $scriptid, $risk, $msg) = @array;

	if ($msg ne $lastmsg) {

		print "\n";
		if ($msg ne "") { print "Description:   $msg \n" };
		if ($service ne "") { print "Service:  $service \n" };

# convert $risk to HIGH, MEDIUM, LOW or INFO for report
#
		if ($risk eq "1") {
			print "Risk:     HIGH \n";
		} elsif ($risk eq "2") {
			print "Risk:     HIGH \n";
		} elsif ($risk eq "3") {
			print "Risk:     MEDIUM \n";
		} elsif ($risk eq "4") {
			print "Risk:     MEDIUM \n";
		} elsif ($risk eq "5") {
			print "Risk:     MEDIUM \n";
		} elsif ($risk eq "6") {
			print "Risk:     LOW \n";
		} else {
			print "Risk:     INFO \n";
		}
	} else {

# else don't print anything
# this allows report to print list of hosts common to each vulnerability

	}

	if ($host ne "") { print "Host:     $host \n" };

# Update test variable
#
	$lastmsg = $msg;

}


$dbh->disconnect;

exit(0); 

