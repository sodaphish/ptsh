#!/usr/bin/perl
use strict;

my $file1 = $ARGV[0]; 
my $file2 = $ARGV[1];

sub getAddObjName
{
	# set device-group DC-test-box address Bis_Fam_pract ip-netmask 165.234.71.0/32
	my $retval = "";
	my $addgrp = 0;
	my $obj = shift;
	$obj =~ s/^set\ device\-group\ DC\-test\-box\ //i; 
	if( $obj =~ m/^address\-group\ / )
	{
		# its an address group
		$obj =~ s/^address\-group\ //;
		$addgrp = 1; 
	} elsif( $obj =~ m/^address\ / ) { 
		# its a single address
		$obj =~ s/^address\ //;
	} #fi

	if( $obj =~ /^\"/ )
	{
		#object with space in its name
		$obj =~ s/^"//; 
		$obj =~ s/".*//; 
		$retval = $obj;
	} else {
		my @parts = split( /\ /, $obj, 2 ); 
		$retval = $parts[0]; 
	} #fi
	return $retval
} #end sub


sub getRuleName
{
	my $rulename = "";
	my $line = shift;

	$line =~ s/^set\ device\-group\ DC\-test\-box\ pre\-rulebase\ security\ rules\ //i; 
	if( $line =~ /^"/ )
	{
		$line =~ s/^"//;
		$line =~ s/".*//;
		$rulename = $line;
	} else {
		my @parts = split( /\ /, $line, 2 ); 
		$rulename = $parts[0]; 
	} 

	return $rulename;
}


sub getSvcName
{
	# set device-group DC-test-box service tcp-6346 protocol tcp port 6346
	# set device-group DC-test-box service tcp-6356 protocol tcp port 6356
	# set device-group DC-test-box service tcp-range-9000-9030 protocol tcp port 9000-9030
	my $retval = "";
	my $obj = shift;

	$obj =~ s/^set\ device\-group\ DC\-test\-box\ service\ //i; 
	if( $obj =~ /^\"/ )
	{
		#object with space in its name
		$obj =~ s/^"//; 
		$obj =~ s/".*//; 
		$retval = $obj;
	} else {
		my @parts = split( /\ /, $obj, 2 ); 
		$retval = $parts[0]; 
	} #fi

	return $retval
} #end sub


sub loadFile
{
	my @file;
	my $filename = shift;
	open( IN, $filename ) or die( $! );
	while( my $line = <IN> )
	{
		push( @file, $line );
	}
	close( IN );
	return @file;
} #end sub


my @file1 = loadFile( $file1 );
my @file2 = loadFile( $file2 );

foreach my $line1 ( @file1 )
{
	my $objname1 = "";
	chomp( $line1 );
	my $type1 = "";

	if( $line1 =~ m/^set\ device\-group\ DC\-test\-box\ service\ / ){
		#line is a service entry
		$type1 = "svc"; 
		$objname1 = getSvcName( "$line1" );
	} elsif( $line1 =~ m/^set\ device\-group\ DC\-test\-box\ nat\ rule/ ){
		$type1 = "nat";
	} elsif( $line1 =~ m/^set\ device\-group\ DC\-test\-box\ security\ rule/ ){
		$objname1 = getRuleName( "$line1" );
		$type1 = "sec";
	} elsif( $line1 =~ m/^set\ device\-group\ DC\-test\-box\ address.*/ ){
		#line is an address or address-group entry
		$type1 = "add";
		$objname1 = getAddObjName( "$line1" );
	} #fi

	foreach my $line2 ( @file2 )
	{
		my $objname2 = "";
		chomp( $line2 );
		my $type2 = "none";
		if( $line2 =~ m/^set\ device\-group\ DC\-test\-box\ service\ / ){
			#line is a service entry
			$type2 = "svc"; 
			$objname2 = getSvcName( "$line2" );
		} elsif( $line2 =~ m/^set\ device\-group\ DC\-test\-box\ nat\ rule/ ){
			$type2 = "nat";
		} elsif( $line2 =~ m/^set\ device\-group\ DC\-test\-box\ security\ rule/ ){
			$objname2 = getRuleName( "$line2" );
			$type2 = "sec";
		} elsif( $line2 =~ m/^set\ device\-group\ DC\-test\-box\ address.*/ ){
			#line is an address or address-group entry
			$type2 = "add";
			$objname2 = getAddObjName( "$line2" );
		} #fi

		if( ( $type1 eq $type2 ) and ( $objname1 eq $objname2 ) and ( $line1 ne $line2 ) )
		{
			printf "%-14s - %-3s - %s: %s\n", $file1, $type1, $objname1, $line1;
			printf "%-14s - %-3s - %s: %s\n\n", $file2, $type2, $objname2, $line2;
		} #fi

	} #end foreach

} #end foreach
