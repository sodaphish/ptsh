<?php

global $menuItems;
global $subMenuItems;
global $f;
global $sub;
global $this;

//set module name
$moduleName = "invoice";

//populate the main menue with a link to us
array_push( $menuItems, "<a href=$this?f=invoice>Invoice</a>" );

if($f == "$moduleName")
{
	switch($sub)
	{
	case 'invoices':
	array_push( $subMenuItems, "<a href=$this?f=invoice>Back</a>");
	array_push ($subMenuItems, "<a href=$this?f=invoice&sub=invoices&c=add>Create an Invoice</a>");
	array_push($subMenuItems, "<a href=$this?f=invoice&sub=invoices&c=edit>Edit an Invoice</a>");
	array_push($subMenuItems, "<a href=$this?f=invoice&sub=invoices&c=delete>Delete an Invoice</a>");
	break;
	case 'customer':
	array_push($subMenuItems,"<a href= $this?f=invoice>Back</a>");
	array_push($subMenuItems,"<a href=$this?f=invoice&sub=customer&c=add>Add a Customer</a>");
	array_push($subMenuItems,"<a href=$this?f=invoice&sub=customer&c=edit>Edit a Customer</a>");
	array_push($subMenuItems,"<a href=$this?f=invoice&sub=customer&c=delete>Delete a Customer</a>");
	break;
default:
	array_push($subMenuItems,"<a href=$this>Home</a>");
	array_push($subMenuItems,"<a href=$this?f=invoice&sub=invoices>Invoice</a>");
	array_push($subMenuItems,"<a href=$this?f=invoice&sub=customer>Customer</a>");
	}//end switch
}//end if

?>
