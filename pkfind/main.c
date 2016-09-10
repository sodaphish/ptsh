#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define True 1
#define False 0


int chkfile( char* filename )
{
	char buffer[9]; 
	FILE *f;
	unsigned long long *test;

	if( f=fopen(filename, "r") )
	{
		while( fread(buffer,8,1,f)!=0)
		{
			buffer[]='\0';
			for(int i=0; i<8; i++)
			{
				strncat( *test, sptinrf("%02X ", (unsigned char)buffer[i]), 1);
			}
			printf("%11u\n", test);
			printf("%s\n",buffer);
		}
		fclose(f);
		return True;
	}
	return False;
}


int main(void)
{
	if( chkfile( "/home/cjs/mine/src/pkfind/README.TXT" ) )
	{
		printf( "checked file\n" );
	} else {
		printf( "couldn't check file\n" );
	}
}
