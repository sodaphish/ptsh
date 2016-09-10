<?php

class Dossier
{

	private $did = False;
	private $title = "";
	private $synopsis = "";
	private $entries = Array(); 
	
	function __construct()
	{
	}

	function __destruct()
	{
	}

	function set_title()
	{
	}

	function set_synopsis()
	{
	}

	function add_entry()
	{
	}

	function del_entry()
	{
	}

} #end Dossier class



class EntryType
{
	private $type_id = 0;
	private $type_label = "";

	function __construct()
	{
	}

	function __destruct()
	{
	}

} #end EntryType class



class DossierEntry
{

	private $entry_id = False;
	private $did = False;
	private $type = 0; #foreign key to the EntryTypes table
	private $author = "";
	private $subject = "";
	private $body = "";

	function __construct()
	{
	}

	function __destruct()
	{
	}

	function set_entry_id()
	{
	}

	function set_did()
	{
	}

	function set_type()
	{
	}

	function set_author()
	{
	}

	function set_subject()
	{
	}

	function set_body()
	{
	}

} # end DossierEntry class

?>
