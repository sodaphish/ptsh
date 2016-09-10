#!/bin/sh

ADMIN=csteele@good-sam.com
CONF=md5summer.conf
FIND=`which find`

if [ $1 ]; then
	OUT_FILE=$1
else 
	OUT_FILE=`mktemp /tmp/$0.XXXXXX`
fi


#
# process()
#   this is the recursive function that processes each file and
#   directory.  this outputs the results of md5sum to $OUT_FILE
function process {
	if [ -f $1 ]; then
		md5sum $1 >> $OUT_FILE
	else 
		if [ -d $1 ]; then
			for f in `$FIND $1 -print -mindepth 1`; do
				process $f
			done
		fi
	fi
}


for file in `cat $CONF`; do
	process $file;
done

#rm $OUT_FILE
echo your list is in $OUT_FILE

exit
