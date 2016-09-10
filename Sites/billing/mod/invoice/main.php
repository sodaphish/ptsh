<?php
switch( $sub )
{
	case'invoices':
		switch($c)
		{
			case'add':
		
				if($date and $status)
				{
       					mysql_query( "insert into invoice(client,date,due_date,note,status,project_id) values('$cust_box','$date','$due_date','$note','$status','$select_project')") or die(mysql_error() );
 
					$invoice_id= mysql_insert_id();
					print"$date$due_date $client $note $status";
				}
				if($Line1 and $Qty1)
				{

					mysql_query("insert into line_items(invoice_id,description,qty,price) values( '$invoice_id','$Line1','$Qty1','$wage1')") or die(mysql_error() );
				}
				if($Line2 and $Qty2)
				{
					mysql_query("insert into line_items(invoice_id,description,qty,price) values('$invoice_id','$Line2','$Qty2','$wage2')") or die(mysql_error() );
				}
				if($Line3 and $Qty3)
				{
					mysql_query("insert into line_items(invoice_id,description,qty,price) values('$invoice_id','$Line3','$Qty3','$wage3')") or die(mysql_error() );
				}	          
				else{ 
					include"frm_invoice_add.html";
					}
				break;

			case'edit':
			    
				if($company_name)
				{
				
				//get customer from database
				}else{
					include "frm_invoice_edit.html";
				}
				break;

			case'editview':
	
				if($id and !$date and ! $status)
				{
					$editview_t = mysql_query("select id,date,due_date,client,project_id,note,status FROM invoice WHERE id=$id")
					or die("Couldn't perform query.");
					global $id,$date,$due_date,$client,$project_id,$note,$status;
	
					list($id,$date,$due_date,$client,$project_id,$note,$status)=mysql_fetch_row($editview_t);
					include"frm_invoice_editview.html";
				}else if($id and $date){
				$editview_update = ("update invoice set id ='$id',date='$date',due_date='$due_date',client='$client',project_id='$project_id',status='$status' where id=$id");
				mysql_query($editview_update);
				print"<p>Updated the Invoice</p>";
				include"frm_invoice_edit.html";
			} else {
				include "frm_invoice_editview.html";
		}
		break;

			case'delete':
				if($id and $checkbox)
				{	
					$set_active2=("update invoice set active = 0 where id=$id");
					mysql_query($set_active2) or die(mysql_error());
					print"<p>Deleted the invoice</p>";
					include "frm_invoice_delete.html";
				}else{
					include "frm_invoice_delete.html";
				}
				break;
				
		default:
		}
	break;

	case 'customer':
		switch($c)
		{
			case'add':
				if($company_name and $address1 and $city)
				{
					mysql_query("insert into client(company_name,contact,address1, address2,city,state,zip,telephone,email,fax,www)values('$company_name','$contact','$address1','$address2','$city','$state','$zip','$telephone','$email','$fax','$wwww')")or die(mysql_error() );
				
				 print"$company_name $contact $address1 $address2 $city $state $zip	$telephone $email $fax $www";  
				}else{
					include "frm_customer_add.html";
				}
				break;
				

			case'edit':
				if($company_name)
				{
					//get from database
				}else{
					include "frm_customer_edit.html";
				}
				break;
			case'editview';
				if($id and ! $company_name and ! $contact)
				{
					//pre populate the edit form
					$editview_r = mysql_query("select id,company_name,contact,address1,address2,city,state,zip,telephone,fax,www,email FROM	client WHERE id=$id") 
					or die(mysql_error() ); 
					global $id, $company_name,$contact,$address1,$address2,$city,$state,$zip,$telephone,$fax,$www,$email;
					list($id,$company_name,$contact,$address1,$address2,$city,$state,$zip,$telephone,$fax,$www,$email) = mysql_fetch_row($editview_r);
						include"frm_customer_editview.html";
	
				}else if($company_name and $id) {
					//update the database
					$viewedit_i=("update client set company_name='$company_name', contact='$contact', address1='$address1', address2='$address2', city='$city', state='$state', zip='$zip', telephone='$telephone', email='$email', fax='$fax', www='$www' where id=$id");
				mysql_query( $viewedit_i);
				print "<p>updated your project.</p>";
				include "frm_customer_edit.html";
			}
				break;
			case'delete':
				if($id and $checkbox)
				{
					$set_active3=("update client set active = 0 where id=$id");
					mysql_query($set_active3) or die(mysql_error());
					print "<p>Deleted the Customer</p>";
					include "frm_customer_delete.html";
				}else{
					include "frm_customer_delete.html";
					}

				break;
			default:




				print"this is the default invoice module page.";
	};
}
?>	
