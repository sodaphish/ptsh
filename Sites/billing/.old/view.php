<?php

if( $id )
{


	$invoice_q = "select client, date, taxrate, paid, notes from invoices where id = $id"; 
	$invoice_r = mysql_query( $invoice_q );

	list( $client, $date, $taxrate, $paid, $notes ) = mysql_fetch_row( $invoice_r );

	//get client data
	$client_q = "select name, address1, address2, city, state, zip, phone, fax, contact from clients where id=$client"; 
	$client_r = mysql_query( $client_q );
	list( $name, $address1, $address2, $city, $state, $zip, $phone, $fax, $contact ) = mysql_fetch_row( $client_r );

	print "[ <a href=$this>Main</a> | <a href=$this?f=send>Send</a> | <a href=$this?f=edit>Edit</a>  ";
	if( ! $paid ) 
	{ 
		print "| <a href=$this?f=paid&id=$id>Mark Paid</a>"; 
	} else { 
		print "| <a href=$this?f=paid&id=$id>Mark Un-Paid</a>"; 
	} 
	print " ]<br><hr>";


	if( ! $paid )
	{
		print "<strong><big>NOT PAID</big></strong>\n";
	} else {
		print "<strong><big>PAID</big></strong>\n";
	}


	$fid = sprintf( "%06d", $id );
	print "
<pre>
                                           Forward Step Technologies
                                           317 E. 2nd Ave
                                           Lennox, SD 57039
                                           billing@forwardsteptech.com
											 
Attn: $contact
$name
$address1";

if( $address2 ){ print "$address2\n"; }
print"
$city, $state $zip
P: $phone
F: $fax


INVOICE #$fid
DATE: $date
TERMS: net-30


INVOICE
========================================================================";

	$sum = 0;
	$i = 1;

	//get line-items
	$lineitem_q = "select descr, quantity, price from lineitems where invoice=$id"; 
	$lineitem_r = mysql_query( $lineitem_q );
	while( list( $descr, $qty, $price ) = mysql_fetch_row( $lineitem_r ) )
	{
		print "
$i) $descr ($qty*\$$price)";
		$sum += ( $qty * $price );
		$i++;
	}
	$sum = sprintf( "%4.2f", $sum );
	print "
========================================================================
sub-total: \$$sum
sales tax ($taxrate%): $" . sprintf( "%4.2f", $sum * ($taxrate/100) ) . "\ntotal: $" . sprintf( "%4.2f", $sum * ($taxrate/100 + 1) ). "\n\n$notes\n";

	print "<hr>";

} else {
	print "No invoice specified.\n"; 
}

?>
