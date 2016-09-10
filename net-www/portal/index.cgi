#!/usr/bin/perl

#
# Personal Journal 
#  by Corey J. Steele <csteele@usd.edu>
#  (C)opyright 1998, 1999, Corey Steele, all rights reserved.
#


# get the necessary modules imported.
use CGI param, header;
use CGI::Carp qw(fatalsToBrowser);

############
#### BEGIN
############

# get the operating variables from the HTTP headers
$username   = param("username");
$password   = param("password");
$function   = param("f");
$page       = param("p");
$query      = param("q");

#set constants
$version    = "4.6.1";
$email      = "csteele\@techie.com";
$name       = "Corey J. Steele";
$filename   = "index.cgi";

$font_face  = "Helvetica";
$font_size  = "-1";

#content files
$journal_directory  = "journal";
$content_directory  = "content";
$slashdot_content   = "$content_directory/slashdot.txt";
$freshmeat_content  = "$content_directory/freshmeat.txt";
$cnn_content        = "$content_directory/cnn.txt";
$linuxtoday_content = "$content_directory/linuxtoday.txt";

# @list holds the functions that are to be linked to by print_links()
@list       = ("Main", "View", "Search" );

# the TODO arrays hold the current list of things that still need to 
#be done for a given page before it will be complete.
@TODO       = ();
@TODO2      = ();


#make sure $function isn't empty.
$function = "Login" if ( login($username, $password) == 0 && $function ne "CHANGELOG" );
$function = "Login" if ( $function eq "" );


# the header info goes in the order of: 
# $title, $font_face, $font_size, $background, $bgcolor, $text, $link, $vlink, $alink
&print_html_header( "pPortal - $function", $font_face, $font_size, "", "#ffffff", "#000000", "#0000ff", "#0000ff", "#ffff00" );


################################################################################
################################################################################



if ( lc($function) eq "login") {
    # display the login dialog
    print "
    <h1>Please Login</h1>
    <form action=\"$filename\" method=\"get\">
    <input type=\"hidden\" value=\"Main\" name=\"f\">
    <b>USERNAME</b> <input type=\"text\" name=\"username\" value=\"$username\"><br>
    <b>PASSWORD</b> <input type=\"password\" name=\"password\" value=\"\"><br>
    <input type=\"submit\" value=\" E N T E R \">
    </form>
    ";
    @TODO = ("beautify");
}



elsif ( lc($function) eq "changelog") {
    print "
    <h1>$function</h1><hr>
    <br><b>developed June '99 - present</b><br>
	<li>4.6.x - finally fixed all the bugs in the monthly roll-over script.</li>
    <li>4.5.x - expanded capabilities of search (case sensitive searches); several minor bug fixes.</li>
    <li>4.4.x - added weather content and linuxtoday news, and minor bug fixes related to path-ing the journal entries.</li>
    <li>4.3.x - bug fixes</li>
    <li>4.2.x - fixed bugs and added some menu link backs</li>
    <li>4.1.x - bug fixes</li>
    <li>4.0.x - a complete re-write; improved speed ten-fold.  integrated slashdot and freshmeat news</li>
    <br><br><b>developed January '99 - April '99</b><br>
    <li>3.x - added e-mail integration in the rawest form, borrowed heavily from c|mail 0.1.</li>
    <br><br><b>developed November '98 - December '98</b><br>
    <li>2.x - first 'formatted' journal base; all entries post 2.x have had the same format</li>
    <br><br><b>developed before November '98</b><br>
    <li>0.x/1.x - first web-based journal application, very rudimentary.</li>
    ";
    
    
}



elsif ( lc($function) eq "add_entry") {
    # submit new entry to journal
    #  procedure
    #    * write the entry to disk
    #    * display a friendly message to the user giving a confirmation
    #      and also listing some statistics on the new size of this particular 
    #      month's entry (i.e. number of lines, word count, size in bytes, etc...)
    #    * link back to main.
    @TODO = ( );
    
    if ($page eq "") {
      # there was no entry given, display a dialog to let them enter one
      &entry_dialog;
    } # end if
    
    else {
      # write the entry that the user just provided us with.
      my $date = &get_date;
      my $data_file = &get_entry_file($date);
      my $time = `date +%r`; 
      #system ("cp $data_file ../");  #make a backup, kindof
	                                 # is this still necessary? (9.8.99)
									 # no. (9.27.99)
      if (-e $data_file) {
        print "opening existing journal ($data_file) for writting...<br>\n";
        open (FIN, ">>$data_file") or die "Open Journal Entry: $!"; }
      else {
        print "opening new journal ($data_file) for writting...<br>\n";
        open (FIN, ">$data_file") or die "Open NEW Journal Entry: $!"; }
      print FIN "-----\n";
      print FIN "$date - $time\n";
      print FIN "$page\n";
      close (FIN);
      print "
      Journal entry added to <a href=$filename?username=$username&password=$password&f=View&p=$data_file>$data_file</a>...<br><br>
      <i>Keep your chronicles; keep them for yourself, your wife, and those who will follow both of you... your children.</i><br>
      \n";      
    } # end else
    
} # end add_entry



elsif ( lc($function) eq "view") {
    # view a specific entry (if specified), or list available entries
    #  procedure
    #    * if no desired entry is specified, display list of entries to view
    #      else, show specific entry
    #    * link back to main
    @TODO = ( );
    
    if ($page ne "") {
      # there has been an entry specified, open that puppy up!
      print "<font size=+3><b>$page</b></font><br>\n<blockquote>\n";
      my $data_file = $page;
      my $lastline = 0;
      open (FOUT, $data_file) or die "Open for viewing: $!";
      while (my $line = <FOUT>) {
        chomp ($line);
	if ( $line eq "-----" ) { $lastline = 1; }
	elsif ( $lastline == 1 ) {
	  print "<b>$line</b><br>\n";
	  $lastline = 0; }
	else {
	  print "<p>$line</p>\n"; }
      } #end while
      close (FOUT);
      print "
      </blockquote>
      <br><br>
      <a href=\"$filename?username=$username&password=$password&f=View\">Click Here</a> to return to the list of viewable chronicles.
      ";
    } #end of if statement
    
    else {
      # no entry specified, get the list of available entries.
      print "Select the entry you wish to view, by clicking on one of the files listed below.<br><br>\n";
      my @files = `ls -t $journal_directory/*.jrnl`;
      chomp (@files);
      foreach (@files) {
        print "<li> <a href=\"$filename?username=$username&password=$password&f=View&p=$_\">$_</a></li>\n";
      } # end foreach
    } # end else
    
} # end of view function



elsif ( lc($function) eq "search") {
    # search the journal if a query is given, otherwise show the dialog and instructions
    @TODO = ( );
    if ( $page ne "" ) {
      #there's something to search for, let's get it!
      # procedure: 
      #  * get list of files to search
      #  * open each file and search for the expression we're hunting for.
      #  * print any found results.      
      my $lastline = 0;
      my $matchcount = 0;
      $lastdate = " ";
      my @files = `ls $journal_directory/*.jrnl`;
      chomp(@files);
      foreach (@files) {
        open (F, "$_"); 
	while (my $line = <F>) {
	  chomp($line);
	  
	  if ($query eq "no") { $search_line = lc ($line); $page = lc($page); }
	  else { $search_line = $line; }
	  
	  if ( $search_line eq "-----" ) { $lastline = 1; }
	  elsif ( $lastline == 1 ) {
	    $lastdate = $line; 
	    $lastline = 0; }
	  else {
	    if ( $search_line =~ $page ) {
	      print "<b>", $matchcount + 1, "</b> <a href=\"$filename?username=$username&password=$password&f=View&p=$_\">$lastdate</a><br>\n$line<br><br>\n";
	      $matchcount++;
	    } #end if
	  } #end else 
	} #end while
	close (F);
      } #end foreach
      print "
      <hr>
      <b>";
      if ($matchcount > 1) { print "$matchcount results matched \"$page\".</b><br>\n"; }
      elsif ($matchcount == 1) { print "1 result matched \"$page\".</b><br>\n"; }
      else { print "0</b> results matched \"$page\".</b><br>\n"; }
      &search_dialog;
    } #end if
    
    else {
      # there's nothing to search for, just display the dialog.
      print "
      Use this search like any other; simply enter you're query in the dialog box, and press the submit button.  The search will run, and return any results as quickly as it can.
      <br><br>
      <b>TIP:</b> The more generic a term you search for, the more results you will get, and the longer the search will take; so be accurate, don't throw \"the\" at the engine, or it'll bloat all over you.
      <br><br>
      ";
      &search_dialog;
    } #end else
    
} # end search()



else {
    # all else fails, display the main screen
    # main screen will include:
    #  a dialog to add an entry to the journal
    #  CNN's World, US, and Tech news
    #  news from Slashdot
    #  news from Freshmeat
    #  mail reports (dubious)
    @TODO = ( );
    &entry_dialog;

    print "
	<!--
    <applet code=\"sevenAMNewsTicker.class\" codebase=\"http://www.7am.com/java\" width=450 height=15>
    <param name=\"channels\" value=\"+WORLDnews +USAnetnews +USAnews \">
    <param name=\"target\" value=\"_blank\">
    </applet>
    <br><br>
    <table width=100% border=0>
    <tr><td width=50% valign=top><font face=\"$font_face\" size=\"$font_size\">
    <b><a target=new href=http://www.freshmeat.net>freshmeat.net</a></b><br>
    ";
    &freshmeat_news;
    print "
    </font></td>
    <td width=50% valign=top><font face=\"$font_face\" size=\"$font_size\">
    <b><a target=new href=http://slashdot.org>slashdot.org</a></b><br>
    ";
    &slashdot_news;
    print "
    </font></td>
    </tr>
    <tr><td width=50% valign=top><font face=\"$font_face\" size=\"$font_size\">
    <b><a target=new href=http://linuxtoday.com>linuxtoday.com</a></b><br>
    ";
    &linuxtoday_news;
    print "
    </font></td>
    <td width=50% valign=top><font face=\"$font_face\" size=\"$font_size\">
    <b><a target=new href=http://www.cnn.com>cnn.com</a></b><br>
    ";
    &cnn_news;
    print "
    </font></td>
    </tr>
    </table>
-->
    <br><br>
    <center>
    <A target=new href=\"http://www.weather.com/weather/cities/us_sd_vermillion.html?wxmagnet\"><Img border=0 SRC=\"$content_directory/current_report.gif\"></a><br>
    <a target=new href=$content_directory/regional_sattelite.gif>regional sattelite image</a> | <a target=new href=$content_directory/regional_radar.gif>regional radar</a> | <a target=new href=$content_directory/yankton_radar.gif>Yankton radar</a>
    </center>
    ";
}



################################################################################
################################################################################



############
#### END
############
&print_html_footer();
exit();



#
################################################################################
#  NECESSARY FUNCTIONS
################################################################################
#



# this sub prints the HTML needed for the top of each html page.
# it takes a number of parameters that control the basic look 
# of the page.
sub print_html_header {
   print CGI::header();
   my ($title, $font_face, $font_size, $background, $bgcolor, $text, $link, $vlink, $alink) = @_;
   print "
   <html>
   <head>
     <title>$title</title>
   </head>
   <style type=\"text/css\">
   A          {color: \"$link\"; text-decoration: none; }
   A:visited  {color: \"$vlink\"; text-decoration: none; }
   A:active   {color: \"$alink\"; text-decoration: none; }
   </style>
   <body background=\"$background\" bgcolor=\"$bgcolor\" text=\"$text\">
   <center>
   <table width=500 border=0>
   <tr><td><font face=\"$font_face\" size=\"$font_size\">
   ";
   &print_location;
   print "<blockquote>\n";
   &print_links;
   return;
}



# this sub prints the HTML needed for the bottom of each html page.
# it takes no parameters
sub print_html_footer {
   print "
   <hr>
   <font size=\"-2\">(C) 1998, 1999, <a href=\"mailto:$email\">$name</a>, all rights reserved.<br>
   pPortal <a href=$filename?username=$username&password=$password&f=CHANGELOG>$version</a>, subject to the terms of the GNU Public License.</font>
   </blockquote>
   </font></td></tr>
   </table>
   </center>
   ";
#   print "<hr><b>THIS PAGE'S TODO</b><br>\n";
   foreach (@TODO) {
#    print "<li>$_</li>\n";
   }
   #print "<br><br>\n<b>OVERALL TODO</b><br>\n";
   foreach (@TODO2) {
     print "<li>$_</li>\n";
   }
   print "
   </body>
   </html>
   ";
   return;
}



# this sub logs a user in, returning a 1 if there was success logging the user in, 
# while returning a 0 if there was failure.
# this should be one of the FEW routines that need to be modified for multi-user
sub login {
    my ($username, $password) = @_;
    if ( ($username ne "ckrit") || ($password ne "ahh-ahs") ) { return "0"; } 
    else { return "1"; }
}



# this sub generates a simple, dynamic location indicator which is displayed
# at the top of each/most page(s) within the site.
sub print_location {
    if ( lc($function) ne "login" && login($username, $password) == 1) {
      print "<font size=+1><b>location: <a href=\"$filename?username=$username&password=$password&f=Main\">Top</a> / $function " if ( lc($function) ne "main"); 
      print "<font size=+1><b>location: Top" if ( lc($function) eq "main" );
      print "</b></font><br>\n";
    }
    elsif ( lc($function) eq "changelog") {
      print "<font size=+1><b>location: CHANGELOG</b></font><br>\n";
    }
    else {
      print "<font size=+1><b>location: Login</b></font><br>\n";
    }
    return;
}



# this sub prints the available selection of links with the exception of the
# current page.  (this is unclear, but trust me, it works.
sub print_links {
    if ( lc($function) ne "login" && login($username, $password) == 1 ) {
        print "<b>links:</b> ";
	foreach (@list) {
	    print "[ <a href=\"$filename?username=$username&password=$password&f=$_\">$_</a> ] " if ($function ne "$_");
	}
        print "<br><br>\n";
    } #end if
    elsif ( lc($function) eq "changelog" ) {
        print "<b>links:</b> [ <a href=\"$filename\">Login</a> ]<br><br>\n";
    }
}



# this sub gets the filename that we will open to write to in the Add_Entry function.
sub get_entry_file {
    #requires a date (as returned by get_date()
    my ($date) = @_;
    $date =~ tr/,//;
    my ($month, $day, $year) = split(/ /, $date);
    $month = lc($month);
    return "$journal_directory/$month-$year.jrnl";
}



# this sub gets the date for our date stamp of the entry.
# at some point, I should look into making this somewhat POSIX compliant, much 
# like all the code here.
sub get_date {
    my $month = `date +%B`; chomp ($month);
    my $day = `date +%d`; chomp ($day);
    my $year = `date +%Y`; chomp ($year);
    my $date = "$month $day, $year";
    return $date;
}



# this presents the user with a dialog for them to enter their entry into.
sub entry_dialog {
    print "
    <table width=100% border=0>
    <tr><td><font face=\"$font_face\" size=\"$font_size\">";
    my $date = &get_date;
    print "
    <b>$date</b><br>
    <center>
    <form method=post action=\"$filename\">
    <input type=hidden name=username value=\"$username\">
    <input type=hidden name=password value=\"$password\">
    <input type=hidden name=f value=\"Add_Entry\">
    <textarea wrap=\"soft\" name=p cols=50 rows=10></textarea><br>
    <input type=submit value=\" s u b m i t \">
    </form>
    </center>
    </td></tr>
    </table>\n";
    return;
}



# this is the dialog for searches
sub search_dialog {
    print "
    <form action=\"$filename\" method=post>
    <input type=hidden name=username value=\"$username\">
    <input type=hidden name=password value=\"$password\">
    <input type=hidden name=f value=\"Search\">
    ";
    if ($query eq "yes") {
        print "
	<input type=radio name=q value=yes CHECKED>Case Sensitive
	<input type=radio name=q value=no>Case In-Sensitive
	";
    }
    else {
        print "
        <input type=radio name=q value=yes>Case Sensitive
        <input type=radio name=q value=no CHECKED>Case In-Sensitive<br>
	";
    }
    print "
    <b>query:</b> <input type=text size=15 name=p value=\"$page\">
    <input type=submit value=\" s e a r c h \">
    </form>
    ";   
    return;
}



# this sub parses the freshmeat news file and outputs the news in <li> mode format.
sub freshmeat_news {
    open (FM, "$freshmeat_content") or die "Error opening Freshmeat news file, \"$freshmeat_content\": $!\n"; 
    while (my $line = <FM>) {
      if ($this_line == 0) { $title = $line; $this_line++; }
      elsif ($this_line ==1) { $date = $line; $this_line++; }
      elsif ($this_line == 2) { $URL = $line; $this_line = 0; 
        print "<li><a target=new href=$URL>$title</a></li>\n"; }
    }
    close (FM);
    return;
}




# this sub parses the linuxtoday.com content
sub linuxtoday_news {
    open (LTOD, "$linuxtoday_content") or die "Error opening LinuxToday news file, \"$linuxtoday_content\": $!\n"; 
    $in = 0;
    $atline = 0;
    while ( my $line = <LTOD>) {
        chomp ($line);
	if ($in == 1) {
	    if ($line eq "&&") {} #ignore that lline
	    elsif ($atline == 0) { $title = $line; $atline++; }
	    elsif ($atline == 1) { $url = $line; $atline++; }
	    elsif ($atline == 2) { $date = $line; print "<li><a target=new href=$url>$title</a></li>"; $atline = 0; }
	} #end if
	elsif ($in == 0) {
	    if ($line eq "&&") { $in = 1; }
	} #end elsif
    } #end while
    close (LTOD);
    return;
}



# this sub parses the slashdot news file and outputs the news in <LI> mode format.
sub slashdot_news {
    open (SD, "$slashdot_content") or die "Error opening Slashdot news file, \"$slashdot_content\": $!\n";
    my $in = 0;
    $atline = 0; 
    while (my $line = <SD>) {
        chomp ($line); 
	if ($in == 1) {
	    if ($line eq "%%") { } #ignore that line
	    elsif ($atline == 0) { $title = $line; $atline++; }
	    elsif ($atline == 1) { $url = $line; $atline++; }
	    elsif ($atline == 2) { $date = $line; $atline++; }
	    elsif ($atline == 3) { $atline++; }
	    elsif ($atline == 4) { $atline++; }
	    elsif ($atline == 5) { $atline++; }
	    elsif ($atline == 6) { $atline++; }
	    elsif ($atline == 7) { $atline++; }
	    elsif ($atline == 8) { print "<li><a target=new href=$url>$title</a></li>\n"; $atline = 0; }
	}
	elsif ($in == 0) {
	    if ($line eq "%%") { $in = 1; }
	}
    } #end while
    close (SD);
    return;
}



# this sub parses the CNN news file and outputs the news in <LI> mode format.
sub cnn_news {
    return; #circumvent the routine for now; it's broken.
    open (CN, "cnn.txt") or die "Error opening CNN news file, \"cnn.txt\": $!";
    while (my $line = <CN>) {
    }
    close (CN);
    return;
}

