#!/usr/bin/perl
use strict;
use IO::Socket;
use LWP::UserAgent;

###############################
# TinyURL script by C.Davies
# (c.davies@cdavies.org)
# A script to tinyurlise urls
# Usage:
# /tinyurl <url>
# Version 0.1 (06/02/2003)
#	*Created tinyurl script
# Version 0.2 (06/02/2003)
#	*Efficiency improvements
#
# Licensed under the GPL.
# Disclaimer at bottom,
# Full text in tar.
#
# Modified for irssi by Tom Gilbert, 06/02/2003.

use vars qw($VERSION %IRSSI);

use Irssi qw(command_bind active_win);
$VERSION = '1.2';
%IRSSI = (
    authors	=> 'giblet',
    contact	=> 'tom@linuxbrit.co.uk',
    name	=> 'tinyurl',
    description	=> 'create a tinyurl from a long one',
    license	=> 'GPL',
    url		=> 'http://linuxbrit.co.uk/',
    changed	=> 'Fri Feb  7 12:29:07 GMT 2003',
);

command_bind(
    tinyurl => sub {
      my ($msg, $server, $witem) = @_;
      my $answer = tinyurl($msg);
      if ($answer) {
        print CLIENTCRAP "tinyurl got: $answer";
        if ($witem && ($witem->{type} eq 'CHANNEL' || $witem->{type} eq 'QUERY')) {
  	      $witem->command("MSG " . $witem->{name} ." ". $answer);
        }
      }
    }
);

sub tinyurl {
	my $url = shift;
  my $ua = LWP::UserAgent->new;
  $ua->agent("tinyurl for irssi/1.1 ");
  my $req = HTTP::Request->new(POST => 'http://tinyurl.com/create.php');
  $req->content_type('application/x-www-form-urlencoded');
  $req->content("url=$url");
  my $res = $ua->request($req);

  if ($res->is_success) {
	  return get_tiny_url($res->content);
  } else {
    print CLIENTCRAP "ERROR: tinyurl: couldn't connect to remote host";
		return "";
	}
}

#get_tiny_url: Pass some HTML, get back the tinyurl contained therein.

sub get_tiny_url($) {
	
	my $tiny_url_body = shift;
	$tiny_url_body =~ /(.*)(tinyurl\svalue=\")(.*)(\")(.*)/;

	return $3;
}

######################################################################
#tinyurl script - X-chat script that makes tinyurls from big ones
#Copyright (C) 2003  C.Davies
#
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

