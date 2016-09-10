Tables_in_fw
blocked
Field	Type	Null	Key	Default	Extra
id	int(11)		PRI	NULL	auto_increment
time	varchar(16)				
date	varchar(32)		MUL		
proto	varchar(16)				
src	varchar(64)		MUL		
srcprt	varchar(16)				
dst	varchar(64)		MUL		
dstprt	varchar(16)				
dddates
Field	Type	Null	Key	Default	Extra
id	int(11)		PRI	NULL	auto_increment
date	varchar(32)		MUL		
leaseinfo
Field	Type	Null	Key	Default	Extra
id	int(11)		PRI	NULL	auto_increment
date	datetime		MUL	0000-00-00 00:00:00	
type	int(1)			0	
ip	varchar(32)		MUL		
mac	varchar(32)		MUL		
host	varchar(64)	YES		NULL	
others
Field	Type	Null	Key	Default	Extra
id	int(11)		PRI	NULL	auto_increment
time	varchar(16)				
date	varchar(32)		MUL		
pixerror	varchar(32)				
message	text		MUL		
stats
Field	Type	Null	Key	Default	Extra
id	int(11)		PRI	NULL	auto_increment
date	varchar(32)		MUL		
rpt	varchar(8)		MUL		
data	text				
