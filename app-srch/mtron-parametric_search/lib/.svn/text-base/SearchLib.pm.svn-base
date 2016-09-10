# filename: SearchLib.pm
# (C)opyright 1999-2000, M-tron Industries, Inc., all rights reserved.
# 	written by Corey J. Steele <csteele@mtron.com>
# last modified: 12/12/2000
#
package SearchLib;
 
BEGIN {
	require Exporter;
	@EXPORT = qw( &LogDeadEnd &SetRanges &PrevNext &IsIn &FormatDropList &WindowMatches &ExpandFrequency &SortList &DropZeros );
	@ISA = qw( Exporter );

	use CGI;
	use NewLog;
	use Env;
	use ParseLib;
}



sub LogDeadEnd {

	#
	# pull in the routine that we're logging to 
	my( $routine ) = @_;

	#
	# we need to put $main::httpHeaders into the proper form
	foreach $valuePair ( split(/}/, $main::httpHeaders ) ){
		my( $key, $val ) = split( / = /, $valuePair );
		$log_entry .= "}$key=$val" if( $log_entry ne "" );
		$log_entry = "$key=$val" if( $log_entry eq "" );
	}

	NewLog( 'inf', "$routine", "$log_entry" );

} #end LogDeadEnd()




sub SetRanges {

	my( $NumOfMatches, $initialHere ) = @_;

	Tokenize( 'TOTAL_MATCHES', $NumOfMatches );

	Tokenize( 'LOW_RANGE', 1 );
	if( $main::__here - $main::__maxNumView >= 0 and $main::__here < $NumOfMatches ){
		Tokenize( 'LOW_RANGE', $main::__here - $main::__maxNumView + 1 );
	} elsif( $main::__here >= $NumOfMatches ){ 
		Tokenize( 'LOW_RANGE', $initialHere + 1 ); 
	}

	Tokenize( 'HIGH_RANGE', $main::__here );
	if( $main::__here <= 0 ){
		Tokenize( 'HIGH_RANGE', $main::__here + $main::__maxNumView );
	}

} #end SetRanges() 




sub PrevNext {

	my( $frame, $end ) = @_;
	
	if( $main::__here - $main::__maxNumView < 0 and $main::__here < $main::__maxNumView ){
	
		#
		# the results will all fit in one screen-full, no need to display prev or next.
	
	} elsif( $frame >= $end ){

		#
		# we're at the end, lets give them a previous button
		$main::__here -= ( 2* $main::__maxNumView );
		Tokenize( 'HERE', $main::__here );
		Parse( "PREVIOUS" );

	} elsif( $main::__here - $main::__maxNumView <= 0 ){
		
		#
		# we've got more results to view, lets show the next button
		Tokenize( 'HERE', $main::__here );
		Parse( "NEXT" );

	} else {
	
		#
		# we're somewhere in the middle of the search output, so we need both prev & next
		$prev = $main::__here - ( 2 * $main::__maxNumView );
		if( $prev < 0 ){ $prev = 0 };
		Tokenize( 'HERE', $main::__here );
		Tokenize( 'PREV', $prev );
		Parse( "PREVIOUS", "NEXT" );
	}

} #end PrevNext()




sub IsIn {

	my( $value, @list ) = @_;
	
	foreach( @list ){
		return 1 if( $value eq $_ );
	}

	return 0;

} #end IsIn()




sub FormatDropList {

	my ($variable, @list) = @_; 
	my $tmpContainer = "";

	#
	# need to sort the list before we form it
	@list = SortList( @list );

	foreach( @list ){
		$tmpContainer .= "<option value=\"$_\">$_"; 
	}

	if( $variable eq "" ){
	  $tmpContainer = "<option value=\"\">ALL" . $tmpContainer; 
	} else {
	  $tmpContainer = "<option value=\"$variable\">$variable<option value=>ALL"; 
	}

} #end FormatDropList()




sub WindowMatches {

	my( $frame, @inList ) = @_;

	my $count = 0;
	my @winMatches = ();

	foreach( @inList ){

		if( $count >= $main::__here and $count < $frame ){
			
			push( @winMatches, $_ );
			$main::__here++;

		}
		$count++;
	}

	return @winMatches;

} #end WindowMatches()




sub ExpandFrequency {

	my( $frequency ) = shift;
	if( $frequency =~ m/[^0-9.]/g or $frequency <= 0 ){
		return undef;
	} else {
		return sprintf( "%8.6f", $frequency );
	}

} #end ExpandFrequency()




sub SortList {

	my @inList = @_;
	my @new_list = ();

	foreach( sort { $a <=> $b } @inList ){
		push( @new_list, $_ );
	}

	return @new_list;

} #end SortList()




sub DropZeros {

	my( $inBound ) = @_;
	$inBound =~ s/0*$//;

	if( $inBound =~ /\.$/ ){
		$inBound .= "0";
	}

	return $inBound;

} #end DropZeros()



1; #end of package SearchLib
