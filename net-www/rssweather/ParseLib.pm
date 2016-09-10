#
# ParseLib.pm v1.2.2 by Corey J. Steele <coreyjsteele@yahoo.com>
#
# (C)opyright 1999-2000, Corey J. Steele, all rights reserved.
#   This source code, and all of the files originally packaged with
#   it, are subject to the terms of the General Public License, as
#   outlined in the file COPYING.  
#
package ParseLib;

BEGIN {
  require Exporter;
  @EXPORT = qw( &LoadTemplate &Parse &Output &Tokenize &Sectionize &AppendOut 
                %__Sections %__Tokens );
  @ISA = qw( Exporter );
}

%__Sections = {};
%__Tokens = {};
$__section = "__GARBAGE"; 



#
# LoadTemplate() - loads the templates of the listed file(s) 
# into memory.
sub LoadTemplate {
  my( @files ) = @_;
  foreach( @files ) {
    open( TMPL, $_ ) or die "$!"; 
      ParseSections(); 
    close( TMPL );
  }
} # end loadTemplate()



#
# ParseSections() - parses the sections of a file and puts them
# in the appropriate hashes
sub ParseSections {
  while( $line = <TMPL> ){
    if( $line =~ m/\#\// ){
      #this is the beginning of a section
      chomp( $line );
      $line =~ s/\#\///; 
      $__SectionContent = "";
      $__section = $line;
    } elsif( $line =~ m/\#\\/ ){
      #this is the end of a section
      chomp( $line );
      Sectionize( $__section, $__SectionContent );
      #$__Sections{$__section} = $__SectionContent; 
      $__section = "__GARBAGE"; 
    } elsif( $line =~ m/^\# / ){
      #this is a comment, we can ignore it
    } elsif( $line =~ m/\#:/ ){
      #this is a variable assignment
      chomp( $line );
      $line =~ s/\#://; 
      my( $variable, $value ) = split( /=/, $line, 2 );
      if( $value =~ m/^file:/ ){
        chomp( $value );
        $value =~ s/file://; 
        my $contents = "";
        open( TMP, $value ); 
          $contents .= $line while( $line = <TMP> );
        close( TMP );
        $__Tokens{$variable} = $contents; 
      } elsif( $value =~ m/^pipe:/ ){
        #this is an output redirect
        $value =~ s/^pipe://; 
        $contents = `$value`;
        $__Tokens{$variable} = $contents;
      } else {
        $__Tokens{$variable} = $value;
      }
    } else {
      #this is content
      $__SectionContent .= $line;
    }
  }
} #end ParseSections()



#
# Parse() - parses the incomming sections and pushes the results onto
# $__OutputBuffer.  Therefore, you need to push items into Parse()
# in the order you want them output'd.
sub Parse {
  foreach( @_ ){
    my $text = $__Sections{$_};
    foreach $key ( keys %__Tokens ){
      $text =~ s/\%\%$key\%\%/$__Tokens{$key}/g if( $text =~ $key );
    }
    chomp( $text );
    $__OutputBuffer .= "$text\n\n";
  }
  return;
} #end Parse()



#
# AppendOut() - manually appends a string to the $__OutputBuffer.  
# equivalent to 'print' in perl, except this ensures that the data
# to be output'd is placed in the right order.
sub AppendOut {
  my $contents = "";
  $contents .= $_ foreach( @_ );
  $__OutputBuffer .= $contents; 
} #end AppendOut()



#
# Output() - prints the contents of $__OutputBuffer to STDOUT by default,
# or output can be re-directed to an output handler passed by @_.  This
# lacks the checking of a valid output handler in the event the output 
# handler is specified, but it will work for now, I think.
sub Output {
	$OUTPUT = shift;
	
	while( $__OutputBuffer =~ /\%\%([a-zA-Z]|[0-9])*\%\%/g ){
		foreach $key ( keys %__Tokens ){
			$__OutputBuffer =~ s/\%\%$key\%\%/$__Tokens{$key}/g if( $__OutputBuffer =~ $key );
		}
	}

	if( $OUTPUT ne "" ){
		print $OUTPUT $__OutputBuffer;
	} else {
		print STDOUT $__OutputBuffer;
	}

} #end Output()



#
# Tokenize() - takes two parameters: name and value.  Tokenize() then 
# creates an entry in the hash %__Tokens for name and value.
sub Tokenize {
  my( $name, @value ) = @_;
  my $content;
  $content .= $_ foreach( @value );
  $__Tokens{$name} = $content; 
} #end Tokenize()



#
# Sectionize() - takes two parameters: name and value.  Sectionize() 
# then creates an entry in the hash %__Sections for name and 
# value.  Does not Parse() section by default, until the user
# specifically calls Parse() on the section.
sub Sectionize {
  my( $name, @value ) = @_;
  my $content; 
  $content .= $_ foreach( @value );
  $__Sections{$name} = $content;
} #end Sectionize()



1;
