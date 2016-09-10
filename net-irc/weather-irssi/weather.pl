#
# weather v0.0.0
# (C)opyright 2003, C.J. Steele, all rights reserved.
# 
# usage: 
# !weather [stationid]
#	outputs current weather conditions for the default station to the 
#	active window
#
# /weather [-o] [stationid]
#	-o: 		results in the forecast being output to the active windo
#	stationid:	specifies a station id other than the default.
#
# /weather_ssearch <city>, <state>
#	searches for the station id for the <city> and <state> specified.
#	-- only provides results for the U.S.
#
use strict;
use Geo::METAR;
use LWP::Simple;
use vars qw( $VERSION %IRSSI );

use Irssi qw( signal_add_last settings_add_bool settings_add_str 
				settings_get_bool settings_get_str );

$VERSION = '0.0.0'; 
%IRSSI = ( 
	authors => 'SodaPhish',
	contact => 'sodaphish@securitylounge.com',
	name => 'weather',
	description => 'provides up-to-date weather for specified locations',
	license => 'BSD-style',
	url => '', 
	changed => 'Nov 17 2003 14:15Z-0600'
);

# the default station id... 
my $stationid = "KFSD"; 

sub forecast 
{
    my ($server, $data, $nick, $address, $target ) = @_;
	my $channel = Irssi::active_win()->get_active_name();
	if( $data =~ /^!weather/i )
	{
		$data =~ s/!weather//i; 
		chomp( $data ); 
		my @args = split( /\ /, $data );

		if( scalar( @args ) > 1 )
		{
			#i.e. '-o KFSD'
			$stationid = $args[1]; 
		} elsif( scalar( @args ) == 1 ){
			#i.e. 'KFSD'
			$stationid = $args[0]; 
		} #else {
			#$stationid = $stationid;
		#}

		my $metar_source = "http://weather.noaa.gov/cgi-bin/mgetmetar.pl?cccc=$stationid";
		my $m = new Geo::METAR;
		my $metardata = get( $metar_source ); 
		$m->metar( "$metardata" );
		my $temp = $m->TEMP_F + 20 . "F";
		my $wind = $m->WIND_MPH . "mph";
		my $windir = $m->WIND_DIR_ENG;
		my $sky = $m->SKY; 

		print "temp: $temp, wind: $windir/$wind, sky: ${@$sky}[0]\n"; 
	}
}

sub stationsearch
{

}



Irssi::signal_add_last( 'message public', 'msghandlr' );
#Irssi::command_bind( 'setbsr', 'setbsr' );

print CRAP "%B>>%n ".$IRSSI{name}." v".$VERSION." loaded...";

