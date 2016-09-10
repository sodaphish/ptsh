# filename: Search.pm
# (C)opyright 1999-2000, M-tron Industries, Inc., all rights reserved.
# 	written by Corey J. Steele <csteele@mtron.com>
#
# last modified: 07/05/2000
#
# Description: this is only the Search() routine, which routes traffic.  This
#	is in its own routine because originally there were several other functions
#	here as well, however many of those have been split out to SearchLib.pm and
#	as a result are no longer here.
#
package Search;
 
BEGIN {
	require Exporter;
	@EXPORT = qw( &Search $firstPage $initialHere $frame );
	@ISA = qw( Exporter );

	use CGI;
	use Env;
	use lib qw( ../cfg );
	use NewLog;
	use ParseLib;
	use SearchLib;
}


#
# this variable is absolutely necessary for purposes of passing failed query information on to the 
# contact parser. as well as for use with logging.
$main::httpHeaders = "";						# we'll start it empty.


#
#These variables are necessary for ALL searches.
$main::__family = CGI::param( "fam" );					# this is the family of products to search
	Tokenize( 'FAM', $main::__family );
$main::__mounting = CGI::param( "mount" );				# this is the mounting type the user wanted to use
	Tokenize( 'MOUNT', $main::__mounting );
	if( $main::__mounting eq "smt" ){
		Tokenize( 'PRETTY_MOUNT', "surface mount" );
	} else {
		Tokenize( 'PRETTY_MOUNT', "through hole" );
	}
$main::__frequency = CGI::param( "freq" ); 				# the frequency the user gave us.  we validate it, expand
	$main::__frequency = ExpandFrequency( $main::__frequency );	# 	it, and tokenize it
	Tokenize( 'FREQUENCY', $main::__frequency );
$main::__here = CGI::param( "here" );					# $main::__here is the bottom of the window we're in
	$main::__here = 0 if( !defined( $main::__here ) );
$firstPage = CGI::param( "firstpage" );					# tells us whether we should log this information b/c its from the first page
$initialHere = $main::__here;						# a variable to remember where $main::__here originally was
$frame = $main::__here + $main::__maxNumView;				# this is the size of the viewing window




#
# this is the new value of this variable for purposes of populating it.  :-)
$main::httpHeaders = "ProductType = $main::__family}MountType = $main::__mounting}Frequency = $main::__frequency}";
Tokenize( 'HTTP_HEADERS', $main::httpHeaders );




sub Search {

	LoadTemplate( "content/search.con" );

	# 
	# this is an error check to make sure we were able to format the 
	# frequency they gave us properly
	if( ! defined( $main::__frequency ) ){
		LoadTemplate( "content/error.con" );
		Parse( "ERR-202", "ERROR_FOOTER" );
		return;
	}


	#
	# the query is the first step in the search process, so we want to
	# log all of the data from that form filling.
	if( $firstPage ){

		#
		# we want to log the first page data to the database.
		NewLog( 'qry', '01', "$main::__family}$main::__mounting}$main::__frequency" );

	}


	#
	# this is the logic to determine which search to perform.  we also
	# take care of loading the necessary templates at this time.
	if( $main::__family eq "crystals" ){
		Tokenize( 'HELP_SUB_TOPIC', "Crystals" );
		use CrystalsSearch;
		CrystalSearch();
	} elsif( $main::__family eq "oscillators" ){
		Tokenize( 'HELP_SUB_TOPIC', "Oscillators" );
		use OscillatorsSearch;
		OscillatorSearch(); 
	} elsif( $main::__family eq "tcxos" ){
		Tokenize( 'HELP_SUB_TOPIC', "TCXOS" );
		use TCXOsSearch;
		TCXOSearch();
	} elsif( $main::__family eq "vcxos" ){
		Tokenize( 'HELP_SUB_TOPIC', "VCXOS" );
		use VCXOsSearch;
		VCXOSearch();
	} elsif( $main::__family eq "ocxos" ){
		Tokenize( 'HELP_SUB_TOPIC', "OCXOS" );
		use OCXOsSearch;
		OCXOSearch();
	} else {
		LoadTemplate( "content/error.con" );
		Parse( "ERR-200", "ERROR_FOOTER" );
	}

} #end Search()




1; 
