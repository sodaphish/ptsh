# filename: CrystalsSearch.pm
# (C)opyright 1999-2000, M-tron Industries, Inc., all rights reserved.
#	written by Corey J. Steele <csteele@mtron.com>
# last updated; 12/12/2000
# 
# Description: This library handles all of the search routines for the 
# 	crystal line of products.  See "Documentation/Parametric Search"
#	for more information on how these routines work.
#
package CrystalsSearch;



 
BEGIN {
	require Exporter;
	@EXPORT = qw( &CrystalSearch );
	@ISA = qw( Exporter );

	use CGI;
	use lib qw( ../cfg );
	use NewLog;
	use ParseLib;
	use SearchLib;
	use Search;
	require "DSN_readonly.pl";

}




sub CrystalSearch {
	
	LoadTemplate( "content/crystal-search_results.con" );

	$main::__fam = CGI::param( "family" );
		Tokenize( 'FAMILY_PARAM', $main::__fam );
	$main::__tol = CGI::param( "tol" );
		Tokenize( 'TOL_PARAM', $main::__tol );
	$main::__stab = CGI::param( "stab" );
		Tokenize( 'STAB_PARAM', $main::__stab );
	$main::__tltemp = CGI::param( "tltemp" );
		Tokenize( 'LTEMP_PARAM', $main::__tltemp );
	$main::__utemp = CGI::param( "utemp" );
		Tokenize( 'UTEMP_PARAM', $main::__utemp );
	$main::__pkg_type = CGI::param( "pkg_type" ); 
		Tokenize( 'PKG_TYPE', $main::__pkg_type );

	# 
	# we use $main::httpHeaders to maintain state in certain circumstances (for instance, in dead-end searches we can tell
	# what part they were looking for that got them to the dead end search.)
	$main::httpHeaders .= "Family = $main::__fam}Tolerance = $main::__tol}Stability = $main::__stab}LowTemp = $main::__tltemp}HighTemp = $main::__utemp}Package Type = $main::__pkg_type";
		Tokenize( 'HTTP_HEADERS', $main::httpHeaders );


	@matches = Crystals_SearchSelect(); 


	#
	# here, we get only the matches that fall within our current viewing window and slap them into an array.
	@windowMatches = WindowMatches( $frame, @matches ); 


	$NumOfMatches = scalar( @matches ); # this is total matches

	# what is $end for?
	$end = $NumOfMatches;


	# shouldn't this actually use @windowMatches instead of @matches?
	if( $NumOfMatches != 0 ){

		SetRanges( $NumOfMatches, $initialHere );

		Crystals_RefineSelect( @matches );


		Parse( "EDIT_SEARCH", "RESULTS_HEADER" );


		$sqlstmt = "select * from ps_crystals where ( id='$windowMatches[0]' ";
		for( my $i = 1; $i < scalar( @windowMatches ); $i++ ){
			$sqlstmt .= " or id='$windowMatches[$i]'";
		}
		$sqlstmt .= ")";


		$dispStmt_h = $main::__dsn->prepare( $sqlstmt )
			or NewLog( 'wrn', '08', "Search() - Could not PREPARE '$sqlstmt'. ($DBI::errstr)" );
		$dispStmt_h->execute
			or NewLog( 'err', '08', "Search() - Could not EXECUTE '$sqlstmt'. ($DBI::errstr)" );


		my $white = 0; #we want grey first


		#
		#here, we're actually outputting the results of the query
		# -- this is really big and ugly, and I appologize for that.
		while( my( $id, $par, $std, $fam, $cut, $mod, $loa, $lte, $ute, $vad, 
			$tol, $sta, $agi, $lfr, $ufr, $sfr, $pdf, $pac, $pri, $obs, 
			$pkg ) = $dispStmt_h->fetchrow() ){

			#$tol = DropZeros( $tol );
			$tol = sprintf( "%6i", $tol );

			#
			#these look worse than they are; these just export the results of the last fetchrow() 
			#to ParseLib-available keys 
			Tokenize( "INDEX", $initialHere + 1 );
			Tokenize( "PART_NUMBER", $par );
			Tokenize( "STD", $std );
			Tokenize( "FAMILY", $fam );
			Tokenize( "CUT", $cut );
			Tokenize( "MODE", $mod );
			Tokenize( "LOAD", $loa );
			Tokenize( "LTEMP", $lte );
			Tokenize( "HTEMP", $ute );
			Tokenize( "VAD", $vad );
			Tokenize( "TOLERANCE", $tol );
			Tokenize( "STABILITY", $sta );
			Tokenize( "PRICE", "$pri" );
			Tokenize( "AGING", $agi );
			Tokenize( "FREQ_LOWER", $lfr );
			Tokenize( "FREQ_UPPER", $ufr );
			Tokenize( "PACKAGE_TYPE", $pac );
			Tokenize( "FREQ_STD", $sfr );
			Tokenize( "PDF", $pdf );
			Tokenize( "PKG_TYPE2", $pkg );


			#
			#we need to padd un-filled VAD's
			if( $__Tokens{'VAD'} eq "" ){

				Tokenize( 'VAD', "N/A" );

			}

 
			#
			#we don't want to display a price of zero, that might give people the wrong idea.
			if( $__Tokens{'PRICE'} <= 0 ){
				Tokenize( "PRICE", "CALL" );
			} else {
				$pri = "\$" . $pri; 
				Tokenize( "PRICE", $pri );
			}


			if( $white ){

				Parse( "WHITE" );
				$white = 0;

			} else {

				Parse( "GREY" );
				$white = 1;

			} #end if 

			$initialHere++;


		} #end while loop


		#close off the table that handles the results
		Parse( "RESULTS_FOOTER" );


		PrevNext( $frame, $end );

	} else {

		#nothing was found that matched their query, what should we do?
		Parse( "NO_RESULTS_HEADER", "RESULTS_FOOTER" );
		LogDeadEnd( '02' );

 	}

} #end CrystalSearch()




sub Crystals_RefineSelect {

	my @matches = @_;

	
	#
	# here, we'll form the sql statement that will get us the values for our drop box options for the user to refine their search.
	my $sqlstmt2 = "select family, tolerance, stability, lemp, utemp, pkg_type from ps_crystals where ( id='$matches[0]' ";
	for( my $i=1; $i <= scalar( @matches ); $i++ ){
		$sqlstmt2 .= " or id='$matches[$i]'";
	}
	$sqlstmt2 .= " )";


	#
	# create some empty arrays that will eventually hold the return values from the SQL statement ($sqlstmt2)
	my @family_options = ();
	my @tol_options = ();
	my @stab_options = ();
	my @tltemp_options = ();
	my @utemp_options = ();
	my @pkg_type_options = ();


	$editStmt_h = $main::__dsn->prepare( $sqlstmt2 )
		or NewLog( 'wrn', '08', "Search() - Could not PREPARE '$sqlstmt'. ($DBI::errstr)" );
	$editStmt_h->execute()
		or NewLog( 'err', '08', "Search() - Could not EXECUTE '$sqlstmt'. ($DBI::errstr)" );


	while( my( $fam, $tol, $stab, $lte, $ute, $pkg ) = $editStmt_h->fetchrow() ){

		push( @family_options, $fam ) if( ! IsIn( $fam, @family_options ) );
		push( @tol_options, sprintf( "%6i", $tol ) ) if( ! IsIn( sprintf( "%6i", $tol ), @tol_options ) ); # these sprintfs are hacks, they suck
		push( @stab_options, $stab ) if( ! IsIn( $stab, @stab_options ) );
		push( @tltemp_options, $lte ) if( ! IsIn( $lte, @tltemp_options ) );
		push( @utemp_options, $ute ) if( ! IsIn( $ute, @utemp_options ) );
		push( @pkg_type_options, $pkg ) if( ! IsIn( $pkg, @pkg_type_options ) );

	} #end while loop


	# 
	# this makes the drop box lists and exports them as tokens
	#  - FormatDropList() is in SearchLib.pm
	Tokenize( 'UTEMP_OPTIONS', FormatDropList( $main::__utemp, @utemp_options ) );
	Tokenize( 'LTEMP_OPTIONS', FormatDropList( $main::__tltemp, @tltemp_options ) );
	Tokenize( 'STABILITY_OPTIONS', FormatDropList( $main::__stab, @stab_options ) );
	Tokenize( 'TOLERANCE_OPTIONS', FormatDropList( $main::__tol, @tol_options ) ); 
	Tokenize( 'FAMILY_OPTIONS', FormatDropList( $main::__fam, @family_options ) );
	Tokenize( 'PKG_TYPE_OPTIONS', FormatDropList( $main::__pkg_type, @pkg_type_options ) );

} #end Crystals_RefineSelect()




#
# Crystals_SearchSelect() - searches ALL of the crystals for parts matching the criteria
# when a match is found, it is pushed onto the @matches array.  The @matches array is 
# evnetually returned containing the Crystal table ID of all the matching crystals.
sub Crystals_SearchSelect {

	#
	# this is the container we'll put our results in to return...
	# do not confuse this with the variable @Search::matches, they are not the same.
	my @matches = ();

	#
	# this is the absolute _bare_ SQL statement we'll execute, (minus a closing parans.)
	my $sqlstmt = "select id from ps_crystals where ( ( ( freq_lower <= $main::__frequency and freq_upper >= $main::__frequency and freq_std is null ) or ( freq_std = $main::__frequency ) ) and package_type = '$main::__mounting' "; 

	#
	#if the user specifies a different package type, include that in the search.
	if( ! $main::__fam eq "" ){ $sqlstmt .= " and family = '$main::__fam'"; }

	#
	#if the user specifies a tolerance, include it in the search.
	if( ! $main::__tol eq "" ){ $sqlstmt .= " and tolerance = '$main::__tol'"; }  #again, the sprintf is a hack to fix a precision bug.

	#
	#if the user specifies a stability, include it in the search.
	if( ! $main::__stab eq "" ){ $sqlstmt .= " and stability = '$main::__stab'"; }

	#
	#
	#if the user specifies a stability, include it in the search.
	if( ! $main::__pkg_type eq "" ){ $sqlstmt .= " and pkg_type = '$main::__pkg_type'"; }

	#
	# we've got to handle temperatures in a special way... take into consideration
	# all possible cases the user would want.
	if( ! $main::__tltemp eq "" and ! $main::__utemp eq "" ){ 
		$sqlstmt .= " and ( lemp <= $main::__tltemp and utemp >= $main::__utemp )"; 
	} elsif( ! $main::__tltemp eq "" ){
		$sqlstmt .= " and lemp <= $main::__tltemp";
	} elsif( ! $main::__utemp eq "" ){
		$sqlstmt .= " and utemp >= $main::__utemp";
	}

	#
	# get rid of obsolete parts
	$sqlstmt .= " and obsolete is NULL";

	#
	# this finishes $sqlstmt off.
	$sqlstmt .= ") order by freq_std desc";


	my $searchStmt_h = $main::__dsn->prepare( $sqlstmt )
		or NewLog( 'wrn', '08', "Search() - Could not PREPARE searchSelect statement. ($DBI::errstr)" );
	$searchStmt_h->execute
		or NewLog( 'err', '08', "Search() - Could not EXECUTE searchSelect statement. ($DBI::errstr)" );


	#
	# get the results of the SQL statement and put them in the array @matches
	while( my( $id ) = $searchStmt_h->fetchrow() ){
		push( @matches, $id );
	}

	return @matches;

} #end Crystals_SearchSelect()




1; #end CrystalsSearch.pm
