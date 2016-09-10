#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/select.h>

#include "inotify.h"

#define ALL_MASK 0xffffffff

#include "inotify.h"
#include "event_queue.h"
#include "inotify_utils.h"



/* This program will take as argument a directory name, and monitor it,
   printing event notifications to the console 
*/
int main (int argc, char **argv)
{
	/* This is the file descriptor for the inotify device */
	int inotify_fd;

	/* First we open the inotify dev entry */
	inotify_fd = open_inotify_dev();
	if (inotify_fd < 0) 
	{
		return 0;
	}



	/* We will need a place to enqueue inotify events,
           this is needed because if you do not read events
	   fast enough, you will miss them. 
	*/
	queue_t q;
	q = queue_create (128);



	/* Watch the directory passed in as argument 
	   Read on for why you might want to alter this for 
	   more efficient inotify use in your app.	
	*/
	watch_dir (inotify_fd, argv[1], ALL_MASK);
	process_inotify_events (q, inotify_fd);



	/* Finish up by destroying the queue, closing the fd
           and returning a proper code
        */
	queue_destroy (q);
	close_inotify_dev (inotify_fd);
	return 0;
}
