<?php

if( $id )
{
	//update this invoice status
	$paid_q = "select paid from invoices where id=$id";
	$paid_r = mysql_query( $paid_q );
	list( $status ) = mysql_fetch_row( $paid_r );


	$paid_u = "";
	if( $status )
	{
		//its paid, mark it unpaid
		$paid_u = "update invoices set paid=0 where id=$id";
	} else {
		//its not paid, mark it paid.
		$paid_u = "update invoices set paid=1 where id=$id";
	}
	mysql_query( $paid_u );
	print "Payment status updated.<br>\n";

} else {
	//no invoice specified
	print "No invoice specified, how'd you get here?<br>\n";
}

?>
