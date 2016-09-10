#!/usr/bin/perl
use LWP::Simple;

# httpget.pl v0.3.1 - by Corey J. Steele
# (C)opyright 1999, Corey J. Steele, all rights reserved.
# 
# This program is distributed under the GNU Public License (GPL),
# for specific information regarding the GPL, please refer to 
# the file "COPYING", or http://www.gnu.org
#
# This is REAL simple:
#   o  create and add() entry for each site you want to retrieve
#      add( "http://site.to.add/file-from-site.txt", "file-to-put-in.txt" )
#      You can get ANY kind of file (as it is interpreted by the web server 
#      on the other end), and put it into your own file (this works for binary
#      as well as ASCII files
#   o  set the $base_directory variable to wherever you want to dump the files
#      that we're getting
#   o  run the script.
#
# If you have problems (i.e. it doesn't work): 
#   o  make sure the execute bit is set for the your state of the file (i.e. if
#      you are the owner of the file, then make sure that the owner exec bit is
#      set... if I'm speaking Greek to you, try `man chmod`.)
#   o  check to see that the perl mod LWP::Simple is installed (do this by
#      typing `perl -e "use LWP::Simple"` at the command line (minus the
#      outside set of quotes); if that errors, you don't, get it.
#   o  check to see that $base_directory exists (try to do an `ls` of it),
#      if it doesn't exist, make it (`mkdir`).
#   o  see that perl is actually where I'm expecting it to be (look at the 
#      first line of this file (#!/usr/bin/perl), if perl is somewhere else
#      on your system, tell me where, there (i.e. change #!/usr/bin/perl to 
#      the path of your perl install.)
#
# NOTE: if you setup httpget.pl to automatically retrieve files from sites you
# do not own or administer, please adhere to local regulations of those sites
# regarding the frequency with which you download those files.  (i.e. Slashdot
# requests a fifteen minute gap between retrievals).
# 
# If all else fails (really!), then feel free to e-mail me at:
#      csteele@old.dhs.org, or hit me on ICQ: 1151157
#

$VERBOSE = 0;
$SILENT = 0; 
$ERROR = 0; 
foreach( @ARGV ) {
	if( $_ eq "--verbose" || $_ eq "-V" ) {
		$VERBOSE = 1; 
	}
	# verbose over-rides silent mode.
	# silent mode only shuts off error messages
	if( ( $_ eq "--silent" || $_ eq "-S" ) && $VERBOSE != 1 ) {
		$SILENT = 1; 
	}
}


@URLS = ();
$base_directory = "./";

# freshmeat's current headlines
add( "http://core.freshmeat.net/backend/recentnews.txt", "freshmeat.txt" );
# slashdot's current stories
add( "http://slashdot.org/ultramode.txt", "slashdot.txt" );
# linuxtoday's headlines
add( "http://linuxtoday.com/lthead.txt", "linuxtoday.txt" );
# an immage from the wather channel that tells me my local weather conditions.
add( "http://autocobrand.weather.com/autocobrand/weather_magnet/SD_Vermillion.gif", "current_report.gif" );
# a regional sattelite image a la the weather channel.
add( "http://image.weather.com/images/sat/regions/n_central_sat_450x284.gif", "regional_sattelite.gif" );
# more weather stuff from the weather channel.
add( "http://image.weather.com/images/radar/regions/n_central_rad_450x284.gif", "regional_radar.gif" );
# dito.
add( "http://image.weather.com/images/radar/single_site/042loc_450x284.gif", "yankton_radar.gif" );

foreach ( keys %sites ) {
    @page = get( $_ );
    if ( defined @page ) { write_file( $sites{$_}, @page ); }
    else { print "Error getting ", $_, "!\n" if( $SILENT == 0 ); }
}

print "httpget.pl ending run...\n" if( $VERBOSE == 1 ); 

exit( 0 );



#
# write_file() 
#  gets the file from the remote location, and writes it to the local location
sub write_file {
    my ($file, @page) = @_; 
    open (IF, ">$file") or $ERROR++;
	  # that > was a >=, but that wrought great havok!
	  print "Error opening $file for writting: $!...\n" if( $ERROR > 0);
	print "writting to $file...\n" if( $VERBOSE == 1 ); 
    print IF @page; 
    close (IF);
    return;
} #end write_file()



#
# add()
#  adds a url/file combination to the list of files to retrieve
sub add {
  my( $link, $file ) = @_;
  $file = $base_directory . $file;
  # support for verbose output...
  print "added: $link, $file\n" if( $VERBOSE == 1 ); 
  $sites{$link} = $file;
} #end add()
