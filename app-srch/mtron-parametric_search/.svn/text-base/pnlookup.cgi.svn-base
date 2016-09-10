#!/usr/bin/perl
print "Content-type: text/html", "\n\n";

use lib 'lib';
use ParseLib;
use CGI param;
use DBI;

$dsn = DBI->connect( 'DBI:mysql:search', 'search', 'readonly' ) or
  die "Connect error: $DBI::errstr\n";


$query = param( "query" );
	Tokenize( 'QUERY', $query );
@tables = ( "crystals", "oscillators", "tcxos", "vcxos", "ocxos" );


LoadTemplate( "content/pnlookup.tmpl" );

if( $query eq "" ){

	#
	# there wasn't a query, we need to display the prompting dialog
	Parse( "HEADER", "ENTRY_FORM", "FOOTER" );

} else {

	#
	# we've got something, process the search.
	Parse( "HEADER" );

	my @results = ();

	foreach $table ( @tables ){

		Tokenize( 'TABLE', $table );

		if( $table eq "crystals" ){
			my $sqlstmt = "select part_number, family, cut, mode, mload, tolerance, stability, lemp, utemp, vad, pdf, price from crystals where part_number='$query'"; 
			$stmt_h = $dsn->prepare( $sqlstmt ) or print "$DBI::errstr<br>\n"; 
			$stmt_h->execute() or print "$DBI::errstr<br>\n";
			while( my($pn, $fa, $cu, $mo, $ml, $to, $st, $lt, $ut, $va, $pd, $pr) = $stmt_h->fetchrow() ){
				Tokenize( 'PN', $pn ); Tokenize( 'FA', $fa ); Tokenize( 'CU', $cu ); 
				Tokenize( 'MO', $mo ); Tokenize( 'ML', $ml ); Tokenize( 'TO', $to );
				Tokenize( 'ST', $st ); Tokenize( 'LT', $lt ); Tokenize( 'UT', $ut );
				Tokenize( 'VA', $va ); Tokenize( 'PD', $pd ); Tokenize( 'PR', $pr );
	
				Parse( "CRYSTAL_RESULT_ROW" ); 
			}
			$stmt_h->finish();
		} elsif( $table eq "oscillators" ){
			my $sqlstmt = "select partnumber, supply_voltage, output_logic, symmetry, stability, ltemp, utemp, description, pdf from oscillators where partnumber='$query'"; 
			$stmt_h = $dsn->prepare( $sqlstmt ) or print "$DBI::errstr<br>\n";
			$stmt_h->execute() or print "$DBI::errstr<br>\n"; 
			while( my($pn, $su, $ou, $sy, $st, $lt, $ut, $de, $pd ) = $stmt_h->fetchrow() ){
				Tokenize( 'PN', $pn ); Tokenize( 'SU', $su ); Tokenize( 'OU', $ou );
				Tokenize( 'SY', $sy ); Tokenize( 'ST', $st ); Tokenize( 'LT', $lt );
				Tokenize( 'UT', $ut ); Tokenize( 'DE', $de ); Tokenize( 'PD', $pd );

				Parse( "OSCILLATOR_RESULT_ROW" );
			}
			$stmt_h->finish();
		} elsif( $table eq "tcxos" ){
			my $sqlstmt = "select part_number, supply_voltage, logic, symmetry, stability, ltemp, utemp, fam, pckg_info, freq_control, pdf from tcxos where part_number = '$query'"; 
			$stmt_h = $dsn->prepare( $sqlstmt ) or print "$DBI::errstr<br>\n"; 
			$stmt_h->execute() or print "$DBI::errstr<br>\n";
			while( my( $pn, $su, $lo, $sy, $st, $lt, $ut, $fa, $pc, $fr, $pd ) = $stmt_h->fetchrow() ){
				Tokenize( 'PN', $pn ); Tokenize( 'SU', $su ); Tokenize( 'LO', $lo );
				Tokenize( 'SY', $sy ); Tokenize( 'ST', $st ); Tokenize( 'LT', $lt );
				Tokenize( 'UT', $ut ); Tokenize( 'FA', $fa ); Tokenize( 'PC', $pc );
				Tokenize( 'FR', $fr ); Tokenize( 'PD', $pd );

				Parse( "TCXO_RESULT_ROW" );
			}
			$stmt_h->finish();
		} elsif( $table eq "vcxos" ){
			my $sqlstmt = "select part_number, supply_voltage, logic, symmetry, stability, ltemp, utemp, fam, pull, pckg_info, freq_control, pdf from vcxos where part_number='$query'"; 
			$stmt_h = $dsn->prepare( $sqlstmt ) or print "$DBI::errstr<br>\n"; 
			$stmt_h->execute() or print "$DBI::errstr<br>\n";
			while( my( $pn, $su, $lo, $sy, $st, $lt, $ut, $fa, $pu, $pc, $fr, $pd ) = $stmt_h->fetchrow() ){
				Tokenize( 'PN', $pn ); Tokenize( 'SU', $su ); Tokenize( 'LO', $lo );
				Tokenize( 'SY', $sy ); Tokenize( 'ST', $st ); Tokenize( 'LT', $lt );
				Tokenize( 'UT', $ut ); Tokenize( 'FA', $fa ); Tokenize( 'PC', $pc );
				Tokenize( 'FR', $fr ); Tokenize( 'PD', $pd ); Tokenize( 'PU', $pu );

				Parse( "VCXO_RESULT_ROW" );
			}
			$stmt_h->finish();
		} elsif( $table eq "ocxos" ){
			my $sqlstmt = "select part_number, supply_voltage, logic, stability, ltemp, utemp, fam, pckg_info, freq_control, pdf from ocxos where part_number='$query'"; 
			$stmt_h = $dsn->prepare( $sqlstmt ) or print "$DBI::errstr<br>\n"; 
			$stmt_h->execute() or print "$DBI::errstr<br>\n";
			while( my( $pn, $su, $lo, $st, $lt, $ut, $fa, $pc, $fr, $pd ) = $stmt_h->fetchrow() ){
				Tokenize( 'PN', $pn ); Tokenize( 'SU', $su ); Tokenize( 'LO', $lo );
				Tokenize( 'ST', $st ); Tokenize( 'LT', $lt ); Tokenize( 'PD', $pd );
				Tokenize( 'UT', $ut ); Tokenize( 'FA', $fa ); Tokenize( 'PC', $pc );
				Tokenize( 'FR', $fr ); 

				Parse( "OCXO_RESULT_ROW" );
			}
			$stmt_h->finish();
		}
	}

	Parse( "FOOTER" );

}

$dsn->disconnect();

Output();
exit( 0 );
