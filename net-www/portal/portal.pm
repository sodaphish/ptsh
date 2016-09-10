#!/usr/bin/perl
#
# (C)opyright 2000, Corey J. Steele, all rights reserved.
#
# TODO:
#   - should functions return values or set Tokens?  
#
package portal;


$version    = "5.0.0";
$base = "/home/csteele/www/portal/journal"; 


#
# MakeEntry() - add an entry to the specified journal
#   ex.   MakeEntry( "$base/april-2000.jrnl", $entry_text );
#   where $entry_text is the text that is to be added.
sub MakeEntry {
	my( $file, @entry ) = @_;
	$entry .= " $_" foreach( @entry );
	$long_date = `date`; chomp( $long_date );
	if( -x $file and -w $file ){
		open( INF, ">$file" ); 
			print INF "-----\n$long_date\n$entry\n"; 
		close( INF );
		return;
	} elsif( -x $file ) {
		die "MakeEntry() - Could not write to $file. ($!)"; 
	} else {
		die "MakeEntry() - General error opening $file for write. ($!)"; 
	}
} #end MakeEntry()




#
# GetEntry() - returns a scalar variable with the contents of
# a specific journal entry (the contents of the whole file)
sub GetEntry {
	my( $file ) = @_;
	my $return_results = "";
	if( -r $file ){
		open( INF, $file );
			while( my( $line ) = <INF> ){
				$return_results .= " $line"; 
			}
		close( INF );
		return $return_results;
	} else {
		return -1; 
		#die "GetEntry() - Error opening journal for read: $!"; 
	}
} #end GetEntry()




#
# GetListOfEntries() - return an array of journal entries (files) that
# exist in the $base directory.
sub GetListOfEntries {
	my $entries = `ls $base/*.jrnl`;
	@return_results = ();
	foreach( split(/ /, $entries ){
		push( @return_results, $_ );
	}
	return @return_results;
} #end GetListOfEntries()




#
# FindMatches() - finds the matches of a query and returns an 
# array of scalar values with the specific entries found matching
sub FindMatches {

} #end FindMatches()




# 
# Login() - authenticate the user.  right now, this will be a joke
# eventually, we'll make this a session-based thing... I hope.
sub Login {
	if( $login eq "csteele" and $password eq "cpe1704tks" ){
		return 1;
	} else {
		return 0;
	}
} #end Login()




#
# CurrentJournal - returns the file name of the 'current' journal
# file; i.e. $base/$month-$year.jrnl
sub CurrentJournal {

} #end CurrentJournal


1;
