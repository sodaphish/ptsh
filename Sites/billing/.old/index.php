
<html>
<body>

<?php
//at some point, this will need to be authenticated too.
$link = mysql_connect( "localhost", "root", "" );
mysql_select_db( "billing" );
$this = "index.php";
if( $f )
{
	// a function was specified
	// functions are: 
	// - view, add, edit, delete
	switch( $f ) {
		case 'view': 
			//we're viewing an invoice
			include "view.php";
			break;
		case 'add':
			//we're adding an invoice
			include "add.php";
			break;
		case 'edit':
			//we're editing an invoice
			break;
		case 'delete':
			//we're marking an invoice as invisible.
			break;
		case 'report':
			//we're going to run some sort of report
			break;
		case 'client':
			//manage clients
			include "client.php";
			break;
		case 'paid':
			//change the payment status bit on an invoice
			include "paid.php";
			break;
		case 'list':
			//list all the invoices (for delete/edit)
			break;
		default:
			print "unknown function!"; 
	}
} else {
	// no functions specified
	// show links to the different functions and a list of existing invoices

	print "
	[ <a href=$this?f=add>Add</a> | <a href=$this?f=report>Reports</a> | <a href=$this?f=client>Manage Clients</a> ]<br><br>
	<hr>
	<strong><big>Unpaid invoices</big></strong>
	";
	$invoice_q = "select id, date, client from invoices where paid=0"; 
	$invoice_r = mysql_query( $invoice_q );
	while( list( $id, $date, $cid ) = mysql_fetch_row( $invoice_r ) )
	{
		$client_q = "select name from clients where id=$cid";
		$client_r = mysql_query( $client_q );
		list( $name ) = mysql_fetch_row( $client_r );

		$li_q = "select quantity, price from lineitems where invoice = $id";
		$li_r = mysql_query( $li_q );
		$sum = 0;
		while( list( $qty, $price ) = mysql_fetch_row( $li_r ) )
		{
			$sum += ($qty * $price ); 
		}
		$fid = sprintf( "%06d", $id );
		$sum = sprintf( "%6.2f", $sum );
		print "<li><a href=$this?f=view&id=$id>#$fid</a> - $name, $date (\$$sum)</li>\n";
	}

	print "
	<hr>
	<strong><big>Invoice Lookup</big></strong>
	<form action=$this method=post>
	<input type=hidden name=f value=view>
	Invoice #: <input type=text name=id size=6> 
	<input type=submit value=\" &gt; &gt; \">
	</form>
	";

}
?>

</body>
</html>
