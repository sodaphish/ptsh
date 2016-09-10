/* 
 * GoogleQuery - (C)opyright 2002, Corey J. Steele, all rights reserved. 
 * 
 *   Initial coding completed on July 3, 2002 exclusively by csteele@sodaphish.com
 * 
 * DESCRIPTION
 *     This program queries google for command-line specified query arguments.  The results are
 *     then dumped to STDOUT in the form of an SQL Query.
 * 
 * CHANGES
 * 07-03-02 Initial coding completed
 * 
 */

import com.google.soap.search.*;
import gnu.regexp.*;

class GoogleQuery {


	public static void main( String[] args )
	{
		String clientKey = "CvBdp/J6lGTLDNn0Y7V6qTnU9LTwSmZJ";
		GoogleSearch search = new GoogleSearch(); 
		if( args.length < 1 )
		{
			System.out.println( "Error: no query specified." );
		} else {
			String queryString = args[0];  
			for( int y = 1; y < args.length; y++ )
			{
				queryString = queryString + " " + args[y]; 
			} 
			try {
				search.setKey( clientKey );
				search.setQueryString( queryString );
				for( int x = 1; x <= 500; x += 10 )
				{
					search.setStartResult( x );
					GoogleSearchResult queryResults = search.doSearch();
					GoogleSearchResultElement[] result = queryResults.getResultElements();
					for (int i = 0; i < result.length; ++i) {
						String title = result[i].getTitle();
						String url = result[i].getURL();
						try {
							RE magic = new RE( "'" );
							title = magic.substituteAll( title, "\\'" );
							url = magic.substituteAll( url, "\\'" );
						} catch ( REException regexFault ) {
							System.out.println( regexFault.getMessage() );
						} //end gnu.regex try-catch 
						//insertData( url, title );
						System.out.println( url + " --- " + title + "\n\n" );
					} 
				} //end search foor-loop
			} catch ( GoogleSearchFault searchFault ) {
				System.out.println( searchFault );
			} //end GoogleSearch try-catch
		} //end usage if-else
	} //end main


	private static boolean insertData( String url, String title )
	{
		System.out.println( "INSERT INTO urls ( url, title ) VALUES ( '" + url + "', '" + title + "' )" );
		return true;
	} //end insertData


} //end GoogleQuery class
