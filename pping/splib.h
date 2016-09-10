#include <sys/time.h>

/* 
 * tvtolf() - converts timeval's to long floats
 * 
 * pre: tv is a properly constructed timeval struct.
 * post: a long float which joins the two parts is returned.
 */
float tvtolf( struct timeval *tv );
