# filename: Catreq.pl
# (C)opyright 2000, M-tron Industries, Inc., all rights reserved.
#	written by Corey J. Steele <csteele@mtron.com>
# last modified: 12/12/2000
#
# Description: this file holds the variables that may change in the
#	catreq.cgi script.  You should not need to change the catreq.cgi
#	script to change simple things about how it works, that should
#	all be done here.

#
# $reql_referer is the location of the catform.htm page... this has to be set
# to the location of where the form will be submitted from, or the catreq.cgi 
# script will refuse to run.
$main::real_referer = "http://argo.mtron.com/~csteele/catform.html";

#
# @catreq_recipients is the array of e-mail addresses that will recieve the 
# email notification of submitted catalog requests.  Please be absolutely 
# certain that you escape the '@' symbol in the address, or perl will crap.
@main::catreq_recipients = ( "csteele\@mtron.com" );
