/*
 * portping v0.0.2 by C.J. Steele <csteele@sodaphish.com> (a.k.a. SodaPhish)
 *
 * 15 Feb 2004
 *
 * TODO/ROADMAP:
 * 	+ need to interrupt connect()'s that last longer than 1s.
 * 	+ time calls to connect() for output
 *	+ write udp_portping()
 * 	+ write man page
 *
 */

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include <signal.h>
#include <sys/time.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>

//#include "splib.h"

#define __DEBUG__ 0

char me[9] = "portping";
char *opt_host = NULL;		/* the target host specified on command-line */
char *opt_port = NULL;		/* the port specified on command-line */
char *opt_proto = NULL;		/* the protocol specified on command-line */
int opt_count = 0;			/* the number of times to try */
int opt_delay = 1;			/* the number seconds between attempts to connect */


int initopts( int argc, char **argv )
{
	int index;
	int c;
	opterr = 0;

	/* process our getopts until there are none... */
	while ((c = getopt (argc, argv, "h:p:P:c:d:")) != -1)
	{
	   	switch (c)
		{
		   	case 'h':
   				opt_host = optarg;
   				break;
   			case 'p':
   				opt_port = optarg;
   				break;
   			case 'P':
   				opt_proto = optarg;
   				break;
			case 'c':
				opt_count = atoi( optarg );
				break;
			case 'd':
				opt_delay = atoi( optarg );
				break;
   			case '?':
   				if (isprint (optopt))
   					fprintf (stderr, "Unknown option `-%c'.\n", optopt);
   				else
   					fprintf (stderr,
   					"Unknown option character `\\x%x'.\n",
   			optopt);
   				return 1;
   			default:
				opterr = 1;
   		}
	} /* end of while */

	/* take care of the leftovers. */
	for( index = optind; index < argc; index++)
	{
		if( opt_host == NULL ) 
		{
			opt_host = argv[index];
		} else {
			if( opt_port == NULL )
				opt_port = argv[index];
			else 
				if( opt_proto == NULL )
				opt_proto = argv[index];
		}
	}

	/* we have to have at least opt_host and opt_port */
	if( opt_host && opt_port )
	{
		if( opterr )
			return -1;
		return 1;
	} 

	return -1;

} /* end initopts() */




int showusage( )
{
	/* printf( "%s usage: %s [-h] hostname [-p] port [-P] proto\n\n", me, me ); */
	printf( "(C)opyright 2004, C.J. Steele <csteele@sodaphish.com> (a.k.a. SodaPhish), all rights reserved.\n" );
	printf( "%s usage: %s [-h] host [-p] port [-d x] [-c y]\n", me, me );
	printf( "\t-h hst\tspecify the target host, either by ip or name\n" );
	printf( "\t-p prt\tspecify the target port, currently tcp only\n" );
	printf( "\t-d sec\tthe number of whole seconds between 'pings'\n" );
	printf( "\t-c cnt\tthe number of 'pings' to send, if unspecified, infinity will be assumed\n\n" );
} /* end showusage() */




int udp_portping( const char* target, const char* targetport )
{
	printf( "not implemented yet...\n" );
	return 0;
} /* end udp_portping */




int tcp_portping( const char* target, const char* targetPort )
{
    int clientSocket, remotePort, status = 0;
    struct hostent *hostPtr = NULL;
    struct sockaddr_in serverName = { 0 };
    char *remoteHost = NULL;
	struct timeval timeStart;
	struct timeval timeEnd; 
	struct timezone tz; //GMT is fine, for now.
	int timeDiff = 0;

	(void)gettimeofday( &timeStart, &tz );

    remoteHost = (char*)target;
    remotePort = atoi( targetPort );

    clientSocket = socket( PF_INET, SOCK_STREAM, IPPROTO_TCP );
    if( -1 == clientSocket )
	        perror( "socket()" );

    hostPtr = gethostbyname( remoteHost );
    if( NULL == hostPtr )
    {
        hostPtr = gethostbyaddr( remoteHost, strlen(remoteHost), AF_INET );
        if (NULL == hostPtr)
    		    perror( "Error resolving server address" );
    }

    serverName.sin_family = AF_INET;
    serverName.sin_port = htons(remotePort);
    (void)memcpy( &serverName.sin_addr, hostPtr->h_addr, hostPtr->h_length );

	alarm( 1 );
	status = connect( clientSocket, (struct sockaddr*) &serverName, sizeof(serverName) );
	alarm( 0 ); // void the alarm, because it didn't fire.
    close( clientSocket );

	(void)gettimeofday( &timeEnd, &tz );

	if( timeEnd.tv_sec != timeStart.tv_sec )
	{
		// the connect() occurred over different seconds, 
		// so the time between start and end will be incorrect if not handled here properly
	}
	timeDiff = timeEnd.tv_usec - timeStart.tv_usec; 

    if (-1 == status)
			printf( ".%i s -- FAILED to connect to %s:%s/tcp\n", timeDiff, target, targetPort );
	else
			printf( ".%i s -- connected to %s:%s/tcp\n", timeDiff, target, targetPort );

	return 0;

} /* end tcp_portping() */




/* 
 * sigConnectTimeout( int )
 * 
 * handle alarms -- generally will only be the result of connect()'s that take too long.
 * 
 * pre: alarm() fired triggering SIG_ALRM
 * post: SIG_DFL has been set
 */
void sigConnectTimeout(int sig)
{
	alarm( 0 ); //void any timer(s)
	printf( "timedout connecting to %s:%s/%s\n", opt_host, opt_port, opt_proto );
	//set sa_handler to SIG_DFL so the process doesn't terminate... could be an issue
	//__sigaction_u.__sa_handler = SIG_DFL;  /* why isn't this found? */
	raise( 0 );
} /* end sigConnectTimeout() */





int main (int argc, char **argv)
{
	int x;

	signal( SIGALRM, sigConnectTimeout ); //handle alarms caused by connect() timeouts

	if( initopts( argc, argv ) < 1 )
	{
		showusage();
		exit(1);
	}

 	if( __DEBUG__ )
			printf( "host: %s port: %s proto: %s count: %i delay: %i\n", opt_host, opt_port, opt_proto, opt_count, opt_delay ); 

	if( ! opt_proto )
			opt_proto = "tcp"; 

	if( opt_count )
	{
		for( x = 1; x <= opt_count; x++ )
		{
			if( strcmp( opt_proto, "tcp" ) == 0)
					tcp_portping( opt_host, opt_port );
			else if( strcmp( opt_proto, "udp" ) == 0)
					udp_portping( opt_host, opt_port );
			sleep( opt_delay );
		}
	} else {
		for(;;)
		{
			if( strcmp( opt_proto, "tcp" ) == 0)
					tcp_portping( opt_host, opt_port );
			else if( strcmp( opt_proto, "udp" ) == 0)
					udp_portping( opt_host, opt_port );
			sleep( opt_delay );
		}
	}
	return 0;
} /* end main */
