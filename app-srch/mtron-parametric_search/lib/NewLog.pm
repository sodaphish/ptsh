# filename: NewLog.pm
#  (C)opyright 2000, M-tron Industries, Inc., all rights reserved.
#  written by Corey J. Steele <csteele@mtron.com>
#
#  last modified: 12/12/2000
#
#  ROUTINE TRANSLATIONS:
#  01 -> initial query
#  02 -> dead-end search in Crystals
#  03 -> dead-end search in Oscillators
#  04 -> dead-end search in OCXOs
#  05 -> dead-end search in VCXOs
#  06 -> dead-end search in the OCXOs
#  07 -> dead-end 'contact me' form results
#  08 -> problems with the DSN in a CrystalsSearch.pm function.
#  09 -> problems with the DSN in a OscillatrsSearch.pm function.
#  0A -> problems with the DSN in a TCXOsSearch.pm function.
#  0B -> problems with the DSN in a VCXOsSearch.pm function.
#  0C -> problems with the DSN in an OCXOsSearch.pm function.
#  0D -> feedback form log entries
#
#
# Description: this package handles logging the transactions reported to it 
#	by the other modules.  This used to write to a database, but as of
#	the December 2000 re-write we have changed it over to writing to a 
#	log file instead.
package NewLog;




BEGIN {
	require Exporter;
	@EXPORT = qw( &NewLog );
	@EXPORT_OK = qw();

	@ISA = qw( Exporter );
	use lib qw( ../cfg );
	require "ParametricSearch.pl";
}



sub NewLog {

	my( $level, $routine, @message ) = @_;
	my $time = time();

	#
	# make @message into one constant string, $entry
	my $entry;
	foreach( @message ){ $entry .= $_; }

	$entry = NukeApostrophy( $entry );

	open( OUT, ">>$log_file" ) or die "Could not open log file! ($!)"; 
	print OUT $time, "\t", $host, "\t", $level, "\t", $routine, "\t", $entry, "\n";
	close( OUT );

} #end Log()



sub NukeApostrophy {

	$inboundMessage = @_; 
	$inboundMessage =~ s/\'/\`/gi; 

	return $inboundMessage;

}



1;
