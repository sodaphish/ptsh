#!/usr/bin/perl
# bobfus.pl v.0.0.1 by C.J. Steele, CISSP
#  (C)opyright 2005, C.J. Steele, all rights reserved.
#
# Binary OBFUScator (bobfus) - a command-line blowfish encryptor and decryptor 
#
# usage: 
#  bobfus -e -k "pass phrase" inputfilename outputfile
#  bobfus -d -k "pass phrase" inputfilename outputfile
#
use strict; 
use Crypt::CBC;
use Getopt::Std;
use MIME::Base64;


#
# print our usage if we haven't even go the right number of args.
usage() if( scalar( @ARGV ) < 5 );


my %o; getopts( 'edk:?', \%o);
my $DEBUG = 1;


if( exists $o{'e'} and $o{'k'} )
{

	# encrypt a file
	print "D: We're encrypting a file...\n" if( $DEBUG );
	my $in = $ARGV[0];
	print "D: our input file is $in\n" if( $DEBUG );
	my $out = $ARGV[1]; 
	print "D: our output file is $out\n" if( $DEBUG );

	if( -e $in and ! -e $out ) 
	{
		my $cipher = Crypt::CBC->new( -key => "$o{'k'}", -cipher => 'Rijndael', -salt => 1 );
		$cipher->start( 'encrypting ');
		open( IN, "<$in" ) or die( "$!" );
		open( OUT, ">$out" ) or die( "$!" );
		while( my $buffer = <IN> )
		{
		    print OUT $cipher->crypt( $buffer );
		}
		print OUT $cipher->finish;
		close( OUT );
		close( IN );
		print "D: file encrypted.\n" if( $DEBUG );
	} else {
		print "E: there's a problem with your source and destination files.\n";
		exit( 1 );
	}

} elsif( exists $o{'d'} and $o{'k'} ){

	# decrypt a file
	my $cipher = Crypt::CBC->new( -key => "$o{'k'}", -cipher => 'Rijndael', -salt => 1 );
	$cipher->start( 'decrypting' );
	print "D: We're decrypting a file...\n" if( $DEBUG );
	my $in = $ARGV[0];
	print "D: our input file is $in\n" if( $DEBUG );
	my $out = $ARGV[1]; 
	print "D: our output file is $out\n" if( $DEBUG );

	if( -e $in and ! -e $out ) 
	{
		open( IN, "<$in" ) or die( "$!" );
		open( OUT, ">$out" ) or die( "$!" );
		while( my $buffer = <IN> )
		{
		    print OUT $cipher->crypt( $buffer );
		}
		print OUT $cipher->finish;
		close( OUT );
		close( IN );
		print "D: file decrypted.\n" if( $DEBUG );
	} else {
		print "E: there's a problem with your source and destination files.\n";
		exit( 1 );
	}

} else {

	# neither encrypt nor decrypt was specified or we don't have a key...
	usage();

}

exit( 0 );




sub usage
{
	print "usage: bobfus -[e|d] -k \"pass phrase\" inputfile outputfile\n";
	print "bobfus by C.J. Steele, CISSP <coreyjsteele\@yahoo.com>\n\n";
	exit( 1 );
}
