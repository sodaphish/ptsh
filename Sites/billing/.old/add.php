<?php
//$link = mysql_connect( "localhost", "root", "" );
//mysql_select_db( "billing" );
if( $formfilled and $client and $date and $taxrate and $li1_descr and $li1_qty and $li1_price )
{
	//the input form was filled, process it
	$invoice_q = "insert into invoices ( client, date, taxrate, notes ) values ( '$client', '$date', '$taxrate', '$notes' )";
	$invoice_r = mysql_query( $invoice_q ) or die( "Couldn't perform insert!" . mysql_error() );

	$invoice = mysql_insert_id();

	if( $li1_descr and $li1_qty and $li1_price ){
		$li_q = "insert into lineitems ( invoice, descr, quantity, price ) values ( '$invoice', '$li1_descr', '$li1_qty', '$li1_price' )";
		$li_r = mysql_query( $li_q ) or die( mysql_error() );
	}

	if( $li2_descr and $li2_qty and $li2_price ){
		$li_q = "insert into lineitems ( invoice, descr, quantity, price ) values ( '$invoice', '$li2_descr', '$li2_qty', '$li2_price' )";
		$li_r = mysql_query( $li_q ) or die( mysql_error() );
	}
	
	if( $li3_descr and $li3_qty and $li3_price ){
		$li_q = "insert into lineitems ( invoice, descr, quantity, price ) values ( '$invoice', '$li3_descr', '$li3_qty', '$li3_price' )";
		$li_r = mysql_query( $li_q ) or die( mysql_error() );
	}
	
	if( $li4_descr and $li4_qty and $li4_price ){
		$li_q = "insert into lineitems ( invoice, descr, quantity, price ) values ( '$invoice', '$li4_descr', '$li4_qty', '$li4_price' )";
		$li_r = mysql_query( $li_q ) or die( mysql_error() );
	}
	
	if( $li5_descr and $li5_qty and $li5_price ){
		$li_q = "insert into lineitems ( invoice, descr, quantity, price ) values ( '$invoice', '$li5_descr', '$li5_qty', '$li5_price' )";
		$li_r = mysql_query( $li_q ) or die( mysql_error() );
	}
	
	if( $li6_descr and $li6_qty and $li6_price ){
		$li_q = "insert into lineitems ( invoice, descr, quantity, price ) values ( '$invoice', '$li6_descr', '$li6_qty', '$li6_price' )";
		$li_r = mysql_query( $li_q ) or die( mysql_error() );
	}

	if( $li7_descr and $li7_qty and $li7_price ){
		$li_q = "insert into lineitems ( invoice, descr, quantity, price ) values ( '$invoice', '$li7_descr', '$li7_qty', '$li7_price' )";
		$li_r = mysql_query( $li_q ) or die( mysql_error() );
	}

	print "Invoice #$invoice was created.<br><br><a href=index.php>Click Here</a><br>\n";

} else {
	//the input form hasn't been filled, display it.
	print "
	<h1>Add an Invoice</h1>
	<form method=post action=$this>
	<input type=hidden name=formfilled value=1>
	<table width=100%>
	<tr>
	<td align=left><b>Client</b>: <select name=client>
	";

	$client_q = "select id, name from clients where visible='1'"; 
	$client_r = mysql_query( $client_q );
	while( list( $id, $name ) = mysql_fetch_row( $client_r ) )
	{
		print "<option value=$id>$name</option>\n";
	}

	$d = date( "m/d/Y" );
	print "
	</td>
	<td align=right><b>Invoice Date</b>: <input type=text name=date size=10 value=$d></td>
	</tr>
	<tr> <td colspan=2 alignt=right> Sales Tax Rate: <input type=text name=taxrate value=\"6.0\" size=4>% </td> </tr>
	</table>

	<hr>

	<b>Line Items</b><br>
	<table width=100% border=1>
	<tr>
		<td bgcolor=#cccccc><b>Description</b></td>
		<td bgcolor=#cccccc><b>Qty.</b></td>
		<td bgcolor=#cccccc><b>Price</b></td>
	</tr>
	<tr>
		<td><input type=text name=li1_descr size=92%></td>
		<td><input type=text name=li1_qty size=3></td>
		<td>$<input type=text name=li1_price size=6></td>
	</tr>
	<tr>
		<td><input type=text name=li2_descr size=92%></td>
		<td><input type=text name=li2_qty size=3></td>
		<td>$<input type=text name=li2_price size=6></td>
	</tr>
	<tr>
		<td><input type=text name=li3_descr size=92%></td>
		<td><input type=text name=li3_qty size=3></td>
		<td>$<input type=text name=li3_price size=6></td>
	</tr>
	<tr>
		<td><input type=text name=li4_descr size=92%></td>
		<td><input type=text name=li4_qty size=3></td>
		<td>$<input type=text name=li4_price size=6></td>
	</tr>
	<tr>
		<td><input type=text name=li5_descr size=92%></td>
		<td><input type=text name=li5_qty size=3></td>
		<td>$<input type=text name=li5_price size=6></td>
	</tr>
	<tr>
		<td><input type=text name=li6_descr size=92%></td>
		<td><input type=text name=li6_qty size=3></td>
		<td>$<input type=text name=li6_price size=6></td>
	</tr>
	<tr>
		<td><input type=text name=li7_descr size=92%></td>
		<td><input type=text name=li7_qty size=3></td>
		<td>$<input type=text name=li7_price size=6></td>
	</tr>
	</table>
	
	<hr>

	<b>Notes</b>:<br>
	<textarea name=notes cols=72 rows=10 wrap=hard>Thank you for your business!</textarea><br>

	<hr>

	<div align=right>
	<input type=submit>
	</div>

	</form>
	";

}
mysql_close( $link );
?>
