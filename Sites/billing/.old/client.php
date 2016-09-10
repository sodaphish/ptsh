<?php

if( $sub )
{
	//process command for client module
	switch( $sub )
	{
		case 'add':
			//add a client
			if( $name and $address1 and $city and $state and $zip and $phone and $contact and $email )
			{
				$add_i = "insert into clients ( name, address1, address2, city, state, zip, phone, fax, contact, email ) VALUES ('$name', '$address1', '$address2', '$city', '$state', '$zip', '$phone', '$fax', '$contact', '$email' )";
				$add_r = mysql_query( $add_i ) or die( mysql_error() );
				print "client added.";
			} else {
				print "inclomplete form data.  Use your browser's back button to return to the form and complete the form.<br>\n";
			}
			break;
		case 'delete':
			//delete a client
			break;
		case 'edit':
			//modify a client
			break;
		default:
			//huh?
			break;
	}

} else {
	//no command for clients module present

	//show the form to add a new client
	print "
	<h2>Add a Client</h2>
	<form method=post action=$this>
	<input type=hidden name=f value=client>
	<input type=hidden name=sub value=add>
	Name: <input type=text name=name><br>
	Address:<br>
	&nbsp;&nbsp;&nbsp;&nbsp;line1: <input type=text name=address1 size=30><br>
	&nbsp;&nbsp;&nbsp;&nbsp;line2: <input type=text name=address2 size=30><br>
	City: <input type=text name=city> State: <input type=text size=2 name=state> Zip: <input type=text name=zip size=9><br>
	Phone: <input type=text name=phone><br>
	Fax: <input type=text name=fax><br>
	<br>
	Contact: <input type=text name=contact> e-mail: <input type=text name=email><br>
	<input type=submit value=add>
	</form>
	<hr>
	";

	//show the form to delete a client
	print "
	<form method=post action=$this>
	<input type=hidden name=f value=client>
	<input type=hidden name=sub value=delete>
	<h2>Delete Client</h2> <select name=delete>
	";
	$del_q = "select id, name from clients where visible='1'"; 
	$del_r = mysql_query( $del_q );
	while( list( $id, $name ) = mysql_fetch_row( $del_r ) )
	{
		print "<option value=$id>$name</option>\n";
	}
	print " 
	</select> <input type=submit value=\"delete\">
	</form>
	<hr>
	";

	//show the form to edit an existing client
	print "
	<form method=post action=$this>
	<input type=hidden name=f value=client>
	<input type=hidden name=sub value=edit>
	<h2>Edit Client</h2> <select name=edit>
	";
	$del_q = "select id, name from clients where visible='1'"; 
	$del_r = mysql_query( $del_q );
	while( list( $id, $name ) = mysql_fetch_row( $del_r ) )
	{
		print "<option value=$id>$name</option>\n";
	}
	print " 
	</select> <input type=submit value=\"edit\">
	</form>
	";
}

?>
