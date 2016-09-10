

#!/usr/bin/perl
# filename: DSN_readwrite.pl
#  (C)opyright 1999-2000, M-tron Industries, Inc., all rights reserved.
#  written by Corey J. Steele <csteele@mtron.com>
#
# Description: use this data source if you will need to select and insert data
# 	in the tables within the 'web' database.  If you only need to select
#	data, please use DSN_readonly.pl.  Use the read/write connection 
#	sparingly.
#
use DBI;

$main::__dsn = DBI->connect( 'DBI:mysql:web', 'search_rw', 'readwrite' ) or
  die "Connect error: $DBI::errstr\n";
