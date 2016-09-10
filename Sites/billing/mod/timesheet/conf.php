<?php
/*
 * mod/timesheet/conf.php 
 * 
 * This is the module-specific configuration file that populates the 
 * navigation system used for the module and sets the necessary 
 * variables as global.  If necessary, other module-wide settings could
 * be made here.
 */


//these are symbols we need to import from the main...
// the way we scope variables in our php.ini (system) file is such 
// that any symbol (variable) used in the modules must be defined
// as 'global's here.
global $menuItems;
global $subMenuItems;
global $f;
global $sub;
global $this;


//this sets our module name which can be used throughout the 
// module as well as 
$moduleName = "timesheet";


/*######################################################################
 * NAVIGATION CODE -- sets up the menus viewed by the users.
 */#####################################################################

//populate the main menu with a link to us.
array_push( $menuItems, "<a href=$this?f=timesheet>TimeSheet</a>" );

//setup context-sensitive sub-menus
// this setsup the navigation menus to be context sensitive depending
// on what the function ($sub) is.
if( $f == "$moduleName")
{

	switch( $sub )
	{
		case 'project':
			//the sub-menu for managing projctects
			array_push( $subMenuItems, "<a href=$this?f=timesheet>Back</a>" );
			array_push( $subMenuItems, "<a href=$this?f=timesheet&sub=project&c=add>Add a Project</a>" );
			array_push( $subMenuItems, "<a href=$this?f=timesheet&sub=project&c=edit>Edit a Project</a>" );
			array_push( $subMenuItems, "<a href=$this?f=timesheet&sub=project&c=delete>Delete a Project</a>" );
			break;
		case 'timecard':
			//the sub-menu for managine timecards
			array_push( $subMenuItems, "<a href=$this?f=timesheet>Back</a>" );
			array_push( $subMenuItems, "<a href=$this?f=timesheet&sub=timecard&c=add>Add an Entry</a>" );
			array_push( $subMenuItems, "<a href=$this?f=timesheet&sub=timecard&c=edit>Edit an Entry</a>" );
			array_push( $subMenuItems, "<a href=$this?f=timesheet&sub=timecard&c=delete>Delete an Entry</a>" );
			break;
		default:
			//show all our sub functionality for this module
			array_push( $subMenuItems, "<a href=$this>Home</a>" );
			array_push( $subMenuItems, "<a href=$this?f=timesheet&sub=project>Projects</a>" );
			array_push( $subMenuItems, "<a href=$this?f=timesheet&sub=timecard>Time Cards</a>" );
	} //end switch

} //end if


?>
