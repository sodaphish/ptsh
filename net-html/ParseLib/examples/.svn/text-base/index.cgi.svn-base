#!/usr/bin/perl
print "Content-type: text/html", "\n\n";

use ParseLib;
use CGI param;

LoadTemplate( "layout.tmpl" );

Tokenize( "DOUG_QUOTE", "Hello world!" );
Sectionize( "HEADER", Parse( "HEADER" ) ); 
# because Parse() pushes the contents of something onto the output buffer, you need to
# be aware that this pushes the parse'd contents of the section "HEADER" into the
# section variable "HEADER"... this is probably a horrible example, but it shows
# some of the odd flexibility

Parse( "BODY" "FOOTER" );
Output();

exit( 0 );
