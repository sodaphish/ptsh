<?php
/*
 * kw.php v0.0.2 by C.J. Steele <csteele@forwardsteptech.com>
 * (C)opyright 2004, C.J. Steele, all rights reserved.
 * 
 * 14 Apr 2004
 * 
 * This allows you to use Mozilla's keyword's to do various things
 * such as to quickly search a dictionary by simply typing in 
 * 'dict someword' in the location bar or 'search some key word' to
 * search the default search engine.
 * 
 * You have to alter your Mozilla prefs.js file (in your profile's 
 * directory) to include the following line...
 * 
 * user_pref("keyword.URL", "http://path.to.your/website/kw.php?");
 * 
 * -- or -- 
 * 
 * user_pref("keyword.URL", "http://sodaphish.com/kw.php?");
 * 
 * You'll also need to make sure your prefs.js file contains: 
 * 
 * user_pref("keyword.enabled", true);
 * 
 * After you restart Mozilla, you should be set.  You can access your 
 * keywords by simply typing in one of the following to the location 
 * of your browser with the necessary arguments... 
 * 
 * search <keywords> - searches the default search engine (google.com) for your specified arguments ($args).
 * dict <word> - searches the default dictionary (dictionary.com) for your specified arguments ($args).
 * news <keywords> - searches the NewsNow news aggrigator for your arguments ($args).
 * google <keywords> - alternative means of searching google.
 * yahoo <keywords> - searches search.yahoo.com instead of google.
 * bible <verse> - looks up the specified verse in the NASB bible.
 * scrip <keywords> - searches the NAB Bible for a particular keyword.
 * cat <keywords> - searches the Catechism of the Catholic Church for a particular keyword.
 * na <keywords> - searches newadvent.org for a particular keyword.
 * infosec <keywords> - searches sodaphish.com's infosec archives for a particular keyword.
 * php <keywrods> - search the php.net site for a keyword.
 * mysql <keywords> - search the mysql.com site for a keyword.
 * weather <keywords> - searches the NOAA's weather.gov for forcast of a \"city, st\" pair.
 * 
 * The result of each of these will take you to a different place
 * 
 * CHANGELOG
 * o  03 Aug 2004 - added support for 'weather'
 * o  14 Apr 2004 - changed the way we bring stuff in to the script, no longer using $argv.
 *                - added infosec keyword search
 *                - release of v0.0.2
 * o  13 Apr 2004 - release of v0.0.1
 */

$gargs = getenv( "QUERY_STRING" ); 
$gargs = preg_replace( "/\&/", "%26", $gargs );

$a = array( ); 
foreach( explode( "%26", $gargs ) as $arg );
{
	$arg = preg_replace( "/\ /", "%20", $arg );
	$arg = preg_replace( "/\+/", "%20", $arg );

	list( $cmd, $args ) =  explode( "%20", $arg, 2 );
	$args = preg_replace( "/\%20/", "+", $args );

	if( $cmd == "dict" )
	{
		//search dictionary.reference.com
		header( "Location: http://dictionary.reference.com/search?q=$args" );
	}else if( $cmd == "thes" ){
		//search our default search engine
		header( "Location: http://thesaurus.reference.com/search?q=$args" );
	}else if( $cmd == "search" ){
		//search our default search engine
		header( "Location: http://www.google.com/search?q=$args" );
	}else if( $cmd == "news" ){
		//search newsnow.co.uk for news
		header( "Location: http://newsnow.co.uk/newsfeed/?search=$args" );
	}else if( $cmd == "groups" ){
		//search news groups 
		header( "Location: http://groups.google.com/groups?q=$args" );
	}else if( $cmd == "google" ){
		//search google instead of the default
		header( "Location: http://www.google.com/search?q=$args" );
	}else if( $cmd == "yahoo" ){
		//search yahoo instead of default search engine
		header( "Location: http://search.yahoo.com/search?p=$args" );
	}else if( $cmd == "bible" ){
		//lookup a particular verse in the NASB Bible
		header( "Location: http://bible.gospelcom.net/cgi-bin/bible?language=english&passage=$args&version=NASB" );
	}else if( $cmd == "scrip" ){
		//search the NACCB NAB Bible for a keyword
		header( "Location: http://www.usccb.org:8765/query.html?col=bible&qt=$args&charset=iso-8859-1" );
	}else if( $cmd == "cat" ){
		//search the Catechism of the RCC for a particular keyword
		header( "Location: http://www.usccb.org:8765/query.html?col=catechis&qt=$args&charset=iso-8859-1" );
	}else if( $cmd == "cpan" ){
		//search the Perl CPAN for a particular keyword
		header( "Location: http://search.cpan.org/search?query=$args" );
	}else if( $cmd == "na" ){
		//search newadvent.org for a particular keyword
		header( "Location: http://www.google.com/custom?cof=L%3Ahttp%3A%2F%2Fwww.newadvent.org%2Fimages%2Flogo.gif%3BAH%3Acenter%3BS%3Ahttp%3A%2F%2Fwww.newadvent.org%3BAWFID%3Aba70ececdfd47fd1%3B&domains=newadvent.org&sitesearch=newadvent.org&q=$args&sa=Search" );
	}else if( $cmd == "infosec" ){
		//search newadvent.org for a particular keyword
		header( "Location: http://sodaphish.com/secnews.php?q=$args" );
	}else if( $cmd == "latin" ){
		//find latin->english lookup
		header( "Location: http://catholic.archives.nd.edu/cgi-bin/lookit.pl?latin=$args" );
	}else if( $cmd == "latin2" ){
		//an alternative latin->english lookup
		header( "Location: http://translate.travlang.com/LatinEnglish/dict.cgi?query=$args&max=50" );
	}else if( $cmd == "amazon" ){
		//find stuff on amazon
		header( "Location: /dev/null" );
	}else if( $cmd == "php" ){
		//find stuff on php.net
		header( "Location: http://www.php.net/manual-lookup.php?pattern=$args&lang=en" );
	}else if( $cmd == "urban" ){
		//find stuff on urbandictionary.com
		header( "Location: http://www.urbandictionary.com/define.php?term=$args&f=1" );
	}else if( $cmd == "mysql" ){
		//find stuff on mysql.com
		header( "Location: http://www.mysql.com/search/?q=$args" );
	}else if( $cmd == "weather" ){
		//$args = preg_replace( "/\+/", ",", $args );
		header( "Location: http://www.crh.noaa.gov/zipcity.php?inputstring=$args" );
	}else if( $cmd == "gnews" ){
		//find stuff on amazon
		header( "Location: http://news.google.com/news?hl=en&edition=us&q=$args&btnG=Search+News" );
	}else if( $cmd == "a9" ){
		//find stuff on amazon's a9 search engine.
		header( "Location: http://a9.com/$args" );
	}else if( $cmd == "wiki" ){
		//find stuff on wikipedia
		header( "Location: http://en.wikipedia.org/wiki/Special:Search?search=$args&go=Go" );
	}else if( $cmd == "ups" ){
		//track UPS packages
		header( "Location: 
		http://wwwapps.ups.com/WebTracking/processInputRequest?HTMLVersion=5.0&sort_by=status&tracknums_displayed=5&TypeOfInquiryNumber=T&loc=en_US&InquiryNumber1=$args&AgreeToTermsAndConditions=yes" ); 
	}else if( $cmd == "virus" ){
		//search for info on viruses	
		//header( "Location: http://naiwebsearch1.nai.com/siteserver/knowledge/search/nai/search-result.asp?q1=$args" );
		header( "Location: http://vil.nai.com/vil/alphar.asp?char=$args&SearchType=2" );
	}

}

print "
<h1>Oops!</h1>
<p>Your keyword ($cmd) couldn't be found.</p>
<p>This allows you to use Mozilla's keyword's to do various things such as to quickly search a dictionary by simply typing in 'dict someword' in the location bar or 'search some key word' to search the default search engine.</p>
<p>You have to alter your Mozilla prefs.js file (in your profile's directory) to include the following line...</p>
<p><code>user_pref(\"keyword.URL\", \"http://path.to.your/website/kw.php?\");</code></p>
<p>-- or --</p>
<p><code>user_pref(\"keyword.URL\", \"http://sodaphish.com/kw.php?\");</code></p>

<br /><br />

<p>Below is a list of the keywords:

<li><code>search</code>: searches the default search engine (google.com) for your specified arguments ($args).</li>
<li><code>dict</code>: searches the default dictionary (dictionary.com) for your specified arguments ($args).</li>
<li><code>urban</code>: searches urbandictionary.com for words</li>
<li><code>news</code>: searches the NewsNow news aggrigator for your arguments ($args).</li>
<li><code>google</code>: alternative means of searching google.</li>
<li><code>gnews</code>: search google news instead of default.</li>
<li><code>yahoo</code>: searches search.yahoo.com instead of google.</li>
<li><code>bible</code>: looks up the specified verse in the NASB bible.</li>
<li><code>scrip</code>: searches the NAB Bible for a particular keyword.</li>
<li><code>cat</code>: searches the Catechism of the Catholic Church for a particular keyword.</li>
<li><code>na</code>: searches newadvent.org for a particular keyword.</li>
<li><code>infosec</code>: searches sodaphish.com's infosec archives for a particular keyword.</li>
<li><code>php</code>: search the php.net site for a keyword.</li>
<li><code>mysql</code>: search the mysql.com site for a keyword.</li>
<li><code>weather</code>: searches the NOAA's weather.gov for forcast of a \"city, st\" pair.</li>
<li><code>a9</code>: searches a9.com for keywords.</li>
<li><code>wiki</code>: searches wikipedia.org for keywords.</li>
<li><code>ups</code>: automatically looks-up a package by tracking number at UPS.</li>
<li><code>virus</code>: searches for virus info at mcafee.com's AVERT.</li>
<hr>
<center>(C)opyright 2004, C.J. Steele, all rights reserved.<br>
<a href=http://sodaphish.com/files/kw.php.txt>Click here</a> for source code.</center>
"; 

?>
