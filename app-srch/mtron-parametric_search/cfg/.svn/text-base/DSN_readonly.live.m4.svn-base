define(`m4_database',`web')
define(`m4_username',`search')
#!/usr/bin/perl
# filename: DSN_readonly.pl
#  (C)opyright 1999-2000, M-tron Industries, Inc., all rights reserved.
#  written by Corey J. Steele <csteele@mtron.com>
#
# Description: use this data source if you will only need to select data
# 	from any of the tables within the 'web' database.  If you will need
#	to write data, please use DSN_readwrite.pl.
#
use DBI;

$main::__dsn = DBI->connect( 'DBI:mysql:m4_database', 'm4_username', 'readonly' ) or
  die "Connect error: $DBI::errstr\n";


