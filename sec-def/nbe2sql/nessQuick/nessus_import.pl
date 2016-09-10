# Nessus Import Script v3.0

#!/usr/local/bin/perl

use DBI;


# Name of import file
#
print "Enter full .nbe filename: ";
$infile = <STDIN>;
chomp $infile;

######################
# Connect To Database
#
$database = "nessus";
$hostname = "localhost";
$username = "user";
$password = "pass";
$dbh = DBI->connect("DBI:mysql:$database:$hostname", $username, $password);
die "Cannot log into database.  Please try again later.\n" unless $dbh;
print "Connected to $database... \n";


# Open file for input
#
open(INPUT,"<$infile")||die("Can't open report file");
print "Opened $infile... \n";


# loop through input file and insert into table
#
print "Processing input file... \n";
while (<INPUT>)
  {


# Initialize field values each time to ensure the are clear
#
	$infield1 = " ";
	$infield2 = " ";
	$infield3 = " ";
	$infield4 = " ";
	$infield5 = " ";
	$infield6 = " ";
	$infield7 = " ";
	$insertid = $sth->{mysql_insertid}; 

# Break out fields from input file
#
	($infield1,$infield2,$infield3,$infield4,$infield5,$infield6,$infield7)=split(/\|/,$_);


# Translate ; to \n for newline
#
	$infield7 =~ tr/;/\n/;
# Translate " to \"
#
	$infield7 =~ tr/"/'/;
# Convert "infield6 factor" to infield6 value HIGH/MEDIUM/LOW
#
        $infield6="7";
        $infield6='1' if ($infield7 =~ "Risk factor : Serious");
        $infield6='2' if ($infield7 =~ "Risk factor : High");
        $infield6='3' if ($infield7 =~ "Risk factor : Medium");
        $infield6='4' if ($infield7 =~ "Risk factor : Medium/Low");
        $infield6='5' if ($infield7 =~ "Risk factor : Low/Medium");
        $infield6='6' if ($infield7 =~ "Risk factor : Low");


# Remove "infield6 factor" from $infield7 field
# Using ` vs / due to existing / in field
#
	$infield7=~ s`Risk factor : High``;
	$infield7=~ s`Risk factor : Serious``;
	$infield7=~ s`Risk factor : Medium``;
	$infield7=~ s`Risk factor : Medium/Low``;
	$infield7=~ s`Risk factor : Low/Medium``;
	$infield7=~ s`Risk factor : Low``;


# Insert values into appropriate table
#
	if ($infield1 eq "results") {
		$dbh->do("insert into results (id, domain, host, service, scriptid, risk, msg) 
		values ('$insertid','$infield2','$infield3','$infield4','$infield5','$infield6',\"$infield7\")
		");
	}
	else {
		$dbh->do("insert into timestamps (id, unused, host, progress, timestamp) 
		values ('$insertid','$infield2','$infield3','$infield4','$infield5')
		");
	}
  }


print "Finished processing input file... \n";


close INPUT;
$dbh->disconnect;
exit(0); 

