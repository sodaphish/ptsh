<?php
include_once( "config.php" );

#pull in our variables
$f = $_GET['f']; 
if( ! $f ){ $f = $_POST['f']; }
$logger->debug( "f: $f" );

$completed = $_GET['completed']; 
if( ! $completed ){ $completed = $_POST['completed']; }
$logger->debug( "completed: $completed" );

$parent = $_GET['parent']; 
if( ! $parent ){ $parent = $_POST['parent']; }
$logger->debug( "parent: $parent" );

$title = $_GET['title']; 
if( ! $title ){ $title = $_POST['title']; }
$logger->debug( "title: $title" );

$body = $_GET["body"];
if( ! $body ){ $body = $_POST['body']; }
$logger->debug( "body: $body" );



function getPost( $postID )
{
	global $logger;
	$postQuery = "select postid, postparent, postdate, postauthor, posttitle, postbody, views from posts where postid=$postID";
	$postResult = mysql_query( $postQuery ) or $logger->error( mysql_error() );
	if( $postResult )
	{
		return mysql_fetch_row( $postResult );
	} else {
		return -1;
	}
} #end getPost()



function getCategory( $catID )
{
	global $logger;
	$categoryQuery = "select catid, cattitle, catdescription from categories where catid=$catID";
	$categoryResult = mysql_query( $categoryQuery ) or $logger->error( mysql_error() );
	return mysql_fetch_row( $categoryResult );
} #end getCategory()



function countViews( $catID )
{
	global $logger;
	$categoryQuery = "select views from posts where postid=$catID";
	$categoryResult = mysql_query( $categoryQuery ) or $logger->error( mysql_error() );
	list( $count ) = mysql_fetch_row( $categoryResult );
	return $count;
} #end countViews()


function findParent( $postID )
{
	global $logger;

	$parentQuery = "select postparent from posts where postid=$postID";
	$parentResult = mysql_query( $parentQuery ) or $logger->error( mysql_error() ); 
	if( $parentResult ) 
	{
		list( $parent ) = mysql_fetch_row( $parentResult );
		if( $parent > 9999 ) 
		{
			findParent( $parent );
		} elseif( $parent > 0 and $parent < 9999 ){
			return $parent;
		}
	} 
	return false;
}




function showCategory( $catID=null )
{
	global $logger;
	global $privlevel__;
	$categoryQuery = "";
	if( $catID )
	{
		$categoryQuery = "select catid, cattitle, catdescription from categories where catid=$catID"; 
	} else {
		$categoryQuery = "select catid, cattitle, catdescription from categories"; 
	}
	$categoryQueryResult = mysql_query( $categoryQuery ) or $logger->error( mysql_error() );
	if( $categoryQueryResult )
	{
		while( list( $catID, $catTitle, $catDescription ) = mysql_fetch_row( $categoryQueryResult ) )
		{
			$convCountQuery = "select count( postid ) as postCount from posts where postparent=$catID"; 
			$logger->debug( $convCountQuery );
			$postCountQueryResult = mysql_query( $convCountQuery ) or $logger->error( mysql_error() );
			if( $postCountQueryResult )
			{
				list( $postCount ) = mysql_fetch_row( $postCountQueryResult );
				print "<tr><td valign=top><b><big><big><a href=\"javascript:switchid('a$catID');\">$catTitle</a></big></big></b><br/>$catDescription<br/><br/>";
				print "<div id=\"a$catID\" style=\"padding-left:30px;display:none;\">\n";
				$postQuery = "select postID, postDate, postAuthor, postTitle, postBody, views from posts where postParent=$catID limit 50";
				$postQueryResult = mysql_query( $postQuery ) or $logger->error( mysql_error() );
				if( $postQueryResult )
				{
					while( list( $postID, $postDate, $postAuthor, $postTitle, $postBody, $views ) = mysql_fetch_row( $postQueryResult ) )
					{
						#print "<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;<a href=$caller?f=view&parent$postID>$postTitle</a> by $postAuthor ($postDate)<br/>&nbsp;&nbsp;&nbsp;&nbsp;" . substr( $postBody, 0, 80 ) . "...</td><td valign=top>$views</td>";
						$replies = countChildren( $postID );
						print "<b><a href=$caller?f=view&parent=$postID>$postTitle</a></b> by $postAuthor ($postDate)<br/>" . substr( $postBody, 0, 80 ) . "<br/>\n[ $views views | $replies replies | <a href=javascript:window.open(\"$caller?f=reply&parent=$postID\",\"win1\",\"fullscreen=0,statusbar=no\")>reply</a>"; 
						if( $privlevel__ >= 2 )
						{
							print " | <a href=$caller?completed=1&f=delete&parent=$postID>delete</a> ]<br/><br/>";
						} else {
							print "]<br/><br/>";
						}
					}
				} else {
					print "$postQuery<br/>\n";
					print mysql_error();
					$logger->error( "$postQuery" );
					$logger->error( mysql_error() );
				}
				print "\n</div>\n</td>\n<td valign=top align=center><nobr><a href=$caller?f=new&parent=$catID>New Topic</a></nobr><br/><nobr>$postCount posts</nobr>\n</td></tr>";
			}
		}
	}
} #end showCategory();


function incrementViewCounter( $postID )
{
	global $logger;
	$count = 0;;

	$viewCountQuery = "select views from posts where postid=$postID";
	$viewCountResult = mysql_query( $viewCountQuery ) or $logger->error( mysql_error() );
	if( $viewCountResult )
	{
		list( $count ) = mysql_fetch_row( $viewCountResult );
	} #else {
		#return "-1";
	#}

	$newCount = $count + 1;
	$viewCountUpdate = "update posts set views=$newCount where postid=$postID";
	$viewCountUpdateResult = mysql_query( $viewCountUpdate ) or $logger->error( mysql_error() );
	if( $viewCountUpdateResult )
	{
		$logger->debug( "$postID's new view count is $count" );
		return $count;
	}
} # end incrementViewCounter()

?>

<html>
<head>
<title><?php print $siteTitle; ?> - Admin Forums</title>
<script language="JavaScript">
var ids=new Array('a1','a2','a3','a4','a5','a6');
function switchid(id){	
	hideallids();
	showdiv(id);
}

function hideallids(){
	//loop through the array and hide each element by id
	for (var i=0;i<ids.length;i++){
		hidediv(ids[i]);
	}		  
}
function hidediv(id) {
	//safe function to hide an element with a specified id
	if (document.getElementById) { // DOM3 = IE5, NS6
		if( document.getElementById( id ) )
		{
			document.getElementById(id).style.display = 'none';
		}
	}
	else {
		if (document.layers) { // Netscape 4
			document.id.display = 'none';
		}
		else { // IE 4
			document.all.id.style.display = 'none';
		}
	}
}
function showdiv(id) {
	//safe function to show an element with a specified id
		  
	if (document.getElementById) { // DOM3 = IE5, NS6
		document.getElementById(id).style.display = 'block';
	}
	else {
		if (document.layers) { // Netscape 4
			document.id.display = 'block';
		}
		else { // IE 4
			document.all.id.style.display = 'block';
		}
	}
}
</script>
</head>
<body>


<div align="center">
<table width="80%" border=0>
<tr><td>

<?php

function countChildren( $postID )
{
	global $logger;
	$countChildrenQuery = "select count( postid ) from posts where postparent=$postID";
	$countChildrenResult = mysql_query( $countChildrenQuery ) or $logger->error( mysql_error() );
	if( $countChildrenResult )
	{
		list( $count ) = mysql_fetch_row( $countChildrenResult );
		return $count; 
	} else {
		return -1;
	}
} #end countChildren()


function showPost( $postID )
{
	global $logger;

	$postDetailQuery = "select postid, postparent, postdate, postauthor, posttitle, postbody, views from posts where postid=$postID";
	$postDetailResult = mysql_query( $postDetailQuery ) or $logger->error( mysql_error() );
	if( $postDetailResult ) 
	{
		list( $i, $p, $d, $a, $t, $b, $v ) = mysql_fetch_row( $postDetailResult );
		print "<div align=left><p><b>$t</b> by $a ($d)<br>\n";
 		print "$v views | <a href=javascript:window.open(\"$caller?f=reply&parent=$postID\",\"win1\",\"resizeable=0,height=600,width=600,statusbar=no\")>reply</a>"; 
		print "<blockquote>$b";
		if( countChildren( $i ) )
		{
			$childDetailQuery = "select postid from posts where postparent=$i";
			$childDetailResult = mysql_query( $childDetailQuery ) or $logger->error( mysql_error() );
			if( $childDetailResult ) 
			{
				while( list( $id ) = mysql_fetch_row( $childDetailResult ) )
				{
					showPost( $id );
				}
			} else {
				print "child view fail";
			} #endif
		}
		print "<br/>\n</blockquote></p></div>";
	} else {
		print "<h1>Error</h1><p>Viewing the post failed!</p><p>" . mysql_error() . "</p><p>$postDetailQuery</p>\n";
		$logger->error( $postDetailQuery ); 
	}
} #end showPost()


function showReply( $parent )
{
	global $logger;
	if( $parent )
	{
		list( $i, $p, $d, $a, $t, $b, $v ) = getPost( $parent );
		print "<strong>RE: \"$t\"</strong><br/><br/>\n";
		print "<form method=post action=$caller>\n<input type=hidden name=completed value=1>\n<input type=hidden name=f value=reply>\n<input type=hidden name=parent value=$parent>\n";
		print "<b>Subject:</b> <input type=text name=title value=\"RE: $t\"><br/>\n<textarea name=body wrap=soft rows=20 cols=60></textarea><br/>";
		print "<input type=submit>\n";
		print "</form>";
	} else {
		$logger->error( "reply with no parent?  Someone is crafting URL's." );
		print "<h1>Error</h1><p>You're trying to reply to a post without specifying the parent.  That doesn't work.  How'd you get here?</p>";
	}
} #end showReply()


switch( $f )
{
	case 'view':
		#view a post
		if( $parent )
		{
			incrementViewCounter( $parent );
			showPost( $parent );
		} else {
			print "whatchew talkin' bout willis?";
		}
		break;
	case 'new':
		if( $completed )
		{
			# they've filled out the form and submitted it.
			$postInsert = "insert into posts ( postparent, postauthor, posttitle, postbody ) values ( $parent, '$username__', '$title', '$body' )";
			$logger->debug( $postInsert );
			$postResult = mysql_query( $postInsert ) or $logger->error( mysql_error() );
			if( $postResult ) 
			{
				print "<b>Your post has been submitted.</b><br/><br/>\n";
				showCategory();
			} else {
				$logger->error( "couldn't insert a post to the dossier. ($postInsert)" );
				print "<h1>Error</h1><p>Couldn't insert your post.  This issue has been logged.</p><p>$postInsert</p><p>" . mysql_error() . "</p>";
			}
			
		} else {
			# they haven't filled out the form, give it to them.
			list( $cID, $cT, $cD ) = getCategory( $parent );
			print "<strong>posting new topic under \"$cT\"</strong><br/><br/>\n";
			print "<form method=post action=$caller>\n<input type=hidden name=completed value=1>\n<input type=hidden name=f value=new>\n<input type=hidden name=parent value=$parent>\n";
			print "<b>Subject:</b> <input type=text name=title><br/>\n<textarea name=body wrap=soft rows=20 cols=60></textarea><br/>";
			print "<input type=submit>\n";
			print "</form>";
		}
		# creaet a post/thread
		break;
	case 'reply':
		# reply to a post/thread
		if( $completed )
		{
			# they filled out the reply form
			if( ( $title ) and ( $body ) )
			{	
				#we've got what we need, go!
				$replyInsert = "insert into posts ( posttitle, postbody, postauthor, postparent ) values ( '$title', '$body', '$username__', $parent)";
				$replyResult = mysql_query( $replyInsert ) or $logger->error( mysql_error() );
				if( $replyResult ) 
				{
					print "your reply has been posted.";
					showCategory();
				}
			} else {
				#still don't have what we need.
				$logger->warn( "user didn't specify title and body" );
			} #endif
		} else {
			showReply( $parent );
		}
		break;
	case 'delete':
		# delete a post/thread
		if( $completed )
		{
			if( $parent )
			{
				$delQuery = "delete from posts where postid=$parent"; 
				$delResult = mysql_query( $delQuery );
				if( $delResult )
				{
					print "<p>Post deleted.</p>";
					$logger->info( "$parent post has been deleted." );
					showCategory(); 
				} else {
					print "<h1>Error</h1><p>Delete failed, please follow-up on this error by emailing sodaphish@gmail.com</p>";
					$logger->error( "Couldn't delete post $parent." );
				} 
			} else {
				$logger->error( "delete completed, but no parent specified? wth?" );
			}
		} else {
			showCategory();
		}
		break;
	default:
		#show the categories and sub categories
		showCategory();

}
?>

</td></tr>
</table>
</div>

</body>
</html>

<?php
$logger->debug( "$caller_short __END__" );
?>
