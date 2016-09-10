#!/usr/bin/perl
# pixbkup v.0.1.1 by C.J. Steele <csteele@forwardsteptech.com>
#       created: 28 Jul 2003
# (C)opyright 2003-2004, C.J. Steele, all rights reserved.
#
# This script uses `telnet` and the perl module 'Expect', to telnet in to
# the specified PIX devices and log the results of the `wr t` command to 
# a log file which is generated on-the-fly.
# 
# The resulting 'log' file needs to be slightly altered prior to attempting
# to import the config in to a running PIX, and great care should be taken
# before attempting to do so.  Anyone remotely familiar with PIX 
# configurations should have no problem altering the 'log' file to a point 
# that is is useable on a running PIX.
# 
# This script should be setup to run via cron on a nightly basis, with both
# stdout and stderr being redirected to /dev/null so password hashes aren't
# transmitted/stored via e-mail.
#
# TODO/ROADMAP
# - support different passwords on different devices. (v.0.2.0)
# - improve error checking during logfile creation (v.0.2.0)
#
use strict;
use Expect;
 
my @hosts = ( "firewall1", "firewall2" ); 
my $pix_tel_pass = "pass"; 
my $pix_ena_pass = "enpass"; 
my $logroot = "/var/bkup/"; 
my $minto = 0;
my $maxto = 7;

foreach my $pix ( @hosts ) 
{
        my $logfile = nameLogFile( $pix ); 
        if( $logfile )
        {
                my $proc = Expect->spawn("telnet $pix");
                $proc->expect($maxto,'-re',"assword:");
                $proc->send_slow($minto,"$pix_tel_pass\r");
                $proc->expect($maxto,'-re',">");
                $proc->send_slow($minto,"en\r");
                $proc->expect($maxto,'-re',"assword:");
                $proc->send_slow($minto,"$pix_ena_pass\r");
                $proc->expect($maxto,'-re',"#");
                $proc->send_slow($minto,"no page\r" ); 

                $proc->log_file( "$logfile", "w" );
                $proc->send_slow($minto,"wr t\r" ); 
                #$proc->expect($maxto, "[OK]" );
                $proc->log_file( undef );

                $proc->send_slow($minto,"page 24\r" ); 
                $proc->send_slow($minto,"exit\r");
        }
}


sub nameLogFile
{

        my $hostname = shift; 
        my ( $day, $mon, $year ) = (gmtime( time() ))[3,4,5];
                $mon++; $mon=sprintf( "%02d", $mon ); $year+=1900;

        my $logfile; 

        eval {
                $logfile = "$logroot$hostname/$year" . "_$mon" . "_$day"; 
                if( -d "$logroot/$hostname" )
                {
                        system( "touch $logfile" );
                } else {
                        system( "mkdir $logroot/$hostname" );
                        system( "touch $logfile" );
                }
        }; return -1 if( $@ );

        return $logfile; 
}
