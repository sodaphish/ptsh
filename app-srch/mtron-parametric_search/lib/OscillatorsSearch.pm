# filename: OscillatorsSearch.pm
# (C)opyright 1999-2000, M-tron Industries, Inc., all rights reserved.
# 	written by Corey J. Steele <csteele@mtron.com>
# last modified: 12/12/2000
#
# Description: This library handles all of the search routines for the
#	oscillator line of products.  See "Documentation/Parametric Search"
#	for more information on how these routines work.
#
package OscillatorsSearch;



 
BEGIN {
	require Exporter;
	@EXPORT = qw( &OscillatorSearch );
	@ISA = qw( Exporter );

	use CGI;
	use lib qw( ../cfg );
	use NewLog;
	use ParseLib;
	use SearchLib;
	use Search;
	require "DSN_readonly.pl";
}




sub OscillatorSearch{

	LoadTemplate( "content/oscillator-search_results.con" );

	$main::__fam = CGI::param( "family" );
		Tokenize( 'FAMILY_PARAM', $main::__fam );
	$main::__tltemp = CGI::param( "tltemp" );
		Tokenize( 'LTEMP_PARAM', $main::__tltemp );
	$main::__utemp = CGI::param( "utemp" );
		Tokenize( 'UTEMP_PARAM', $main::__utemp );
	$main::__supvolt = CGI::param( "supply_voltage" );
		Tokenize( 'SUPVOLT_PARAM', $main::__supvolt );
	$main::__outlogic = CGI::param( "output_logic" );
		Tokenize( 'OUTPUT_LOGIC_PARAM', $main::__outlogic );
	$main::__symmetry = CGI::param( "symmetry" );
		Tokenize( 'SYMMETRY_PARAM', $main::__symmetry );
	$main::__stability = CGI::param( "stability" );
		Tokenize( 'STABILITY_PARAM', $main::__stability );
	$main::__footprint = CGI::param( "footprint" );
		Tokenize( 'FOOTPRINT_PARAM', $main::__footprint );
	$main::__output_type = CGI::param( "output_type" );
		Tokenize( 'OUTPUT_TYPE_PARAM', $main::__output_type );


	$main::httpHeaders .= "Family = $main::__fam}LowTemp = $main::__tltemp}HighTemp = $main::__utemp}SupplyVoltage = $main::__supvolt}OutputLogic = $main::__outlogic}Symmetry = $main::__symmetry}Stability = $main::__stability}Footprint = $main::__footprint}OutputType = $main::__output_type";
		Tokenize( 'HTTP_HEADERS', $main::httpHeaders );


	@matches = Oscillators_SearchSelect(); 
	@windowMatches = WindowMatches( $frame, @matches );

	$NumOfMatches = scalar( @matches );
	$end = $NumOfMatches;


	if( $NumOfMatches != 0 ){

		SetRanges( $NumOfMatches, $initialHere );

		Oscillators_RefineSelect( @matches );

		Parse( "EDIT_SEARCH", "RESULTS_HEADER" );


		$sqlstmt = "select * from ps_oscillators where ( id='$windowMatches[0]' ";
		for( my $i = 1; $i < scalar( @windowMatches ); $i++ ){
			$sqlstmt .= " or id ='$windowMatches[$i]'";
		}
		$sqlstmt .= ")";


		$dispStmt_h = $main::__dsn->prepare( $sqlstmt )
			or NewLog( 'wrn', '09', "Search() - Could not PREPARE '$sqlstmt'. ($DBI::errstr)" );
		$dispStmt_h->execute
			or NewLog( 'err', '09', "Search() - Could not EXECUTE '$sqlstmt'. ($DBI::errstr)" );

		my $white = 0;


		while( my( $id, $par, $std, $fam, $lte, $ute, $des, $sup, $out, $sym, $sta, $agi, 
		        $lfr, $ufr, $sfr, $pdf, $pac, $pri, $oul, $obs, $pkg ) = $dispStmt_h->fetchrow() ){

			Tokenize( "INDEX", $initialHere + 1 );
			Tokenize( "ID", $id );
			Tokenize( "PART_NUMBER", $par );
			Tokenize( "STD", $std ); 
			Tokenize( "OSCILLATOR_FAMILY", $fam );
			Tokenize( "LTEMP", $lte );
			Tokenize( "HTEMP", $ute );
			Tokenize( "DESCRIPTION", $des );
			Tokenize( "SUPPLY_VOLTAGE", $sup );
			Tokenize( "OUTPUT_LOGIC", $out );
			Tokenize( "SYMMETRY", $sym );
			Tokenize( "STABILITY", $sta );
			Tokenize( "AGING", $agi );
			Tokenize( "FREQ_LOWER", $lfr );
			Tokenize( "FREQ_UPPER", $ufr );
			Tokenize( "FREQ_STD", $sfr );
			Tokenize( "PACKAGE_TYPE", $pac );
			Tokenize( "PDF", $pdf );
			Tokenize( "PRICE", $pri );
			Tokenize( "FOOTPRINT", $pkg );
			Tokenize( "OUTPUT_TYPE", $pac );
			
			if( $__Tokens{'DESCRIPTION'} eq "" ){
				Tokenize( 'DESCRIPTION', "N/A" );
			}

			if( $Tokens{'PRICE'} eq "" ){
				Tokenize( 'PRICE', "CALL" );
			}

			if( $white ){
				Parse( "WHITE" ); 
				$white = 0;
			} else {
				Parse( "GREY" );
				$white = 1;
			}

			$initialHere++;

		} #end while


		Parse( "RESULTS_FOOTER" );

		PrevNext( $frame, $end ); 

	} else {

		Parse( "NO_RESULTS_HEADER", "RESULTS_FOOTER" );
		LogDeadEnd( '03' );

	}

} #end OscillatorSearch()




sub Oscillators_RefineSelect {

	local @matches = @_;

	my $sqlstmt2 = "select family, ltemp, utemp, supply_voltage, output_logic, symmetry, stability, package_type, pkg_type, description from ps_oscillators where ( id='$matches[0]' ";
	for( my $i = 1; $i <= scalar( @matches ); $i++ ){
		$sqlstmt2 .= " or id='$matches[$i]'";
	}
	$sqlstmt2 .= " )";

	@family_options = ();
	@tltemp_options = ();
	@utemp_options = ();
	@supply_voltage_options = ();
	@output_logic_options = ();
	@symmetry_options = ();
	@stability_options = ();
	@output_type_options = ();
	@footprint_options = ();

	$editStmt_h = $main::__dsn->prepare( $sqlstmt2 )
		or NewLog( 'wrn', '09', "Search() - could not PREPARE '$sqlstmt2'. ($DBI::errstr)" );
	$editStmt_h->execute
		or NewLog( 'err', '09', "Search() - could not EXECUTE '$sqlstmt2'. ($DBI::errstr)" );


	while( my( $fam, $lte, $ute, $sup, $out, $sym, $sta, $pac, $pkg, $des ) = $editStmt_h->fetchrow() ){

		push( @family_options, $fam ) if( ! IsIn( $fam, @family_options ) );
		push( @tltemp_options, $lte ) if( ! IsIn( $lte, @tltemp_options ) );
		push( @utemp_options, $ute ) if( ! IsIn( $ute, @utemp_options ) );
		push( @supply_voltage_options, $sup ) if( ! IsIn( $sup, @supply_voltage_options ) );
		push( @output_logic_options, $out ) if( ! IsIn( $out, @output_logic_options ) );
		push( @symmetry_options, $sym ) if( ! IsIn( $sym, @symmetry_options ) );
		push( @stability_options, $sta ) if( ! IsIn( $sta, @stability_options ) );
		push( @output_type_options, $des ) if( ! IsIn( $des, @output_type_options ) );
		push( @footprint_options, $pkg ) if( ! IsIn( $pkg, @footprint_options ) );

	} #end while

	Tokenize( 'FAMILY_OPTIONS', FormatDropList( $main::__fam, @family_options ) );
	Tokenize( 'LTEMP_OPTIONS', FormatDropList( $main::__tltemp, @tltemp_options ) );
	Tokenize( 'UTEMP_OPTIONS', FormatDropList( $main::__utemp, @utemp_options ) );
	Tokenize( 'SUPPLY_VOLTAGE_OPTIONS', FormatDropList( $main::__supvolt, @supply_voltage_options ) );
	Tokenize( 'OUTPUT_LOGIC_OPTIONS', FormatDropList( $main::__outlogic, @output_logic_options ) );
	Tokenize( 'SYMMETRY_OPTIONS', FormatDropList( $main::__symmetry, @symmetry_options ) );
	Tokenize( 'STABILITY_OPTIONS', FormatDropList( $main::__stability, @stability_options ) );
	Tokenize( 'OUTPUT_TYPE_OPTIONS', FormatDropList( $main::__output_type, @output_type_options ) );
	Tokenize( 'FOOTPRINT_OPTIONS', FormatDropList( $main::__footprint, @footprint_options ) );

} #end Oscillators_RefineSelect()




sub Oscillators_SearchSelect {

	my @matches = ();

	my $sqlstmt = "select id from ps_oscillators where ( ( ( freq_lower <= $main::__frequency and freq_upper >= $main::__frequency and freq_std is null ) or ( freq_std = $main::__frequency ) ) and package_type = '$main::__mounting' ";
	if( ! $main::__fam eq "" ){ $sqlstmt .= " and family = '$main::__fam'"; }
	if( ! $main::__supvolt eq "" ){ $sqlstmt .= " and supply_voltage like $main::__supvolt"; }
	if( ! $main::__outlogic eq "" ){ $sqlstmt .= " and output_logic = '$main::__outlogic'"; }
	if( ! $main::__symmetry eq "" ){ $sqlstmt .= " and symmetry = '$main::__symmetry'"; }
	if( ! $main::__stability eq "" ){ $sqlstmt .=" and stability = '$main::__stability'"; }
	if( ! $main::__output_type eq "" ){ $sqlstmt .=" and description = '$main::__output_type'"; }
	if( ! $main::__footprint eq "" ){ $sqlstmt .=" and pkg_type = '$main::__footprint'"; }
	if( ! $main::__tltemp eq "" and ! $main::__utemp eq "" ){
		$sqlstmt .= " and ( ltemp <= $main::__tltemp and utemp >= $main::__utemp )"; 
	} elsif( ! $main::__tltemp eq "" ){
		$sqlstmt .= " and ltemp <= $main::__tltemp";
	} elsif( ! $main::__utemp eq "" ){
		$sqlstmt .= " and utemp >= $main::__utemp";
	}

	$sqlstmt .= " and obsolete is NULL";
	$sqlstmt .= " ) order by freq_std desc";


	my $searchStmt_h = $main::__dsn->prepare( $sqlstmt )
		or NewLog( 'wrn', '09', "Search() - could not PREPARE '$sqlstmt'.  ($DBI::errstr)" );
	$searchStmt_h->execute
		or NewLog( 'err', '09', "Search() - could not EXECUTE '$sqlstmt'.  ($DBI::errstr)" );


	while( my( $id ) = $searchStmt_h->fetchrow() ){
		push( @matches, $id );
	}


	return @matches;

} #end Oscillators_SearchSelect()




1;
