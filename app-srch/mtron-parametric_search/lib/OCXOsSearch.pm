# filename: OCXOsSearch.pm
#  (C)opyright 1999-2000, M-tron Industries, Inc., all rights reserved.
#  written by Corey J. Steele <csteele@mtron.com>
#
package OCXOsSearch;
 
BEGIN {
	require Exporter;
	@EXPORT = qw( &OCXOSearch );
	@ISA = qw( Exporter );

	use CGI;
	use NewLog;
	use ParseLib;
	use SearchLib;
	use Search;
}


sub OCXOSearch {
	LoadTemplate( "content/ocxo-search_results.con" );

	#
	# these are all variables that are 'specific' to this search
	# the scope is not specific (i.e. $main::), but they should only be
	# filled in this search
	$main::__fam = CGI::param( "family" );
		Tokenize( 'FAMILY_PARAM', $main::__fam );
	$main::__tltemp = CGI::param( "tltemp" );
		Tokenize( 'LTEMP_PARAM', $main::__tltemp );
	$main::__utemp = CGI::param( "utemp" );
		Tokenize( 'UTEMP_PARAM', $main::__utemp );
	$main::__stability = CGI::param( "stability" );
		Tokenize( 'STABILITY_PARAM', $main::__stability );
	$main::__outlogic = CGI::param( "output_logic" );
		Tokenize( 'OUTPUT_LOGIC_PARAM', $main::__outlogic );
	$main::__supvolt = CGI::param( "supply_voltage" );
		Tokenize( 'SUPVOLT_PARAM', $main::__supvolt );

	$main::httpHeaders .= "Family = $main::__fam}LowTemp = $main::__tltemp}HighTemp = $main::__utemp}Stability = $main::__stability}OutputLogic = $main::__outlogic}SupplyVoltage = $main::__supvolt";
	Tokenize( 'HTTP_HEADERS', $main::httpHeaders );

	# 
	# them in the array @matches.
	@matches = OCXOs_SearchSelect();

	#
	# get the IDs of the matches that are currently within our viewing
	# window
	@windowMatches = WindowMatches( $frame, @matches );

	$NumOfMatches = scalar( @matches );
	$end = $NumOfMatches;

	if( $NumOfMatches != 0 ){

		#
		# this sets the tokens needed to properly output the 
		# search header
		SetRanges( $NumOfMatches, $initialHere );

		OCXOs_RefineSelect( @matches );

		#
		# output the initial headers of the search
		Parse( "EDIT_SEARCH", "RESULTS_HEADER" );

		my $sqlstmt = "select * from ocxos where( id='$windowMatches[0]' ";
		for( my $i = 1; $i < scalar( @windowMatches ); $i++ ){
			$sqlstmt .= " or id='$windowMatches[$i]'"; 
		} $sqlstmt .= ")";

		my $dispStmt_h = $main::__dsn->prepare( $sqlstmt)
			or NewLog( 'wrn', '0C', "Search() - Could not PREPARE '$sqlstmt'. ($DBI::errstr)" );
		$dispStmt_h->execute
			or NewLog( 'err', '0C', "Search() - Could not EXECUTE '$sqlstmt'. ($DBI::errstr)" );

		#
		# we use this to key which color of output we're supposed to show.
		my $white = 0;

		while( my( $id, $fami, $par, $lte, $ute, $sta, $fre, $log, $pck, $sup, 
			$pdf, $pckg, $fam, $lfr, $ufr ) = $dispStmt_h->fetchrow() ){

			$sup = DropZeros( $sup );
			$sta = DropZeros( $sta );

			Tokenize( 'INDEX', $initialHere + 1 );
			Tokenize( 'ID', $id );
			Tokenize( 'FAMILY', $fami );
			Tokenize( 'PART_NUMBER', $par );
			Tokenize( 'LTEMP', $lte );
			Tokenize( 'UTEMP', $ute );
			Tokenize( 'STABILITY', $sta );
			Tokenize( 'FREQ_CONTROL', $fre );
			Tokenize( 'LOGIC', $log );
			Tokenize( 'PCKG_INFO', $pck );
			Tokenize( 'SUPPLY_VOLTAGE', $sup );
			Tokenize( 'PDF', $pdf );
			Tokenize( 'PCKG', $pckg );
			Tokenize( 'TECHNOLOGY', $fam );
			Tokenize( 'FREQ_LOWER', $lfr );
			Tokenize( 'FREQ_UPPER', $ufr );

			if( $white ){
				Parse( "WHITE" );
				$white = 0;
			} else {
				Parse( "GREY" );
				$white = 1;
			}
			
			$initialHere++;

		} #end output while

		Parse( "RESULTS_FOOTER" );

		#
		# this prints the previous and next links at the bottom of the search.
		PrevNext( $frame, $end );

	} else {

		Parse( "NO_RESULTS_HEADER", "RESULTS_FOOTER" );
		LogDeadEnd( '06' );

	}

} #end OCXOSearch()




sub OCXOs_RefineSelect {

	local @matches = @_;

	my $sqlstmt = "select family, ltemp, utemp, stability, logic, supply_voltage from ocxos where ( id='$matches[0]'";
	for( my $i = 1; $i < scalar( @matches ); $i++ ){
		$sqlstmt .= " or id='$matches[$i]'";
	} $sqlstmt .= " )";

	@family_options = ();
	@tltemp_options = ();
	@utemp_options = ();
	@stability_options = ();
	@logic_options = ();
	@supply_voltage_options = ();

	$editStmt_h = $main::__dsn->prepare( $sqlstmt )
		or NewLog( 'wrn', '0C', "Search() - Could not PREPARE '$sqlstmt'. ($DBI::errstr)" );
	$editStmt_h->execute
		or NewLog( 'err', 'OC', "Search() - Could not EXECUTE '$sqlstmt'. ($DBI::errstr)" );

	while( my( $fam, $lte, $ute, $sta, $log, $sup ) = $editStmt_h->fetchrow() ){
		push( @family_options, $fam ) if( ! IsIn( $fam, @family_options ) );
		push( @tltemp_options, $lte ) if( ! IsIn( $lte, @tltemp_options ) );
		push( @utemp_options, $ute ) if( ! IsIn( $ute, @utemp_options ) );
		push( @stability_options, DropZeros( $sta ) ) if( ! IsIn( DropZeros( $sta ), @stability_options ) );
		push( @logic_options, $log ) if( ! IsIn( $log, @logic_options ) );
		push( @supply_voltage_options, $sup ) if( ! IsIn( $sup, @supply_voltage_options ) );
	} #end while

	Tokenize( 'FAMILY_OPTIONS', FormatDropList( $main::__fam, @family_options ) );
	Tokenize( 'LTEMP_OPTIONS', FormatDropList( $main::__tltemp, @tltemp_options ) );
	Tokenize( 'UTEMP_OPTIONS', FormatDropList( $main::__utemp, @utemp_options ) );
	Tokenize( 'STABILITY_OPTIONS', FormatDropList( $main::__stability, @stability_options ) );
	Tokenize( 'SUPPLY_VOLTAGE_OPTIONS', FormatDropList( $main::__supvolt, @supply_voltage_options ) );
	Tokenize( 'OUTPUT_LOGIC_OPTIONS', FormatDropList( $main::__outlogic, @logic_options ) );

} #end OCXOs_RefineSelect()



sub OCXOs_SearchSelect {
	my @matches = ();

	my $sqlstmt = "select id from ocxos where (pckg='$main::__mounting' and (freq_lower <= $main::__frequency and freq_upper >= $main::__frequency)";

	if( $main::__fam ne "" ){ $sqlstmt .= " and family='$main::__fam'"; }
	if( $main::__stability ne "" ){ $sqlstmt .= " and stability like " . sprintf( "%10.6f", $main::__stability ); }
	if( $main::__outlogic ne "" ){ $sqlstmt .= " and logic='$main::__outlogic'"; }
	if( $main::__supvolt ne "" ){ $sqlstmt .= " and supply_voltage='$main::__supvolt'"; }
	if( $main::__tltemp ne "" and $main::__utemp ne "" ){ 
		$sqlstmt .= " and ( ltemp <= $main::__tltemp and utemp >= $main::__utemp )";
	} elsif( $main::__tltemp ne "" ){
		$sqlstmt .= " and ltemp <= $main::__tltemp"; 
	} elsif( $main::__utemp ne "" ){
		$sqlstmt .= " and utemp >= $main::__utemp";
	}

	$sqlstmt .= "and obsolete is null";

	$sqlstmt .= " )";
	
	my $stmt_h = $main::__dsn->prepare( $sqlstmt );
		#or NewLog( 'wrn', "Search() - Could not PREPARE '$sqlstmt'. ($DBI::errstr)" );
	$stmt_h->execute;
		#or Log( 'err', "Search() - Could not EXECUTE '$sqlstmt'. ($DBI::errstr)" );

	while( my( $id ) = $stmt_h->fetchrow() ){
		push( @matches, $id );
	}

	return @matches;

} #end OCXOs_SearchSelect();




1;
