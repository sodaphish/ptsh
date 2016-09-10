#!/usr/bin/perl

main {

  my $line_count = 0;

  open( IN, $ARGV[0] ) or die "usage: pdoc.pl filename\n\n";

  print "<html><head><title>$ARGV[0]</title></head><body>\n\n"; 

    while( $line = <IN> ){
      if( $line =~ /^\#/ ){
        $line =~ s/^\#//;
        #print "$line_count: $line"; 
        my( $cmd, @contents ) = split( /\s/, $line );
        #chomp( @contents );
        if( $cmd =~ /^\// ){
          #indent x notches, where x is the number of slashes
          my $level = 1; 
          if( length( $cmd ) > 1 ){ chop( $cmd ); }
          while( $cmd ){
            print "<blockquote>"; 
            chop( $cmd );
            $level++;
          }
          print "<h$level>", @contents, "</h$level>";
          print "\n\n";

        } elsif( $cmd =~ /^\>/ ){
          #tab in x times where x is the number of greater than signs
          while( $cmd ){ 
            print "&nbsp;&nbsp;&nbsp;&nbsp;";
            chop( $cmd ); 
          }
          print "$_ " foreach( @contents ); 
          print "<br>\n\n"; 

        } elsif( $cmd =~ /^\\/ ){
          #un-indent x notches, where x is the number of back slashes
          if( length( $cmd ) > 1 ){ chop( $cmd ); }
          while( $cmd ){
            print "</blockquote>";
            chop( $cmd );
          }

        } elsif( $cmd =~ /^\|/ ){
          #echo this html command
          print @contents, "\n";

        } else {
          print "$_ " foreach( @contents );
          print "<br>\n";

        } #end if
      } else {
        #it's not a special line
      } #end if

      $line_count++;

    } #end while 

  print "</body></html>"; 

  close( IN );

}


exit( 0 );

=head1 NAME

pdoc.pl - convert ignus-style comments to HTML

=head1 SYNOPSIS

B<pdoc.pl> [file] 

=head1 DESCRIPTION

This simple script converts ignus's internal coding style into a man page-like HTML document.  Use a shell re-direct to capture the output to a file. 

=head1 USAGE

Insert any of the macros defined below, in your perl source code, and you can then generate HTML based documentation for the code with B<pdoc.pl>.  There are three types of commands (presently): block-level indention commands, non-block-level indention commands, and raw HTML inserts.  

Block-level indention commands work in pairs, similar to HTML tags (i.e. B<#//> requires a corresponding B<#\\>) to format block headings. Block headings are bold-faced, and generally of a larger size font. 

Non-block-level indention commands do not work in pairs, and do not do any special formatting.

=over 5

The following are indention commands:
 

=item B<#/>I<//...> - begins a heading B<x> levels deep, where B<x> is the number of /'s in the command.  B<#//> creates a heading two blocks deep.

=item B<#\>I<\\...> - is the antithesis of B<#/>, and brings the level of indention back a level for ever \ present in the command. 

=item B<#E<gt>>I<E<gt>E<gt>...> - indents four spaces per E<gt> in the command. note that #E<gt> does B<NOT> require any closing command to return to the start of the block. 

=item B<#! HTML> - permits you to insert arbitrary HTML into the output stream.  This is not a necessary feature, but may be nice to have.

=back

Start programs with B<#/ filename>, and end them with B<#\ filename>. For each function define a B<#// functionName()> before the beginning of the function, and a B<#\\ functionName() just before the start of the actual line I<sub functionName()>.  Each section the function gets a B<#/// DEFINITIONS:> (for example), and that section needs to be closed with a B<#\\\ DEFINITIONS:>.  Though the section/function/block name is not important in the closing block-level indention, it helps to understand why that particular command is there.

=head1 AUTHOR

Corey J. Steele E<lt>csteele@ignus.comE<gt>

(C)opyright 1999, Corey J. Steele, all rights reserved.

