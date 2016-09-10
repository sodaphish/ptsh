#include <Carbon/Carbon.h>

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>

#define __DEBUG__ 0

int tcp_portping( const char* target, const char* targetport )
{
    int clientSocket, remotePort, status = 0;
    struct hostent *hostPtr = NULL;
    struct sockaddr_in serverName = { 0 };
    char *remoteHost = NULL;

    remoteHost = (char*)target;
    remotePort = atoi(targetport);

    clientSocket = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (-1 == clientSocket)
	        perror("socket()");

    hostPtr = gethostbyname(remoteHost);
    if (NULL == hostPtr)
    {
        hostPtr = gethostbyaddr(remoteHost, 
		strlen(remoteHost), AF_INET);
        if (NULL == hostPtr)
    		    perror("Error resolving server address");
    }

    serverName.sin_family = AF_INET;
    serverName.sin_port = htons(remotePort);
    (void) memcpy(&serverName.sin_addr, hostPtr->h_addr, hostPtr->h_length);

    status = connect(clientSocket, (struct sockaddr*) &serverName, sizeof(serverName));
    if (-1 == status)
			printf( "FAILED to connect to %s:%s/tcp\n", target, targetport );
	else
			printf( "connected to %s:%s/tcp\n", target, targetport );

    close(clientSocket);
	return 0;

} /* end tcp_portping() */


int main(int argc, char* argv[])
{
    IBNibRef 		nibRef;
    WindowRef 		window;
    
    OSStatus		err;

    // Create a Nib reference passing the name of the nib file (without the .nib extension)
    // CreateNibReference only searches into the application bundle.
    err = CreateNibReference(CFSTR("main"), &nibRef);
    require_noerr( err, CantGetNibRef );
    
    // Once the nib reference is created, set the menu bar. "MainMenu" is the name of the menu bar
    // object. This name is set in InterfaceBuilder when the nib is created.
    err = SetMenuBarFromNib(nibRef, CFSTR("MenuBar"));
    require_noerr( err, CantSetMenuBar );
    
    // Then create a window. "MainWindow" is the name of the window object. This name is set in 
    // InterfaceBuilder when the nib is created.
    err = CreateWindowFromNib(nibRef, CFSTR("MainWindow"), &window);
    require_noerr( err, CantCreateWindow );

    // We don't need the nib reference anymore.
    DisposeNibReference(nibRef);
    
    // The window was created hidden so show it.
    ShowWindow( window );
    
    // Call the event loop
	RunApplicationEventLoop();


CantCreateWindow:
CantSetMenuBar:
CantGetNibRef:

	return err;
}

