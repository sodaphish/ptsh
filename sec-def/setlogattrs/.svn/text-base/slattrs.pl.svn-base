#!/usr/bin/perl
# slattrs.pl v0.1.0 by C.J. Steele, CISSP, <coreyjsteele@yahoo.com>
#
# This program monitors directories (via FAM) and sets attribute bits on files
# created in those directories so the files are append-only.  This is used,
# almost exclusively, to secure log servers so that the logs are append-only
# and cannot be edited by rouge users, hackers, or unscrupulus sysadmins (who
# might be covering their butts on something dumb they did.)
#
# You can configure which directories are monitored by mangling the
# %monitor_these hash, which is in the format of "'directory' => 'flag'" where
# "directory" is the full path you want to monitor and "flag" is either "r" or
# "n", meaning recursive or not.  Subdirectories of recursively monitored
# directories will be monitored as opposed to non-recursive directories which
# will NOT monitor subdirectories.  You can also specify which files you do NOT
# want to be included in the monitoring (there are some files which need to be
# excluded, such as your Xorg.0.log files) or functionality is broken.
# 
# You can also tune where the pidfile is dropped to suit local environments.
#
# For `slattrs.pl` to run, You'll have to have FAM (and thus portmapper)
# running on the machine to be monitored.  These need to be setup with due care
# to ensure they can not be accessed from beyond the local machine.
#
# TODO:
# * catch sigint so we can die-out properly and kill off our pidfile and
# 	cleanup other things.
#
use strict;
use SGI::FAM; 
use Filesys::Ext2 qw( lsattr chattr ); 
use Shell qw( find ); 
use English;

my %monitor_these = (
	"/var/log/hosts" => "r", 
	"/var/log" => "n" 
	);	
my @exceptions = ( "/var/log/Xorg.0.log", "/var/log/Xorg.0.log.old" );
my $pidfile = "/tmp/slattrs.pid";




########################################################################
#        DO NOT EDIT ANYTHING BELOW THIS POINT UNLESS YOU REALLY       #
#                KNOW WHAT YOU'RE DOING AND ACTUALLY DO                #
########################################################################


# my debug symbols will not be particularly useful to discern additional
# functionality, so don't enable this unless you're making changes and you want
# to follow my debug convention.
my $DEBUG = 0;


# we have to be root to use this... if you stopped using Filesys::Ext2, and did
# system calls to `chattr`, you could setuid the binaries and get rid of
# needing root, but that'd be an epically crappy idea, so don't.
if( $UID != 0 )
{
	print "E: you must be root!\n";
	exit( 1 );
}

# check to see if other instances of this script are running and die if they
# are. 
justme();

# sorta demonizing... I you still need to `nohup` the process or it dies with
# your tty.  This is all handled through the slattrs.init script, for simplicity
fork && exit; 

print "...dropping to the background. (pid $$)\n";

open( PIDFILE, ">$pidfile" ) or die( "E: couldn't open $pidfile" );
print "D: writing pidfile\n" if( $DEBUG );
print PIDFILE "$$\n";
close( PIDFILE );


# 
# load up the directories we want to monitor -- these can be recursive or not.
# See the bits of documentation up by %monitor_these for more
my $fam=new SGI::FAM;
foreach my $dir ( keys %monitor_these )
{
	if( -r $dir and -d $dir )
	{
		# its a directory and its readable...
		if( $monitor_these{$dir} =~ /^r/i )
		{
			#this is a recursive directory, load its subdirectories
			foreach my $sd ( find( "/var/log/hosts", "-type d", "-print" ) )
			{
				chomp( $sd );
				if( -r $sd and -d $sd )
				{
					$fam->monitor( "$sd" );
					print "D: FAM monitor setup on '$sd'\n" if( $DEBUG );
				} else {
					# not sure how we'd ever get here given we need to run as root 
					# and the other checks that occur, but better safe than sorry.
					print "E: cannot read $dir or it is not a directory\n";
				} #end if
			} #end foreach 
		} else {
			# not a recursive loading directory, ignore sub directories.
			$fam->monitor( $dir );
		}
	} else {
		print "E: cannot read $dir or it is not a directory\n";
	} #endif
} #end foreach


#
# This is where we do the actual monitoring... the only bit thats slightly
# confusing, frankly, is the $fam->which( $fe) bit that produces the
# non-terminated directory name the event occurred in.
while( 1 ) 
{
	# this should be a little less blocking... not that it matters particularly.
	if( $fam->pending )
	{
		my $fe = $fam->next_event; 
		if( $fe->type eq "create" )
		{
			my $file = $fam->which( $fe ) . "/" . $fe->filename; 
			if( -f $file and ! isin( $file, @exceptions ) )
			{
				# we only want to be trying to chattr /files/ that are created
				print "D: file=$file\n" if( $DEBUG );
				print "D: 'create' event detected on $file\n" if( $DEBUG );
				eval {
					print "D: lsattr before ", lsattr( ($file) ), "\n" if( $DEBUG );
					chattr( "+a", ($file) ); 
					print "D: lsattr after ", lsattr( ($file) ), "\n" if( $DEBUG );
				}; if( $@ ){
					print STDERR "E: couldn't chattr() ", $fe->filename, " ($@)\n";
				} #end if
			} #end if
		} #end if
	} else {
		#this may need to be tuned
		sleep 1;
	} #endif
} #	end while

	
exit( 0 );




sub justme
# checks to see if our pidfile exists (is open()-able) and if so, gets the pid
# and kills it with signal zero to see if its there, if it isn't, we return
# (and thus we continue processing.)
{
	if( open( PIDFILE, $pidfile ) )
	{
		my $pid; chop( $pid = <PIDFILE> );
		kill( 0, $pid ) and die "$0 already running (pid $pid).";
	}
} #end justme()




sub isin
# checks an array (@a) for the occurence of a specific element ($e) and returns
# a 1 (true) or 0 (false)
{
	my( $e, @a ) = @_;
	foreach( @a )
	{
		return 1 if( $_ eq $e );
	}
	return 0;
} #end isin()
