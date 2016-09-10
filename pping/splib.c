#include <sys/time.h>
#include <stdio.h>

float tvtolf( struct timeval tv )
{
	float rtv = 0.0;
	rtv += (float)tv.tv_sec;
	rtv += (float)tv.tv_usec / 1.0; //tv_usec is a long (32-bit int)
	return rtv;
}


void main()
{
	struct timeval timeStart, timeEnd;
	float timeStart_f, timeEnd_f;
	struct timezone tz; 
	int x, y = 0;

	(void)gettimeofday( &timeStart, &tz );
	for( x = 0; x < 10000; x++ ){ y++; }
	(void)gettimeofday( &timeEnd, &tz );

	timeStart_f = tvtolf( timeStart );
	timeEnd_f = tvtolf( timeEnd );

	printf( "%f - %f = %f\n", timeEnd_f, timeStart_f, timeEnd_f - timeStart_f );
}
