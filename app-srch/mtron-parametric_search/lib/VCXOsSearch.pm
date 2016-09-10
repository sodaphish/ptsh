# filename: VCXOsSearch.pm
# (C)opyright 1999, M-tron Industries, Inc., all rights reserved.
# 	written by Corey J. Steele <csteele@mtron.com>
# last modified: 12/12/2000
#
# Description: This library handles all of the search routines for the 
#	VCXO line of products.  See "Documentation/Parametric Search" for
#	more information on how these routines work.
#
package VCXOsSearch;



 
BEGIN {
	require Exporter;
	@EXPORT = qw( &VCXOSearch );
	@ISA = qw( Exporter );

	use CGI;
	use lib qw( ../cfg );
	use NewLog;
	use ParseLib;
	use SearchLib;
	use Search;
	require "DSN_readonly.pl";

}




sub VCXOSearch {
	LoadTemplate( "content/vcxo-search_results.con" );

	#
	# these are all variables taht are 'specific' to this search
	# the scope is not specific, but they should only be filled 
	# (or populated) in this search.
	$main::__fam = CGI::param( "family" );
		Tokenize( 'FAMILY_PARAM', $main::__fam );
	$main::__tltemp = CGI::param( "tltemp" );
		Tokenize( 'LTEMP_PARAM', $main::__tltemp );
	$main::__utemp = CGI::param( "utemp" );
		Tokenize( 'UTEMP_PARAM', $main::__utemp );
	$main::__stability = CGI::param( "stability" );
		Tokenize( 'STABILITY_PARAM', $main::__stability );
	$main::__symmetry = CGI::param( "symmetry" );
		Tokenize( 'SYMMETRY_PARAM', $main::__symmetry );
	$main::__outlogic = CGI::param( "output_logic" );
		Tokenize( 'OUTPUT_LOGIC_PARAM', $main::__outlogic );
	$main::__pull = CGI::param( "pull" );
		Tokenize( 'PULLABILITY_PARAM', $main::__pull );
	$main::__supvolt = CGI::param( "supply_voltage" );
		Tokenize( 'SUPPLY_VOLTAGE_PARAM', $main::__supvolt );
	$main::__package_type = CGI::param( "package_type" );
		Tokenize( 'PACKAGE_TYPE_PARAM', $main::__package_type );

	$main::httpHeaders .= "Family = $main::__fam}LowTemp = $main::__tltemp}HighTemp = $main::__utemp}Stability = $main::__stability}OutputLogic = $main::__outlogic}SupplyVoltage = $main::__supvolt}Pullability = $main::__pull}PackageType = $main::__package_type";
	Tokenize( 'HTTP_HEADERS', $main::httpHeaders );

	#
	# get the matches and put them in the array @matches.
	@matches = VCXOs_SearchSelect();

	#
	# get the IDs of the matches in the current window.
	@windowMatches = WindowMatches( $frame, @matches );

	$NumOfMatches = scalar( @matches );
	$end = $NumOfMatches;
	

	if( $NumOfMatches != 0 ){

		#
		# this sets the tokens needed to properly display the search headers
		SetRanges( $NumOfMatches, $initialHere );

		VCXOs_RefineSelect( @matches );

		#
		# output the initial headers of the search...
		Parse( "EDIT_SEARCH", "RESULTS_HEADER" );
 
		my $sqlstmt = "select * from ps_vcxos where ( id='$windowMatches[0]'";
		for( my $i = 1; $i < scalar( @windowMatches ); $i++ ){
			$sqlstmt .= " or id='$windowMatches[$i]'";
		} $sqlstmt .= " )";

		my $dispStmt_h = $main::__dsn->prepare( $sqlstmt )
			or NewLog( 'wrn', '0B', "Search() - Could not PREPARE '$sqlstmt'.  ($DBI::errstr)" );
		$dispStmt_h->execute
			or NewLog( 'err', '0B', "Search() - Could not EXECUTE '$sqlstmt'. ($DBI::errstr)" );

		my $white = 0;

		while( my( $id, $fam, $par, $lte, $ute, $sta, $fre, $sym, $log, $pul, $pckg, $sup, $pdf, 
			$pck, $tech, $lfr, $ufr, $sfr ) = $dispStmt_h->fetchrow() ){

			$sup = DropZeros( $sup );

			Tokenize( 'INDEX', $initialHere + 1 );
			Tokenize( 'ID', $id );
			Tokenize( '_FAMILY', $fam ); 
			Tokenize( 'PART_NUMBER', $par );
			Tokenize( 'LTEMP', $lte );
			Tokenize( 'UTEMP', $ute );
			Tokenize( 'STABILITY', $sta );
			Tokenize( 'OUTPUT_TYPE', $fre );
			Tokenize( 'SYMMETRY', $sym );
			Tokenize( 'OUTPUT_LOGIC', $log );
			Tokenize( 'PULL', $pul );
			Tokenize( 'PCKG_INFO', $pckg );
			Tokenize( 'SUPPLY_VOLTAGE', $sup );
			Tokenize( 'PDF', $pdf );
			Tokenize( 'PCKG', $pck );
			Tokenize( 'TECHNOLOGY', $tech );
			Tokenize( 'FREQ_LOWER', $lfr );
			Tokenize( 'FREQ_UPPER', $ufr );
			Tokenize( 'FREQ_STD', $sfr );

			if( $sym eq "" ){ Tokenize( 'SYMMETRY', "N\A" ); }

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
		# this outputs the next and prev links at the bottom
		PrevNext( $frame, $end );

	} else {

		Parse( "NO_RESULTS_HEADER", "RESULTS_FOOTER" );
		LogDeadEnd( '05' );

	}

} #end VCXOSearch()


sub VCXOs_RefineSelect {

	local @matches = @_;

	my $sqlstmt = "select family, ltemp, utemp, stability, symmetry, logic, supply_voltage, pull, pckg_info from ps_vcxos where ( id='$matches[0]'";
	for( my $i = 1; $i < scalar( @matches ); $i++ ){
		$sqlstmt .= " or id='$matches[$i]'";
	} $sqlstmt .= " )";

	@family_options = ();
	@tltemp_options = ();
	@utemp_options = ();
	@stability_options = ();
	@symmetry_options = ();
	@output_logic_options = ();
	@supply_voltage_options = ();
	@pullability_options = ();
	@package_type_options = ();
	
	my $editStmt_h = $main::__dsn->prepare( $sqlstmt )
		or NewLog( 'wrn', '0B', "Search() - Could not PREPARE '$sqlstmt'. ($DBI::errstr)" );
	$editStmt_h->execute
		or NewLog( 'err', '0B', "Search() - Could not EXECUTE '$sqlstmt'. ($DBI::errstr)" );

	while( my( $fam, $lte, $ute, $sta, $sym, $log, $sup, $pull, $pck ) = $editStmt_h->fetchrow() ){
		push( @family_options, $fam ) if( ! IsIn( $fam, @family_options ) );
		push( @tltemp_options, $lte ) if( ! IsIn( $lte, @tltemp_options ) );
		push( @utemp_options, $ute ) if( ! IsIn( $ute, @utemp_options ) );
		push( @stability_options, $sta ) if( ! IsIn( $sta, @stability_options ) );
		push( @symmetry_options, $sym ) if( ! IsIn( $sym, @symmetry_options ) );
		push( @output_logic_options, $log ) if( ! IsIn( $log, @output_logic_options ) );
		push( @supply_voltage_options, DropZeros( $sup ) ) if( ! IsIn( DropZeros( $sup ), @supply_voltage_options ) );
		push( @pullability_options, $pull ) if( ! IsIn( $pull, @pullability_options ) );
		push( @package_type_options, $pck ) if( ! IsIn( $pck, @package_type_options ) );
	} #end while

	Tokenize( 'FAMILY_OPTIONS', FormatDropList( $main::__fam, @family_options ) );
	Tokenize( 'LTEMP_OPTIONS', FormatDropList( $main::__tltemp, @tltemp_options ) );
	Tokenize( 'UTEMP_OPTIONS', FormatDropList( $main::__utemp, @utemp_options ) );
	Tokenize( 'STABILITY_OPTIONS', FormatDropList( $main::__stability, @stability_options ) );
	Tokenize( 'SYMMETRY_OPTIONS', FormatDropList( $main::__symmetry, @symmetry_options ) );
	Tokenize( 'OUTPUT_LOGIC_OPTIONS', FormatDropList( $main::__outlogic, @output_logic_options ) );
	Tokenize( 'SUPPLY_VOLTAGE_OPTIONS', FormatDropList( $main::__supvolt, @supply_voltage_options ) );
	Tokenize( 'PULLABILITY_OPTIONS', FormatDropList( $main::__pull, @pullability_options ) );
	Tokenize( 'PACKAGE_TYPE_OPTIONS', FormatDropList( $main::__package_type, @package_type_options ) );

} #end VCXOs_RefineSelect()


sub VCXOs_SearchSelect {
	my @matches = ();

	my $sqlstmt = "select id from ps_vcxos where ( ( ( freq_lower <= $main::__frequency and freq_upper >= $main::__frequency and freq_std is null ) or ( freq_std = $main::__frequency) ) and pckg='$main::__mounting' ";

	if( $main::__fam ne "" ){ $sqlstmt .= " and family='$main::__fam'"; }
	if( $main::__stability ne "" ){ $sqlstmt .= " and stability like $main::__stability"; }
	if( $main::__symmetry ne "" ){ $sqlstmt .= " and symmetry='$main::__symmetry'"; }
	if( $main::__outlogic ne "" ){ $sqlstmt .= " and logic='$main::__outlogic'"; }
	if( $main::__supvolt ne "" ){ $sqlstmt .= " and supply_voltage like " . sprintf( "%1.2f", $main::__supvolt); }
	if( $main::__pull ne "" ){ $sqlstmt .=" and pull>=$main::__pull"; }
	if( $main::__package_type ne "" ){ $sqlstmt .= " and pckg_info = '$main::__package_type'"; }
	if( $main::__tltemp ne "" and $main::__utemp ne "" ){
		$sqlstmt .= " and ( ltemp <= $main::__tltemp and utemp >= $main::__utemp )";
	} elsif( $main::__tltemp ne "" ){
		$sqlstmt .= " and ltemp <= $main::__tltemp";
	} elsif( $main::__utemp ne "" ){
		$sqlstmt .= " and utemp >= $main::__utemp";
	}
	
	$sqlstmt .= " and obsolete is null";

	$sqlstmt .= " ) order by freq_std desc";

	my $stmt_h = $main::__dsn->prepare( $sqlstmt )
		or NewLog( 'wrn', '0B', "Search() - Could not PREPARE '$sqlstmt'. ($DBI::errstr)" );
	$stmt_h->execute
		or NewLog( 'err', '0B', "Search() - Could not EXECUTE '$sqlstmt'. ($DBI::errstr)" );

	while( my( $id ) = $stmt_h->fetchrow() ){
		push( @matches, $id );
	}

	return @matches;

} #end of VCXOs_SearchSelect()

1;
