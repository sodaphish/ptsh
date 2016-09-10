<?php

switch( $sub )
{
	case 'timecard':
		//handle the timecard subs.
		switch( $c )
		{
			case 'add':
				if( $date and $hours and  $employee)
				{
					mysql_query( "insert into timecard(date,hours,employee,description,project_id) values('$date','$hours','$employee','$description', '$title_box')") or die( mysql_error() );

					print"$date $hours $employee $description";
				}else{
					include "frm_add_timesheet.html";
					}
				break;
			case 'edit':
				if($date)
				{
					//get from database
				}else{
				include "frm_edit_timesheet.html";
				}
				break;
			case 'editview':
				if($id and ! $date and ! $description )
				{
					$editview_t = mysql_query("select id, project_id,date,hours,employee,description FROM timecard WHERE id=$id")
						or die("Couldn't perform query.");
						global $id,$project_id,$date,$hours,$employee,$description;
						list($id,$project_id,$date,$hours,$employee,$description )= mysql_fetch_row($editview_t);
							include"frm_editview_timesheet.html";
					}else if($id and $date){
					$viewedit_u = ("update timecard set id='$id', date='$date', hours='$hours',employee='$employee',description='$description' where id=$id" );
					mysql_query( $viewedit_u );
					print"<p>Updated the time Card</p>";
					include"frm_edit_timesheet.html";
				}  else {
					include "frm_editview_timesheet.html";
				}
				break;
			case 'delete':
				if($id and $checkbox)
				{
					$set_active2=( "update timecard set active = 0 where id=$id ");
					mysql_query($set_active2) or die(mysql_erorr());
					print "<p>Deleted the timecard</p>";
					include "frm_delete_timesheet.html";
				}else{
					include "frm_delete_timesheet.html";
					}
				
			
				break;
			default:
				//no clue wtf to do
		}
		break;
	case 'project':
		//handle project subs.
		switch( $c )
		{
			case 'add':
				print"in add";
				if( $title and $start and $due )
				{ 
					print"in add if";
					mysql_query( "insert into project(title,due_date,start_date,description) values('$title','$due','$start','$description')") or die( mysql_error() );
					//the form has been completed, proceed with adding to datbase.
					print "$title $start $due $description";
					// this is where we would insert into the database.
				} else {
					include "frm_add_project.html";
				}
				break;

			case 'editview':
				if($id and ! $title and ! $description )
				{
					//pre-populate the edit form
					$editview_r = mysql_query("select id,title,due_date,start_date,description FROM project WHERE id =$id") 
						or die( "Couldn't perform query." );
					global $id, $title, $due, $start, $description;
					list( $id, $title, $due, $start, $description ) = mysql_fetch_row( $editview_r );
					include "frm_editview_project.html";
				} else if( $id and $title) {
					//update the database
					$viewedit_i =( "update project set title='$title', due_date='$due', start_date='$start', description='$description' where id=$id" );
					mysql_query( $viewedit_i );
					print "<p>updated your project.</p>";
				include "frm_edit_project.html";
				}else if($id and !$title){
				 print "<p>you need to include a title.</p>";
				 include "frm_editview_project.html";
				 }
				break;
			case 'edit':
				if($title)
				{
				//get the project from database
				}else{
					include "frm_edit_project.html";
				}
				break;
			case 'delete':
				if($id and $checkbox)
				{
				$set_active =("update project set active=0 where id=$id");
				mysql_query($set_active)or die(mysql_error());
				print "<p>deleted the project.</p>";
				include "frm_delete_project.html";
				
					//delete it from the database
				} else{
					include "frm_delete_project.html";
				}
				break;
			default:
				//no clue wtf to do
		}
		break;
	default:
		print "this is the default timesheet module page.";
}

?>
