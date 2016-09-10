#!/usr/bin/perl
use strict;
use LWP::Simple;
use POSIX qw( strftime );
use Net::SMTP;

my $smtp = Net::SMTP->new( 'localhost' );
my $datestring = strftime( "%Y-%m-%d", localtime );
my $content = get( "http://sodaphish.com/wc/whybanned2.php" );

my $bans = "";
foreach( split( /\n/, $content ) )
{
	$bans .= "$_\n" if( $_ =~ $datestring );
}

$smtp->mail( 'hostedby@hostedbycorey.com' );
$smtp->to( 'sodaphish@gmail.com' );
$smtp->data();
$smtp->datasend( 'To: sodaphish@gmail.com' );
$smtp->datasend( "\n" );
$smtp->datasend( "The following is a list of bans entered today:\n" );
$smtp->datasend( "$bans" );
$smtp->datasend( "\n\n" );
$smtp->datasend( "(This is an automated message.)" );
$smtp->dataend();

$smtp->quit;


exit( 0 );
