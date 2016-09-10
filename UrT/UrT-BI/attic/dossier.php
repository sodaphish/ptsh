<?php

include_once( "config.php" );

?>
<html>
<head>
	<title>|WC| Dossier</title>
</head>
<body>

<div align="center">
<table width=80% border=0>
<tr><td>

<?php

$url = $caller;


$f = $_POST["f"];
if( ! $f ){
        $f = $_GET["f"];
}

$q = $_POST["q"];
if( ! $q ){
        $q = $_GET["q"];
}

$maxdepth = $_POST["maxdepth"];
if( ! $maxdepth ){
        $maxdepth = $_GET["maxdepth"];
}


$public = $_POST["public"];
if( ! $public ){
        $public = $_GET["public"];
}


$title = $_POST["title"];
if( ! $title ){
        $public = $_GET["title"];
}

$desc = $_POST["desc"];
if( ! $desc ){
        $desc = $_GET["desc"];
}

$parent = $_POST["parent"];
if( ! $parent ){
        $parent = $_GET["parent"];
}


if( ! $maxdepth ){ $maxdepth = 9; }
#print "[ <a href=$url?maxdepth=$maxdepth>main</a> ] <br><br>";

$level = 0;
$link = mysql_connect( "localhost", "root", "d@t@net12" )
	or die( mysql_error() );
mysql_select_db( "urt" ) 
	or die( mysql_error() );

if( $q >= 0 and $f == "update" )
{

	//set public to binary value
	if( $public == "on" ){ $public = 1; }else{ $public = 0; }

	//perform the update and show updated values.
	$update = "update location set loc_name='$title', loc_desc='$desc', loc_parent='$parent', loc_public='$public' WHERE loc_id = '$q'"; 
	$upd_res = mysql_query( $update ); 
	print "<font color=#00ff00<i>Record updated!</i></font><br><br>";
	show_full_location( $q );

} elseif( $f == "search" and $q >= 0 )
{

	//search the db for records matching the query
	$search = "select loc_id from location where loc_name like '%$q%' or loc_desc like '%$q%'";
	$search_res = mysql_query( $search );

	if( mysql_num_rows( $search_res ) )
	{
		while( list( $qid ) = mysql_fetch_row( $search_res ) )
		{
			print "<li><a href=$url?q=$qid&maxdepth=$maxdepth>" . process_full_loc_name( $qid ) . "</a></li>\n";
		}
	} else {
		print "Sorry, there were no matches to your query.<br>\n";
	}

} elseif( $f == "add" )
{

	if( $public == "on" ){
		$public = 1;
	} else {
		$public = 0;
	}

	$insert = "insert into location ( loc_name, loc_desc, loc_parent, loc_public ) values ( '$title', '$desc', '$parent', '$public' )"; 
	$ins_res = mysql_query( $insert )
		or die( mysql_error() ); 

	show_search_control();
	print "<br><hr><br><br>"; 
	show_threshold_control(); 
	//show all items
	show_add_location_control();
	print "<br><br>\n";
	process_location( 0 ); 
	// show dialog for adding locations

	show_add_location_control();

} elseif( $q and $f == "delete" )
{

	// delete the node and set all of its children's parent node to the parent of that node, or 0.
	$np_query = "select loc_parent from location where loc_id = $q"; 
	$np_res = mysql_query( $np_query );
	list( $new_parent ) = mysql_fetch_row( $np_res );

	$del_query = "delete from location where loc_id = $q";
	$del_res = mysql_query( $del_query ); 

	$np_update = "update location set loc_parent = $new_parent where loc_parent=$q"; 
	$npupd_res = mysql_query( $np_update );


	print "I have deleted the node and re-parented all of its children to the the parent of the node we just deleted.  Trust me, it should be okay.<br><br>"; 

	print "<br><hr><br><br>"; 
	process_location( 0 ); 

	print "<br><hr><br><br>"; 
	show_add_location_control();

} elseif( $q )
{

	//show a specific query
	show_full_location( $q );

} else {


	show_search_control();
	print "<br><br><hr><br>";
	show_threshold_control(); 
	process_location( 0 ); 
	print "<br><br><hr><br>"; 
	show_add_location_control();
	print "<br><br><hr><br>"; 
	show_search_control();

}

mysql_close($link);


/*
 ***********************************************************************************************************
 ***********************************************************************************************************
 ****** FUNCTIONS FOLLOW THIS BREAK
 ***********************************************************************************************************
 ***********************************************************************************************************
 */


function show_threshold_control()
{
	global $maxdepth; 
	global $url;

	print "
		<form action=$url method=post>
		<b>Viewing Threshold:</b> <select name=maxdepth>
		<option value=99999>None</option>
	";
	for( $x = 3; $x <= 15; $x++ )
	{
		if( $x == $maxdepth )
		{	
			print "<option value=$x SELECTED>$x</option>";
		} else {
			print "<option value=$x>$x</option>";
		}
	}
	print "
		</select>
		<input type=submit value=&gt;&gt;&gt;>
		</form>
	";

}


function show_search_control()
{
	global $url;

	print "
		<b>Search for a node:</b><br>
		<form action=$url method=post>
		<input type=hidden name=f value=search>
		<input type=hidden name=maxdepth value=$maxdepth>
		<b>Find:</b> <input type=text name=q value=\"$q\"> 
		<input type=submit value=\"&gt;&gt;&gt;\">
		</form>
	";

}



function show_add_location_control( )
{
	global $maxdepth;
	global $q;
	global $url;

	print "
		<B>Add a Node</b><br>
		<form action=$url method=post>
		<input type=hidden name=f value=add>
		<input type=hidden name=maxdepth value=$maxdepth>
		<b>Parent:</b> <select name=parent>
		<option value=0>No Parent, super-node.</option>
	";
	$loc_query = "select loc_id from location"; 
	$loc_res = mysql_query( $loc_query );
	while( list( $lid ) = mysql_fetch_row( $loc_res ) )
	{
		if( $q == $lid )
		{
			print "<option value=$lid SELECTED>" . process_full_loc_name( $lid ) . "</option>"; 
		} else {
			print "<option value=$lid>" . process_full_loc_name( $lid ) . "</option>"; 
		}
	}
	print "
		</select><br><br>
		<b>Title:</b> <input type=text name=title value=\"$name\"><br>
		<b>Public Knowledge:</b><input type=checkbox name=public><br><br>
		<b>Description:</b><br>
		<textarea name=desc wrap=soft cols=50 rows=10>$desc</textarea>
		<br><br>
		<input type=submit value=\"Add Record\">
		</form>
	"; 
}



function show_full_location( $id )
{
	global $maxdepth;
	global $url;

	// display form with values filled and submit box.
	$loc_query = "select loc_name, loc_desc, loc_parent, loc_public from location where loc_id=$id"; 
	$loc_res = mysql_query( $loc_query );
	
	list( $name, $desc, $parent, $public ) = mysql_fetch_row( $loc_res );

	print "
		<blockquote>
		<h2>$name</h2>
		[ <a href=$url?q=$id&f=delete>Delete This Node</a> ] <!-- | <a href=printview.php?q=$id>Print View</a> ]--><br><br>
		<form action=$url method=post>
		<input type=hidden name=q value=$id>
		<input type=hidden name=f value=update>
		<input type=hidden name=maxdepth value=$maxdepth>
		<b>Parent:</b> <select name=parent>
		<option value=0>No Parent, super-node.</option>
	";
	$loc_query = "select loc_id from location"; 
	$loc_res = mysql_query( $loc_query );
	while( list( $lid ) = mysql_fetch_row( $loc_res ) )
	{
		if( $lid != $parent )
		{
			print "<option value=$lid>" . process_full_loc_name( $lid ) . "</option>"; 
		} else {
			print "<option value=$lid selected>" . process_full_loc_name( $lid ) . "</option>"; 
		}
	}
	print "
		</select><br><br>
		<b>Title:</b> <input type=text name=title value=\"$name\"><br>
		<b>Public Knowledge:</b>
	"; 
	if( $public ){ print "<input type=checkbox name=public CHECKED><br><br>"; } else { print "<input type=checkbox name=public><br><br>"; }

	print "
		<b>Description:</b><br>
		<textarea name=desc wrap=soft cols=50 rows=10>$desc</textarea>
		<br><br>
		<input type=submit value=\"Update Record\">
		</form>

		<br><br>
		<h2>Objects below $name</h2>
		<i>There is no threshold applied to these objects.</i>
		<br><br>

	"; 

	// show title of children...
	process_location( $id ); 

	print "
		</blockquote>
		<br><br><hr><br>\n
	";

	show_add_location_control();

}



function process_location( $location )
{
	global $level; 
	global $maxdepth; 

	if( $level < $maxdepth )
	{
		$query = "select loc_id from location where loc_parent='$location' order by loc_name"; 
		$qres = mysql_query( $query );
		$name = process_loc_name( $location ); 
		if( mysql_num_rows( $qres ) )
		{
			show_location( $name, $level, $location );
			while( list( $locid ) = mysql_fetch_row( $qres ) )
			{
				$level++;
				process_location( $locid ); 
				$level--;
			}
		} else {
			show_location( $name, $level, $location); 
		}
	} else {
		return;
	}
}



function show_location( $n, $l, $id )
{
	global $maxdepth;
	global $url;
	while( $l )
	{
		print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"; 
		$l--;
	}
	print "<a href=$url?q=$id&maxdepth=$maxdepth>$n</a><br>\n";
}



function process_loc_name( $location )
{
	$name_query = "select loc_name from location where loc_id = $location";
	$name_result = mysql_query( $name_query );
	list( $name ) = mysql_fetch_row( $name_result );
	return $name; 
}


function process_full_loc_name( $location )
{
	$name_query = "select loc_name, loc_parent from location where loc_id = $location"; 
	$name_result = mysql_query( $name_query ); 
	list( $name_bit, $parent ) = mysql_fetch_row( $name_result ); 
	if( $parent != 0 ) 
	{
		$name_bit = process_full_loc_name( $parent ) . " > $name_bit "; 
	} 
	return $name_bit; 
}

?>


</td></tr>
</table>
</div>

</body>
</html>

<?php $logger->debug( "$caller_short __END__" );
