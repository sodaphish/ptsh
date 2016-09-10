#if !defined(MAY_NOT_MODIFY)
/****==========------------------------------------------------==========****/
/*                                                                          */
/* tcpshow, v1.74                                                           */
/*                                                                          */
/* Quickie to decode a "tcpdump" savefile.                                  */
/*                                                                          */
/* The application data is displayed as ASCII -- application protocols are  */
/* not decoded.                                                             */
/*                                                                          */
/* The data captured by "tcpdump" might be less than in the original        */
/* packet.  We kludge a solution to this with setjmp()/longjmp().           */
/*                                                                          */
/* Although written to read tcpdump savefiles, with tcpdump itself as a     */
/* front-end, it'll decode any hex dump that adheres to the format          */
/* expected.  Some programs which capture network data offer an option to   */
/* save the trace to a file in hex format -- this can often be massaged     */
/* easily with Perl/awk/sh scripts to turn it into the format expected.     */
/* As a special case, "tcpdump -s 1518 -lenx | tcpshow -cooked" works       */
/* rather well, and "tcpdump -s 1518 -lenx | tcpshow -cooked -data" is nice */
/* for watching the data traffic in real time.                              */
/*                                                                          */
/* ------------------------------------------------------------------------ */
/*                                                                          */
/* Known Bugs:                                                              */
/* 1. If "-s n" wasn't specified with tcpdump, then when using the          */
/*    "-nodata" flag, the "DATA: n bytes" line doesn't get output for the   */
/*    1st packet.                                                           */
/*                                                                          */
/* ------------------------------------------------------------------------ */
/*                                                                          */
/* Copyright (c) 1996, 1997, 1998 I.T. NetworX Ltd.  All rights reserved.   */
/*                                                                          */
/* This source code is owned and copyrighted by I.T. NetworX Ltd.  This     */
/* file and all files derived from it, directly or indirectly (such files   */
/* collectively and separately being referred to henceforth as "this file") */
/* may be used, modified and redistributed subject to the following six     */
/* Conditions.                                                              */
/*                                                                          */
/* Condition 1 of 6:                                                        */
/* That all text (code/comments, etc.) in this file surrounded by the macro */
/* block "#if !defined(MAY_NOT_MODIFY) ... #endif", including the macro     */
/* statements themselves, may not be modified in any way, or deleted.  In   */
/* particular, this comment block and the printf() statements identifying   */
/* I.T. NetworX as being the copyright owner, in the function usage(), may  */
/* not be modified or deleted.  The single, only, exception to this is that */
/* the non-inclusion of C comments by a C compiler/linker, in the object    */
/* and executable images it produces, is permitted.                         */
/*                                                                          */
/* Condition 2 of 6:                                                        */
/* That no financial gain be made from using this file or modifying this    */
/* file.  It is permitted to charge for redistributing this file.           */
/*                                                                          */
/* Condition 3 of 6:                                                        */
/* That no conditions other than these six Conditions be applied to the     */
/* use, modification or redistribution of this file.                        */
/*                                                                          */
/* Condition 4 of 6:                                                        */
/* That all modifications to this file show prominently the name of the     */
/* person that made the change and the date on which the change was made.   */
/*                                                                          */
/* Condition 5 of 6:                                                        */
/* That I.T. NetworX, its employees, agents and everybody else in the world */
/* dead, living and yet to be born, are hereby free from liability of all   */
/* and every kind arising from the use of this file by anybody for any      */
/* purpose.  This file comes "as is" and all warranties, express or         */
/* implied, are disclaimed.  As the manual page for chat(1) says, "if it    */
/* breaks, then you get to keep both pieces".                               */
/*                                                                          */
/* Condition 6 of 6:                                                        */
/* That I.T. NetworX reserves the right to alter these Conditions at any    */
/* time without giving prior notice, such alterations to apply only to the  */
/* version current at the time of issue of the alterations and all later    */
/* versions, and such alterations to apply only to versions produced        */
/* exclusively by I.T. NetworX or its agents.                               */
/*                                                                          */
/* Addendum to Copyright:                                                   */
/* I'm not a legal eagle and I worded the above notice off the top of my    */
/* head, so it may be full of holes, but the spirit of my intentions are    */
/* clear from reading it.  Please respect these intentions.                 */
/*                                                                          */
/* Me too:                                                                  */
/* If anybody makes significant improvements to this file, such as adding   */
/* decode support for DHCP or DNS traffic, or IP and TCP options, I would   */
/* appreciate it if they sent me a copy of their work (mike@NetworX.ie).    */
/* Thanks.                                                                  */
/*                                                                          */
/* ------------------------------------------------------------------------ */
/*                                                                          */
/* File layout is as follows:                                               */
/* system includes                                                          */
/* local includes                                                           */
/* #define macros                                                           */
/* typedefs                                                                 */
/* declarations of extern variables                                         */
/* declarations of extern functions                                         */
/* declarations of global variables                                         */
/* declarations of global functions                                         */
/* declarations of static variables                                         */
/* declarations of static functions                                         */
/* definitions of functions                                                 */
/* (all functions and variables are declared/defined in alphabetical order) */
/*                                                                          */
/* ------------------------------------------------------------------------ */
/*                                                                          */
/* Compiles as follows:                                                     */
/* cc -s -O -o tcpshow tcpshow.c                                            */
/*                                                                          */
/* ------------------------------------------------------------------------ */
/*                                                                          */
/* Who and when:                                                            */
/* MikeRyan, 11apr96.                                                       */
/*                                                                          */
/* I.T. NetworX,                                                            */
/* Stonebridge House,                                                       */
/* Shankill,                                                                */
/* Co. Dublin.                                                              */
/* Ireland.                                                                 */
/* Phone: +353-1-28-27-233                                                  */
/* Fax:   +353-1-28-27-230                                                  */
/* Email: mike@NetworX.ie                                                   */
/*                                                                          */
/* ------------------------------------------------------------------------ */
/*                                                                          */
/* Modification History                                                     */
/* MikeRyan, 14may96: Allow "tcpdump" expressions to be passed in.          */
/* MikeRyan, 15may96: Added UDP decode logic.                               */
/* MikeRyan, 16may96: Added ICMP decode logic.                              */
/* MikeRyan, 16may96: Added -b switch to break long lines                   */
/*                          -w option to specify the width of the page      */
/*                          -h flag to give help on usage.                  */
/* MikeRyan, 28may96: Added -nolink                                         */
/*                          -nodata                                         */
/*                          -noip                                           */
/*                          -track                                          */
/*                          -terse                                          */
/*                          -sb                                             */
/*                          -s                                              */
/* MikeRyan, 25jun96: Incorporated my "general.h" typedef's, so that the    */
/*                    present source file doesn't depend on any             */
/*                    non-standard header files.  This allows it to be      */
/*                    distributed as a single file.  Also included the      */
/*                    copyright notice, as I'm making the program freely    */
/*                    available.                                            */
/* MikeRyan, 26jun96: Added -cooked and -pp.                                */
/* MikeRyan, 26may97: Made "-terse" the default; added "-verbose".          */
/* mr971010   v1.2    Reformatted layout to match my current preference     */
/*                    (purely cosmetic change).                             */
/* mr971014   v1.3    Set width of page to 60 characters and turned on line */
/*                    wrap by default.  Changed "bflag" to "noBflag" in the */
/*                    process.                                              */
/* mr971021   v1.4    (a) Always show the "Packet n" line (it wasn't being  */
/*                        displayed when "-data" was used).                 */
/*                    (b) Display the separator line (prsep()) before the   */
/*                        1st packet (this is more consistent).             */
/*                    (c) Added "-noPortNames" flag, to turn off mapping    */
/*                        port numbers into port names.  Now, port names    */
/*                        are shown except when "-noPortNames" is used.     */
/*                    (d) Display short hostnames instead of IP addresses,  */
/*                        unless "-noHostNames" is specified; display fully */
/*                        qualified hostnames if "-fqdn" is specified.      */
/*                        Function svcname() was renamed to portName() and  */
/*                        enhanced a little during all this.                */
/* mr971120   v1.5    (a) Added ARP/RARP decoding.                          */
/* mr980117   v1.6    (a) Added delta time for 2nd and subsequent packets.  */
/* mr980118   v1.7    (a) Corrected minor 'bug' in etherAddr().             */
/*                    (b) Added -noEtherNames and the code to print         */
/*                        Ethernet names (which happens by default).  This  */
/*                        code is presently particular to FreeBSD, so to    */
/*                        leave it out (so that Ethernet names are never    */
/*                        displayed) define the macro NOETHERNAMES.         */
/* mr980129   v1.71   (a) Changed version from x.y to x.yz.                 */
/*                    (b) Added icmpExtras() to display the additional      */
/*                        information in some ICMP headers.                 */
/* mr980130   v1.72   (a) Added ETHER_PROTO_UNKNOWN to correct a bug in     */
/*                        showHdr().                                        */
/* mr980202   v1.73   (a) Changed "-data" to "-minDecode", indicating a     */
/*                        minimal decode of the headers.  The change was    */
/*                        made because "tcpshow -data -nodata" had the      */
/*                        potential for confusion!                          */
/*                    (b) Changed options like "-nodata" to "-noData".      */
/*                    (c) Recoded etherProto() to generalise it a bit more. */
/*                        Also removed ETHER_PROTO_UNKNOWN as it's not      */
/*                        needed given the recoding of etherProto().        */
/* mr980303   v1.74   (a) Don't display "-noEtherNames" as a run-time       */
/*                        option if NOETHERNAMES is defined.                */
/*                    (b) Changed "-minDecode" to "-minHdrDecode".          */
/*                                                                          */
/****==========------------------------------------------------==========****/
#endif


#include <sys/types.h>                 // mr971021 Next four includes
#include <sys/socket.h>
#if !defined(NOETHERNAMES)
#include <net/ethernet.h>              // mr980118 Particular to FreeBSD?
#endif
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <setjmp.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>


/* Some general defines.                                                    */
#if defined(FALSE)
#undef FALSE
#endif
#if defined(TRUE)
#undef TRUE
#endif
#define FALSE           (boolean)0
#define TRUE            (boolean)1
#define elif               else if
#if !defined(reg)
#define reg               register     /* For debugging purposes            */
#endif


#define VERSION               1.74     /* Please change when appropriate    */
#define COOKER           "tcpdump"
#define MAXCOOKARGS            100     /* Max tcpdump expression words      */

#define MAXPKT               10240     /* Should be 1518 for Ethernet       */
#define NCOLS                   60     /* mr971014 Changed from 1024        */
#define MAX_HOSTNAMELEN        255     // mr971021
#define MAX_PORTNAMELEN         32     // mr971021
#define ETHER_ADDRLEN           17     // mr971120 Ether addr in ASCII
#define IP_ADDRLEN              15     // mr971120 IP addr in ASCII

// Ethernet protocol types (add to this list as needed).
#define ETHER_PROTO_IP      0x0800
#define ETHER_PROTO_ARP     0x0806
#define ETHER_PROTO_RARP    0x8035

// ARP/RARP header elements.
#define ARP_REQ                  1
#define ARP_RSP                  2
#define RARP_REQ                 3
#define RARP_RSP                 4
#define ARP_HW_ETHER             1     // Hardware type is Ethernet
#define ARP_PROTO_IP        0x0800     // Protocol type is IP

/* IP header elements.                                                      */
#define IPHDRLEN                20
#define FRAGOFF             0x1FFF
#define MF                  0x2000
#define DF                  0x4000

/* TCP header elements.                                                     */
#define TCPHDRLEN               20
#define URG                 0x0020
#define ACK                 0x0010
#define PSH                 0x0008
#define RST                 0x0004
#define SYN                 0x0002
#define FIN                 0x0001

/* UDP header elements.                                                     */
#define UDPHDRLEN                8

/* IP protocol types.                                                       */
#define IP                       0
#define ICMP                     1
#define IGMP                     2
#define GGP                      3
#define IPENCAP                  4
#define ST                       5
#define TCP                      6
#define EGP                      8
#define PUP                     12
#define UDP                     17
#define HMP                     20
#define XNSIDP                  22
#define RDP                     27
#define ISOTP4                  29
#define XTP                     36
#define IDPRCMTP                39
#define RSVP                    46
#define VMTP                    81
#define OSPF                    89
#define IPIP                    94
#define ENCAP                   98

/* ICMP types.                                                              */
#define ECHO_REPLY               0
#define DST_UNREACH              3
#define SRC_QUENCH               4
#define REDIRECT                 5
#define ECHO_REQ                 8
#define ROUTER_AD                9
#define ROUTER_SOL              10
#define TIME_EXCEED             11
#define PARAM_PROB              12
#define TIME_REQ                13
#define TIME_REPLY              14
#define INFO_REQ                15
#define INFO_REPLY              16
#define MASK_REQ                17
#define MASK_REPLY              18

/* ICMP codes for type == Destination Unreachable.                          */
#define NET_UNREACH              0
#define HOST_UNREACH             1
#define PROTO_UNREACH            2
#define PORT_UNREACH             3
#define DF_SET                   4
#define SRCROUTE_FAILED          5
#define DSTNET_UNKNOWN           6
#define DSTHOST_UNKNOWN          7
#define SRCHOST_ISOLATED         8
#define DSTNET_PROHIB            9
#define DSTHOST_PROHIB          10
#define NET_UNREACH_TOS         11
#define HOST_UNREACH_TOS        12
#define COMM_PROHIB             13
#define HOST_PREC_VIOL          14
#define PREC_CUTOFF             15

/* ICMP codes for type == Redirect.                                         */
#define REDIR_FOR_NET            0
#define REDIR_FOR_HOST           1
#define REDIR_FOR_TOSNET         2
#define REDIR_FOR_TOSHOST        3

/* ICMP codes for type == Time Exceeded.                                    */
#define TTL_ZERO                 0
#define REASS_TIMEOUT            1

/* ICMP codes for type == Parameter Problem.                                */
#define IP_HDR_BAD               0
#define MISSING_OPT              1

/* Skip remaining lines of current packet.  Note that this causes a         */
/* longjmp(), so a succeeding "return" from a function isn't needed.        */
#define nextPkt()   for (dataLen = 0; ; ) (void)getPkt()
/* Display a separator line between packet decodes.                         */
#define prSep() \
printf( \
   "--------------------------------------" \
   "-------------------------------------\n" \
)


/* My own preferred basic data types -- amend per target machine.           */
typedef char boolean;
typedef float float4;
typedef double float8;
typedef char int1;
typedef short int2;
typedef int int4;
typedef unsigned char uint1;
typedef unsigned short uint2;
typedef unsigned int uint4;
typedef unsigned char uchar;


#if !defined(NOETHERNAMES)
// mr980118 ether_ntohost() and related functions aren't prototyped in the
// standard include directory.
extern struct ether_addr *ether_aton(char *);
extern int ether_ntohost(char *, struct ether_addr *);
#endif


int main(int, char **);


static boolean noBflag = FALSE;
static char *cookArgs[MAXCOOKARGS+1];
static boolean cookedFlag = FALSE;
static uint2 dataLen = 0;
static char *dfltCookArgs[] = {
   COOKER, "-enx", "-s10240", "-r-", (char *)NULL
};
static char dHostName[MAX_HOSTNAMELEN+1];
static char dIp[IP_ADDRLEN+1];         // Destination IP address
static int etherType;                  // mr971120 Protocol encoded in frame
static boolean fqdnFlag = FALSE;       // mr971021
static jmp_buf jmpBuf;
static boolean minHdrDecodeFlag = FALSE;
static boolean noDataFlag = FALSE;
#if !defined(NOETHERNAMES)
static boolean noEtherNames = FALSE;   // mr980118
#else
static boolean noEtherNames = TRUE;    // mr980303
#endif
static boolean noIpflag = FALSE;
static boolean noLinkFlag = FALSE;
static boolean noHostNames = FALSE;    // mr971021
static boolean noPortNames = FALSE;    // mr971021
static int nPktsShown = 0;
static char *off = "off,";             /* "off" in middle of list           */
static char *off_e = "off";            /* "off" at end of list              */
static char *on = "on, ";              /* "on" in middle of list            */
static char *on_e = "on";              /* "on" at end of list               */
static int pageWidth = NCOLS;
static char *pkt;
static boolean ppFlag = FALSE;
static uint1 proto;
static boolean sFlag = FALSE;
static boolean sbFlag = FALSE;
static char sHostName[MAX_HOSTNAMELEN+1];
static char sIp[IP_ADDRLEN+1];         // Source IP address
static boolean terseFlag = TRUE;
static boolean trackFlag = FALSE;
static char *unknown = "<unknown>";
static boolean verboseFlag = FALSE;    /* MikeRyan, 26may97                 */


static double canonTime(char *, double *, int *);
static char *deltaTime(double *, char *);
static void error(char *);
static char *etherAddr(char *, char **);
static char *etherName(char *, boolean);
static char *etherProto(char *, int *);
static void forkTcpdump(int, char **);
static uint1 getByte(char **);
static uint4 getLongWord(char **);
static char *getPkt(void);
static uint2 getWord(char **);
static char *hostName(char *, boolean);
static char *icmpCode(uint1, uint1);
static char *icmpExtras(uint1, uint1, char **, uint2 *);
static char *icmpType(uint1);
static char *ipAddr(char **);
static char *ipProto(uint1);
static char nextChar(char **);
static char *portName(uint2, char *, boolean);
static char *rmWSpace(char *);
static char *showArp(char *);
static char *showData(char *);
static char *showHdr(char *);
static char *showIcmp(char *);
static char *showIp(char *);
static void showPkt(char *);
static char *showRarp(char *);
static char *showTcp(char *);
static char *showUdp(char *);
static char *skip(char *, uint2);
static void usage(void);


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Return the canonical time (time in time units).                          */
/*                                                                          */
/****==========------------------------------------------------==========****/

static double canonTime (char *dayTime, double *multiplier, int *multLen) {

   double time;


   time = (double)atoi(dayTime) * 60 * 60;
   dayTime += 3;

   time += (double)atoi(dayTime) * 60;
   dayTime += 3;

   time += (double)atoi(dayTime);
   dayTime += 3;

   // Time resolution differs between machines.  We guess the resolution by
   // looking at the length of the fractional part of the time stamp.
   // Rather than using pow(), which requires the maths library, we just
   // run a simple loop to produce the same result.  This is only done once,
   // so efficiency doesn't matter.
   if (nPktsShown == 1) {
      int i;
      *multLen = strlen(dayTime);
      for (i = 0, *multiplier = 1; i < *multLen; ++i) *multiplier *= 10;
   }

   return time * *multiplier + (double)atol(dayTime);

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Return the time difference between this and the previous packet.         */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *deltaTime (double *prevTime, char *time) {

   double currTime;
   double delta;
   static char deltaString[32];
   int hours;
   int mins;
   static double multiplier;
   static int multLen;                 // Length of multiplier in chars
   char *s;
   int secs;


   // The timestamp may not be a valid time (e.g. if tcpdump isn't producing
   // the input but, rather, some end-user script).  We need to increase the
   // strength of this validation someday :-)
   if (!isdigit(*time) || time[2] != ':' || time[5] != ':') return "";

   currTime = canonTime(time, &multiplier, &multLen);

   if (nPktsShown == 1) {
      *prevTime = currTime;            // Initialise on 1st packet
      return "";
   }

   delta = currTime - *prevTime;
   *prevTime = currTime;

   // Convert the delta time to daytime representation.
   // The subtractions from 'delta' simulate the % operator.  (Note: don't
   // change the value of 'multiplier', as it's set only on the 1st call to
   // canonTime()).
   hours = (int)(delta / (multiplier * 60 * 60));
   delta -= (double)hours * multiplier * 60 * 60;
   mins = (int)(delta / (multiplier * 60));
   delta -= (double)mins * multiplier * 60;
   secs = (int)(delta / multiplier);
   delta -= (double)secs * multiplier;
   (void)strcpy(deltaString, " (");
   s = &deltaString[2];
   (void)sprintf(s, "%02d:", hours);
   s += 3;
   (void)sprintf(s, "%02d:", mins);
   s += 3;
   (void)sprintf(s, "%d.", secs);
   while (*s) ++s;
   (void)sprintf(s, "%0*d", multLen, (int)delta);
   while (*s) ++s;
   *s++ = ')';
   *s = '\0';

   // Remove the hours and mins components if they're zero.
   s = deltaString + 2;                // Skip over " ("
   if ((hours=atoi(s)) == 0) {
      s += 3;
      if ((mins=atoi(s)) == 0) {
	 s += 3;
      }
   }
   bcopy(s, deltaString+2, strlen(s)+1);

   return deltaString;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Print an error message and exit.                                         */
/*                                                                          */
/****==========------------------------------------------------==========****/

static void error (char *msg) {

   fprintf(stderr, "***Error: %s\n", msg);
   exit(1);

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Print a formatted Ethernet address.                                      */
/* If pPkt is non-zero, we read the address from the packet stream in raw   */
/* hex format.                                                              */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *etherAddr (char *eAddr, char **pPkt) {

   uint1 byte;
   static char formatted[ETHER_ADDRLEN+1];
   int i;
   int j;


   // If non-zero, read the hex bytes from the packet stream.
   if (pPkt) {
      byte = getByte(pPkt); sprintf(formatted+0,  "%02X:", byte);
      byte = getByte(pPkt); sprintf(formatted+3,  "%02X:", byte);
      byte = getByte(pPkt); sprintf(formatted+6,  "%02X:", byte);
      byte = getByte(pPkt); sprintf(formatted+9,  "%02X:", byte);
      byte = getByte(pPkt); sprintf(formatted+12, "%02X:", byte);
      byte = getByte(pPkt); sprintf(formatted+15, "%02X",  byte);
   }
   else {
      // The address is already in ASCII form; just pad out.
      for (i = j = 0; i < 6; i++)
	 if (eAddr[1] == ':' || eAddr[1] == '\0') {   // mr980118
	    formatted[j++] = '0';
	    formatted[j++] = toupper(eAddr[0]);
	    formatted[j++] = ':';
	    eAddr += 2;
	 }
	 else {
	    formatted[j++] = toupper(eAddr[0]);
	    formatted[j++] = toupper(eAddr[1]);
	    formatted[j++] = ':';
	    eAddr += 3;
	 }
      formatted[j-1] = '\0';
   }

   return formatted;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* If noEtherNames is true, then if returnEtherAddr is true return the      */
/*    Ethernet address, otherwise return the value of 'unknown';            */
/* otherwise, if there is no matching Ethernet name, then if                */
/*    returnEtherAddr is true, return the Ethernet address, otherwise       */
/*    return 'unknown';                                                     */
/* otherwise, return the Ethernet name.                                     */
/*                                                                          */
/* CURRENTLY, THIS FUNCTION USES LIBRARY CALLS PARTICULAR TO FREEBSD 2.1+.  */
/*                                                                          */
/*                                                                          */
/* mr980118                                                                 */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *etherName (char *etherAddr, boolean returnEtherAddr) {

#if defined(NOETHERNAMES)
   return returnEtherAddr? etherAddr: "no name";
#else
   struct ether_addr *e;
   static char name[MAX_HOSTNAMELEN+1];


   if (noEtherNames) return returnEtherAddr? etherAddr: unknown;

   if (!(e=ether_aton(etherAddr))) error("Badly formatted Ethernet address");

   if (ether_ntohost(name, e) != 0)
      return returnEtherAddr? etherAddr: unknown;

   return name;
#endif

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Return the type of protocol encapsulated in the Ethernet frame and also  */
/* a string representing that value.                                        */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *etherProto (char *typeStr, int *pType) {

   int type;


   (void)sscanf(typeStr, "%x", &type);
   if (pType) *pType = type;

   if (type == ETHER_PROTO_IP)
      return "IP";
   elif (type == ETHER_PROTO_ARP)
      return "ARP";
   elif (type == ETHER_PROTO_RARP)
      return "RARP";
   else
      return typeStr;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Run tcpdump to pre-process the trace file.                               */
/*                                                                          */
/****==========------------------------------------------------==========****/

static void forkTcpdump (int argc, char **argv) {

   int fd[2];
   int i;
   pid_t pid;


   /* Required "tcpdump" flags.                                             */
   i = 0;
   while (dfltCookArgs[i]) {
      cookArgs[i] = dfltCookArgs[i];
      i++;
   }
   while (argc-- > 0) {
      if (i >= MAXCOOKARGS) error("Too many expressions");
      cookArgs[i++] = *argv++;
   }
   cookArgs[i] = (char *)NULL;

   /* Fork tcpdump to cook our input.                                       */
   if (pipe(fd)) error("pipe() failed");
   if ((pid=fork()) < 0) error("fork() failed");
   if (pid == 0) {
      (void)close(1);
      if (dup(fd[1]) != 1) error("dup() failed");
      (void)close(fd[0]);
      (void)close(fd[1]);
      execvp(COOKER, cookArgs);
      error("execvp() failed");
   }

   (void)close(0);
   if (dup(fd[0]) != 0) error("dup() failed");
   (void)close(fd[0]);
   (void)close(fd[1]);

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Return the byte value and increment the pointer by sizeof(byte).         */
/*                                                                          */
/****==========------------------------------------------------==========****/

static uint1 getByte (char **pPkt) {

   char byte[1*2+1];                   /* ASCII representation of a byte    */
   unsigned int val;


   byte[0] = nextChar(pPkt);
   byte[1] = nextChar(pPkt);
   byte[2] = '\0';

   (void)sscanf(byte, "%x", &val);

   return (uint1)val;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Return the longword value and increment the pointer by sizeof(longWord). */
/*                                                                          */
/****==========------------------------------------------------==========****/

static uint4 getLongWord (char **pPkt) {

   char longWord[4*2+1];              /* ASCII representation of a longword */
   unsigned long val;


   longWord[0] = nextChar(pPkt);
   longWord[1] = nextChar(pPkt);
   longWord[2] = nextChar(pPkt);
   longWord[3] = nextChar(pPkt);
   longWord[4] = nextChar(pPkt);
   longWord[5] = nextChar(pPkt);
   longWord[6] = nextChar(pPkt);
   longWord[7] = nextChar(pPkt);
   longWord[8] = '\0';

   (void)sscanf(longWord, "%lx", &val);

   return (uint4)val;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Read in the next line of packet data.                                    */
/*                                                                          */
/* Set global pointer "pkt" to start of buffer containing the packet line.  */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *getPkt () {

   static boolean beenHereAlready = FALSE;
   static char pktBuf[MAXPKT+1];


   if (fgets(pktBuf, MAXPKT+1, stdin) == (char *)NULL) {
      if (nPktsShown > 0) prSep();
      exit(0);
   }

   /* Line without leading <tab> means start of new packet.                 */
   if (*pktBuf == '\t')
      return pkt = rmWSpace(pktBuf);
   elif (!beenHereAlready) {           /* setjmp() won't have been called   */
      beenHereAlready = TRUE;          /*  before reading 1st packet        */
      return pkt = pktBuf;
   }
   else {
      if (dataLen > 0)
         printf("\n\t<*** Rest of data missing from packet dump ***>\n");
      pkt = pktBuf;
      longjmp(jmpBuf, 1);
   }

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Return the word value and increment the pointer by sizeof(word).         */
/*                                                                          */
/****==========------------------------------------------------==========****/

static uint2 getWord (char **pPkt) {

   char word[2*2+1];                   /* ASCII representation of a word    */
   unsigned int val;


   word[0] = nextChar(pPkt);
   word[1] = nextChar(pPkt);
   word[2] = nextChar(pPkt);
   word[3] = nextChar(pPkt);
   word[4] = '\0';

   (void)sscanf(word, "%x", &val);

   return (uint2)val;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* If noHostNames is true, then if returnIpAddr is true return the IP       */
/*    address, otherwise return the value of 'unknown';                     */
/* otherwise, if there is no matching hostname, then if returnIpAddr is     */
/*    true, return the IP address, otherwise return 'unknown';              */
/* otherwise, if fqdnFlag is true, return the fully-qualified hostname;     */
/* otherwise, return the short hostname.                                    */
/*                                                                          */
/*                                                                          */
/* mr971021                                                                 */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *hostName (char *ipAddr, boolean returnIpAddr) {

   struct hostent *h;
   static char name[MAX_HOSTNAMELEN+1];
   struct in_addr inAddr;
   char *s;


   if (noHostNames) return returnIpAddr? ipAddr: unknown;

   inAddr.s_addr = inet_addr(ipAddr);
   if (!(h = gethostbyaddr((char *)&inAddr, sizeof(inAddr), AF_INET)))
      return returnIpAddr? ipAddr: unknown;
   if (strlen(h->h_name) > MAX_HOSTNAMELEN) error("Hostname too long");
   (void)strcpy(name, h->h_name);

   if (!fqdnFlag) {
      s = name;
      while (*s && *s != '.') ++s;
      *s = '\0';
   }

   return name;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Print the code relating to the ICMP type.                                */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *icmpCode (uint1 type, uint1 code) {

   char *bad;
   char *descr;


   bad = "<*** CORRUPT ***>";
   descr = (char *)NULL;

   switch (type) {
    case ECHO_REPLY:
      switch (code) {
       case 0:                                                          break;
       default:                descr = bad;                             break;
      }
      break;
    case DST_UNREACH:
      switch (code) {
       case NET_UNREACH:       descr = "network-unreachable";           break;
       case HOST_UNREACH:      descr = "host-unreachable";              break;
       case PROTO_UNREACH:     descr = "protocol-unreachable";          break;
       case PORT_UNREACH:      descr = "port-unreachable";              break;
       case DF_SET:            descr = "frag-needed-but-DF-set";        break;
       case SRCROUTE_FAILED:   descr = "source-route-failed";           break;
       case DSTNET_UNKNOWN:    descr = "destination-network-unknown";   break;
       case DSTHOST_UNKNOWN:   descr = "destination-host-unknown";      break;
       case SRCHOST_ISOLATED:  descr = "source-host-isolated";          break;
       case DSTNET_PROHIB:     descr = "dest-net-admin-prohibited";     break;
       case DSTHOST_PROHIB:    descr = "dest-host-admin-prohibited";    break;
       case NET_UNREACH_TOS:   descr = "network-unreachable-for-TOS";   break;
       case HOST_UNREACH_TOS:  descr = "host-unreachable-for-TOS";      break;
       case COMM_PROHIB:       descr = "trafffic-prohibited-by-filter"; break;
       case HOST_PREC_VIOL:    descr = "host-precedence-violation";     break;
       case PREC_CUTOFF:       descr = "precedence-cutoff-in-effect";   break;
       default:                descr = bad;                             break;
      }
      break;
    case SRC_QUENCH:
      switch (code) {
       case 0:                                                          break;
       default:                descr = bad;                             break;
      }
      break;
    case REDIRECT:
      switch (code) {
       case REDIR_FOR_NET:     descr = "route-wrong-for-network";       break;
       case REDIR_FOR_HOST:    descr = "route-wrong-for-host";          break;
       case REDIR_FOR_TOSNET:  descr = "route-wrong-for-TOS-and-net";   break;
       case REDIR_FOR_TOSHOST: descr = "route-wrong-for-TOS-and-host";  break;
       default:                descr = bad;                             break;
      }
      break;
    case ECHO_REQ:
      switch (code) {
       case 0:                                                          break;
       default:                descr = bad;                             break;
      }
      break;
    case ROUTER_AD:
      switch (code) {
       case 0:                                                          break;
       default:                descr = bad;                             break;
      }
      break;
    case ROUTER_SOL:
      switch (code) {
       case 0:                                                          break;
       default:                descr = bad;                             break;
      }
      break;
    case TIME_EXCEED:
      switch (code) {
       case TTL_ZERO:          descr = "TTL-reached-zero";              break;
       case REASS_TIMEOUT:     descr = "reassembly-timer-expired";      break;
       default:                descr = bad;                             break;
      }
      break;
    case PARAM_PROB:
      switch (code) {
       case IP_HDR_BAD:        descr = "IP-header-bad";                 break;
       case MISSING_OPT:       descr = "required-option-is-missing";    break;
       default:                descr = bad;                             break;
      }
      break;
    case TIME_REQ:
      switch (code) {
       case 0:                                                          break;
       default:                descr = bad;                             break;
      }
      break;
    case TIME_REPLY:
      switch (code) {
       case 0:                                                          break;
       default:                descr = bad;                             break;
      }
      break;
    case INFO_REQ:
      switch (code) {
       case 0:                                                          break;
       default:                descr = bad;                             break;
      }
      break;
    case INFO_REPLY:
      switch (code) {
       case 0:                                                          break;
       default:                descr = bad;                             break;
      }
      break;
    case MASK_REQ:
      switch (code) {
       case 0:                                                          break;
       default:                descr = bad;                             break;
      }
      break;
    case MASK_REPLY:
      switch (code) {
       case 0:                                                          break;
       default:                descr = bad;                             break;
      }
      break;
    default:
      break;
   }

   return descr;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Some ICMP messages contain additional information.                       */
/* Return this information if it's available, NULL otherwise.               */
/*                                                                          */
/* On entry, *pPkt points at the 1st byte following the ICMP checksum.      */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *icmpExtras (
   uint1 type, uint1 code, char **pPkt, uint2 *nSkipped
) {

   char *dfSetText1 = "My next-hop MTU is ";
   uint2 dstPort;
   boolean haveInfo;
#if defined(INFOBUF)
#error "INFOBUF already defined"
#endif
#define INFOBUF 255
   static char info[INFOBUF+1];
   int ipHdrLen;
   uint2 mtu;
   char *portUnreachText1 = "Port ";
   char *portUnreachText2 = " is unreachable";
   char *redirectText1 = "Use router ";
   char *redirectText2 = " instead";
   char *s;
   uint1 transportProto;


   haveInfo = FALSE;

   // We're only interested in the ones that have extra information.
   switch (type) {
    case DST_UNREACH:
      switch (code) {
       case PORT_UNREACH:
	 *pPkt = skip(*pPkt, 4); *nSkipped += 4;   // Skip over MBZ field
	 ipHdrLen = (int)getByte(pPkt); *nSkipped += 1;
	 ipHdrLen = (ipHdrLen & 0x0F) * 4;
	 *pPkt = skip(*pPkt, 8); *nSkipped += 8;   // Skip to protocol field
	 transportProto = getByte(pPkt); *nSkipped += 1;
	 // Subtract ten because we've already processed these bytes.
	 *pPkt = skip(*pPkt, ipHdrLen-1-1-8); *nSkipped += ipHdrLen-1-1-8;
	 *pPkt = skip(*pPkt, 2); *nSkipped += 2;   // Skip past source port
	 dstPort = getWord(pPkt); *nSkipped += sizeof dstPort;
	 switch (transportProto) {
	  case TCP: s = "tcp"; break;
	  case UDP: s = "udp"; break;
	  default:  error("IP protocol field != TCP or UDP");
	 }
	 s = portName(dstPort, s, TRUE);
	 if (strlen(portUnreachText1)+strlen(portUnreachText2)+strlen(s) >
	     INFOBUF) error("INFOBUF too small");
	 (void)strcpy(info, portUnreachText1);
	 (void)strcat(info, s);
	 (void)strcat(info, portUnreachText2);
	 haveInfo = TRUE;
	 break;
       case DF_SET:
         // If the router sending the ICMP is properly playing its part in
	 // PMTU discovery, the high word will contain the next-hop MTU.
	 *pPkt = skip(*pPkt, 2); *nSkipped += 2;
         mtu = getWord(pPkt); *nSkipped += sizeof(mtu);
         if (mtu) {
	    (void)strcpy(info, dfSetText1);
	    (void)sprintf(info+strlen(info), "%d", mtu);
	    haveInfo = TRUE;
         }
	 break;
      }
      break;
    case REDIRECT:
      s = hostName(ipAddr(pPkt), TRUE); *nSkipped += 4;
      if (strlen(redirectText1)+strlen(redirectText2)+strlen(s) > INFOBUF)
	 error("INFOBUF too small");
      (void)strcpy(info, redirectText1);
      (void)strcat(info, s);
      (void)strcat(info, redirectText2);
      haveInfo = TRUE;
      break;
    case TIME_REQ:
      break;
    case TIME_REPLY:
      break;
    case INFO_REQ:
      break;
    case INFO_REPLY:
      break;
    case MASK_REQ:
      break;
    case MASK_REPLY:
      break;
   }

   return haveInfo? info: (char *)NULL;
#undef INFOBUF

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Print the type of ICMP packet.                                           */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *icmpType (uint1 type) {

   char *descr;


   switch (type) {
    case ECHO_REPLY:  descr = "echo-reply";              break;
    case DST_UNREACH: descr = "destination-unreachable"; break;
    case SRC_QUENCH:  descr = "source-quench";           break;
    case REDIRECT:    descr = "redirect";                break;
    case ECHO_REQ:    descr = "echo-request";            break;
    case ROUTER_AD:   descr = "router-advertisement";    break;
    case ROUTER_SOL:  descr = "router-solicitation";     break;
    case TIME_EXCEED: descr = "time-exceeded";           break;
    case PARAM_PROB:  descr = "parameter-problem";       break;
    case TIME_REQ:    descr = "timestamp-request";       break;
    case TIME_REPLY:  descr = "timestamp-reply";         break;
    case INFO_REQ:    descr = "information-request";     break;
    case INFO_REPLY:  descr = "information-reply";       break;
    case MASK_REQ:    descr = "address-mask-request";    break;
    case MASK_REPLY:  descr = "address-mask-reply";      break;
    default:          descr = unknown;                   break;
   }

   return descr;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Print the IP address in dotted-quad.                                     */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *ipAddr (char **pPkt) {

   static char addr[IP_ADDRLEN+1];
   uint2 byte1;
   uint2 byte2;
   uint2 byte3;
   uint2 byte4;


   /* We don't use inet_ntoa() because it wants a socket structure.         */
   byte1 = (uint2)getByte(pPkt);
   byte2 = (uint2)getByte(pPkt);
   byte3 = (uint2)getByte(pPkt);
   byte4 = (uint2)getByte(pPkt);
   (void)sprintf(addr, "%d.%d.%d.%d", byte1, byte2, byte3, byte4);

   return addr;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Print the type of protocol encapsulated in the IP datagram.              */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *ipProto (uint1 code) {

   char *name;


   /* A simple table won't do, as the codes aren't contiguous.               */
   switch (code) {
    case IP:
       name = "IP"; break;
    case ICMP:
       name = "ICMP"; break;
    case IGMP:
       name = "IGMP"; break;
    case GGP:
       name = "GGP"; break;
    case IPENCAP:
       name = "IPENCAP"; break;
    case ST:
       name = "ST"; break;
    case TCP:
       name = "TCP"; break;
    case EGP:
       name = "EGP"; break;
    case PUP:
       name = "PUP"; break;
    case UDP:
       name = "UDP"; break;
    case HMP:
       name = "HMP"; break;
    case XNSIDP:
       name = "XNSIDP"; break;
    case RDP:
       name = "RDP"; break;
    case ISOTP4:
       name = "ISOTP4"; break;
    case XTP:
       name = "XTP"; break;
    case IDPRCMTP:
       name = "IDPRCMTP"; break;
    case RSVP:
       name = "RSVP"; break;
    case VMTP:
       name = "VMTP"; break;
    case OSPF:
       name = "OSPF"; break;
    case IPIP:
       name = "IPIP"; break;
    case ENCAP:
       name = "ENCAP"; break;
    default:
       name = unknown; break;
   }

   return name;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Decode a "tcpdump" savefile.                                             */
/*                                                                          */
/****==========------------------------------------------------==========****/

int main (int argc, char **argv) {

   /* Command line options.                                                 */
   while (--argc > 0 && **++argv == '-')
      if (strcmp(*argv, "-minHdrDecode") == 0)
         minHdrDecodeFlag = noLinkFlag = noIpflag = TRUE;
      elif (strcmp(*argv, "-s") == 0) sFlag = TRUE;
      elif (strcmp(*argv, "-b") == 0) noBflag = TRUE;
      elif (strcmp(*argv, "-sb") == 0) sbFlag = TRUE;
      elif (strcmp(*argv, "-terse") == 0) terseFlag = TRUE;
      elif (strcmp(*argv, "-verbose") == 0) {
	 verboseFlag = TRUE;
	 terseFlag = FALSE;
      }
      elif (strcmp(*argv, "-track") == 0) trackFlag = TRUE;
      elif (strcmp(*argv, "-noData") == 0) noDataFlag = TRUE;
      elif (strcmp(*argv, "-noLink") == 0) noLinkFlag = TRUE;
      elif (strcmp(*argv, "-noIp") == 0) noIpflag = TRUE;
      elif (strcmp(*argv, "-noHostNames") == 0) noHostNames = TRUE;
#if !defined(NOETHERNAMES)
      elif (strcmp(*argv, "-noEtherNames") == 0) noEtherNames = TRUE;
#endif
      elif (strcmp(*argv, "-noPortNames") == 0) noPortNames = TRUE;
      elif (strcmp(*argv, "-fqdn") == 0) fqdnFlag = TRUE;
      elif (strcmp(*argv, "-cooked") == 0) cookedFlag = TRUE;
      elif (strcmp(*argv, "-pp") == 0) ppFlag = TRUE;
      elif (strcmp(*argv, "-h") == 0) usage();
      elif (strcmp(*argv, "-w") == 0) {
         if (--argc <= 0) error("-w needs a numeric argument");
         if ((pageWidth=atoi(*++argv)) < 1) error("-w value too small");
      }
      else error("Unknown command line flag");

   if (!cookedFlag)
      forkTcpdump(argc, argv);
   elif (argc != 0)
      fprintf(stderr, "input is cooked -- ignoring tcpdump expressions\n");

   pkt = getPkt();
   for ( ; ; ) if (!setjmp(jmpBuf)) showPkt(pkt);

   exit(0);
   return 0;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Return the next character in the packet buffer.                          */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char nextChar (char **pPkt) {

   if (!**pPkt) *pPkt = getPkt();

   return *(*pPkt)++;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* If noPortNames is true, then if wantNumber is true, return the port      */
/*    number, otherwise return the value of 'unknown';                      */
/* otherwise, if the port has a name return that name;                      */
/* otherwise, if wantNumber is true return the port number;                 */
/* otherwise, return the value of 'unknown'.                                */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *portName (uint2 port, char *proto, boolean wantNumber) {

   char *name;
   static char number[6];
   struct servent *service;            /* Doesn't need to be static         */


   // We could tighten this code up a little, but don't want to call
   // getservbyport() unless necessary.
   if (noPortNames)
      if (!wantNumber)
	 name = unknown;
      else {
	 (void)sprintf(number, "%d", port);
	 name = number;
      }
   /* The crappy manpage doesn't say the port must be in net byte order.    */
   elif ( (service = getservbyport((int)htons(port), proto)) )
      name = service->s_name;
   elif (!wantNumber)
      name = unknown;
   else {
      (void)sprintf(number, "%u", port);
      name = number;
   }

   if (strlen(name) > MAX_PORTNAMELEN) error("Port name too long");

   return name;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Remove whitespace from the buffer.                                       */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *rmWSpace (reg char *pktBuf) {

   static char cleanPkt[MAXPKT+1];
   reg char *cleanBuf;


   cleanBuf = cleanPkt;
   while (*pktBuf) {
      if (!isspace(*pktBuf)) *cleanBuf++ = *pktBuf;
      pktBuf++;
   }
   *cleanBuf = '\0';

   return cleanPkt;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Decode the ARP data.                                                     */
/*                                                                          */
/* This function and showRarp() could be merged into one.                   */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *showArp (char *p) {

   uint1 hLen;
   uint2 hType;
   uint2 op;
   uint1 pLen;
   uint2 pType;
   char sEtherAddr[ETHER_ADDRLEN+1];   // Sender Ethernet address
   char sEtherName[MAX_HOSTNAMELEN+1]; // Sender Ethernet name
   char sHostName[MAX_HOSTNAMELEN+1];  // Sender hostname
   char sIpAddr[IP_ADDRLEN+1];         // Sender IP address
   char tEtherAddr[ETHER_ADDRLEN+1];   // Target Ethernet address
   char tEtherName[MAX_HOSTNAMELEN+1]; // Target Ethernet name
   char tHostName[MAX_HOSTNAMELEN+1];  // Target hostname
   char tIpAddr[IP_ADDRLEN+1];         // Target IP address
   uint2 nSkipped;


   hType      = getWord(&p); nSkipped = sizeof(hType);
   pType      = getWord(&p); nSkipped = sizeof(pType);
   hLen       = getByte(&p); nSkipped = sizeof(hLen);
   pLen       = getByte(&p); nSkipped = sizeof(pLen);
   op         = getWord(&p); nSkipped = sizeof(op);
   (void)strcpy(sEtherAddr, etherAddr(0, &p)); nSkipped += 6;
   (void)strcpy(sIpAddr, ipAddr(&p));          nSkipped += 4;
   (void)strcpy(tEtherAddr, etherAddr(0, &p)); nSkipped += 6;
   (void)strcpy(tIpAddr, ipAddr(&p));          nSkipped += 4;

   (void)strcpy(sEtherName, etherName(sEtherAddr, TRUE));
   (void)strcpy(tEtherName, etherName(tEtherAddr, TRUE));
   (void)strcpy(sHostName, hostName(sIpAddr, TRUE));
   (void)strcpy(tHostName, hostName(tIpAddr, TRUE));

   if (minHdrDecodeFlag) {
      switch (op) {
       case ARP_REQ:
	 printf(
	    "%s (%s) asks where is %s\n",
	    sHostName, sEtherName, tHostName
	 );
	 break;
       case ARP_RSP:
	 printf(
	    "%s says to %s it's at %s\n",
	    sHostName, tHostName, sEtherName
	 );
	 break;
      }
      return p;
   }

   if (terseFlag) {
      printf(
	 "ARP:\thtype=%s ptype=%s hlen=%d plen=%d op=%s\n",
	 hType == ARP_HW_ETHER? "Ethernet": unknown,
	 pType == ARP_PROTO_IP? "IP": unknown,
	 hLen, pLen, op == ARP_REQ? "request": "response"
      );
      printf(
	 "\tsender-MAC-addr=%s sender-IP-address=%s\n",
	 sEtherName, sHostName
      );
      printf(
	 "\ttarget-MAC-addr=%s target-IP-address=%s\n",
	 tEtherName, tHostName
      );
   }

   else {
      printf("ARP Header\n");
      printf(
	 "\tHardware Type:\t\t\t%s\n",
	 hType == ARP_HW_ETHER? "Ethernet": unknown
      );
      printf(
	 "\tProtocol Type:\t\t\t%s\n",
	 pType == ARP_PROTO_IP? "IP": unknown
      );
      printf("\tHardware Address Length:\t%d bytes\n", hLen);
      printf("\tProtocol Address Length:\t%d bytes\n", pLen);
      printf(
	 "\tOperation:\t\t\tARP %s\n",
	 op == ARP_REQ? "request": "response"
      );
      printf("\tSender Hardware Address:\t%s", sEtherAddr);
      if (!noEtherNames) printf(" (%s)", etherName(sEtherAddr, FALSE));
      printf("\n\tSender IP Address:\t\t%s", sIpAddr);
      if (!noHostNames) printf(" (%s)", hostName(sIpAddr, FALSE));
      printf("\n\tTarget Hardware Address:\t%s", tEtherAddr);
      if (!noEtherNames) printf(" (%s)", etherName(tEtherAddr, FALSE));
      printf("\n\tTarget IP Address:\t\t%s", tIpAddr);
      if (!noHostNames) printf(" (%s)", hostName(tIpAddr, FALSE));
      putchar('\n');
   }

   return p;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Decode the TCP/UDP data.                                                 */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *showData (char *p) {

   uint1 byte;
   int col;
   char *descr;


   if (minHdrDecodeFlag)
      putchar('\t');
   elif (terseFlag)
      printf("DATA:\t");
   else {
      switch (proto) {
       case TCP:  descr = "TCP";   break;
       case UDP:  descr = "UDP";   break;
       case ICMP: descr = "ICMP";  break;
       default:   descr = unknown; break;
      }
      printf("%s Data\n\t", descr);
   }
   if (noDataFlag) {
      uint2 ndatabytes = dataLen;
      dataLen = 0;
      printf("%d bytes\n", ndatabytes);
      return skip(p, ndatabytes);
   }

   if (dataLen == 0) {
      printf("<No data>\n");
      return p;
   }

   switch (noBflag) {
    case FALSE:
      for (col = 1; dataLen > 0; dataLen--, col++) {
         byte = getByte(&p);
         if (byte == '\n') {
            putchar('\n');
            byte = '\t';
            col = 0;
         }
         elif (col > pageWidth) {
            printf("%s\n\t", sbFlag? "<br>": "");
            col = 1;
         }
         if (byte != '\t' && byte != '\n' && !isprint(byte)) byte = '.';
         putchar(byte);
      }
      break;
    case TRUE:
      for ( ; dataLen > 0; dataLen--) {
         byte = getByte(&p);
         if (byte == '\n') {
            putchar('\n');
            byte = '\t';
         }
         if (byte != '\t' && byte != '\n' && !isprint(byte)) byte = '.';
         putchar(byte);
      }
      break;
    default:
      error("Tri-valued boolean!");
   }
   putchar('\n');

   return p;
   
}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Decode the packet header.                                                */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *showHdr (char *p) {

   char eFrom[ETHER_ADDRLEN+1];        /* Source Ethernet address           */
   char eFromName[MAX_HOSTNAMELEN+1];  // Sender Ethernet name
   char eTo[ETHER_ADDRLEN+1];          /* Destination Ethernet address      */
   char eToName[MAX_HOSTNAMELEN+1];    // Target Ethernet name
   char eType[20];                     /* Ethernet type (decoded to ASCII)  */
   static double prevTime;             // Timestamp of previous packet
   char time[16];                      /* Packet timestamp                  */


   if (ppFlag) {
      (void)sscanf(p, "%s", time);
      etherType = ETHER_PROTO_IP;      /* tcpdump doesn't supply link type  */
      if (!noLinkFlag) {
         if (terseFlag)
	    printf("TIME:\t%s%s\n", time, deltaTime(&prevTime, time));
         else
	    printf(
	       "\tTimestamp:\t\t\t%s%s\n", time, deltaTime(&prevTime, time)
	    );
	}
      return getPkt();
   }

   (void)sscanf(p, "%s %s %s %s", time, eFrom, eTo, eType);
   (void)etherProto(eType, &etherType);

   (void)strcpy(eFrom, etherAddr(eFrom, 0));
   (void)strcpy(eFromName, etherName(eFrom, TRUE));
   (void)strcpy(eTo, etherAddr(eTo, 0));
   (void)strcpy(eToName, etherName(eTo, TRUE));

   if (!noLinkFlag) {
      if (terseFlag) {
         printf("TIME:\t%s%s\n", time, deltaTime(&prevTime, time));
         printf(
	    "LINK:\t%s -> %s type=%s\n",
	    eFromName, eToName, etherProto(eType, 0)
	 );
      }
      else {
         printf("\tTimestamp:\t\t\t%s%s\n", time, deltaTime(&prevTime, time));
         printf("\tSource Ethernet Address:\t%s", eFrom);
         if (!noEtherNames) printf(" (%s)", etherName(eFrom, FALSE));
         printf("\n\tDestination Ethernet Address:\t%s", eTo);
         if (!noEtherNames) printf(" (%s)", etherName(eTo, FALSE));
         printf("\n\tEncapsulated Protocol:\t\t%s\n", etherProto(eType, 0));
      }
   }

   return getPkt();

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Decode the ICMP header.                                                  */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *showIcmp (char *p) {

   uint2 cksum;
   uint1 code;
   char *extraInfo;
   char *msgType;
   uint2 nSkipped;
   uint1 type;
   char *why;


   type  = getByte(&p); nSkipped  = sizeof(type);
   code  = getByte(&p); nSkipped += sizeof(code);
   cksum = getWord(&p); nSkipped += sizeof(cksum);

   msgType = icmpType(type);
   why = icmpCode(type, code);
   extraInfo = icmpExtras(type, code, &p, &nSkipped);

   /* The length of the ICMP packet isn't recorded in the packet itself.    */
   dataLen -= nSkipped;

   if (minHdrDecodeFlag) {
      printf(
         "%s -> %s ICMP %s%s%s\n",
         sHostName, dHostName, msgType, why? " because ": "", why? why: ""
      );
      if (extraInfo) printf("\t%s\n", extraInfo);
      return p;                        /* Header is read; nothing to skip   */
   }

   if (terseFlag) {
      printf(
         "ICMP:\t%s%s%s cksum=%04X\n",
         msgType, why? " because ": "", why? why: "", cksum
      );
      if (extraInfo) printf("\t%s\n", extraInfo);
   }
   else {
      printf("ICMP Header\n");
      printf(
         "\tType:\t\t\t\t%s%s%s\n",
         msgType, why? "\n\tBecause:\t\t\t": "", why? why: ""
      );
      if (extraInfo) printf("\tAdditional Information:\t\t%s\n", extraInfo);
      printf("\tChecksum:\t\t\t0x%04X\n", cksum);
   }

   return p;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Decode the IP header.                                                    */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *showIp (char *p) {

   uint2 cksum;
   uint2 dgramLen;
   uint2 flags;
   uint2 hLen;
   uint2 id;
   uint2 nSkipped;
   uint1 servType;
   uint1 ttl;
   uint1 ver;


   ver = getByte(&p); nSkipped  = sizeof(ver);
   if ((ver & 0xF0) != 0x40) {
      if (terseFlag) printf("IP:\tnot v4\n");
      else
         printf(
            "IP Header\n\t<Not an IPv4 datagram (ver=%d)>\n",
            (ver & 0xF0) >> 4
         );
      nextPkt();
   }
   servType = getByte(&p);        nSkipped += sizeof(servType);
   dgramLen = getWord(&p);        nSkipped += sizeof(dgramLen);
   id       = getWord(&p);        nSkipped += sizeof(id);
   flags    = getWord(&p);        nSkipped += sizeof(flags);
   ttl      = getByte(&p);        nSkipped += sizeof(ttl);
   proto    = getByte(&p);        nSkipped += sizeof(proto);
   cksum    = getWord(&p);        nSkipped += sizeof(cksum);
   (void)strcpy(sIp, ipAddr(&p)); nSkipped += 4;
   (void)strcpy(dIp, ipAddr(&p)); nSkipped += 4;
   hLen     = (ver & 0x0F) * 4;
   dataLen  = dgramLen - hLen;

   (void)strcpy(sHostName, hostName(sIp, TRUE));
   (void)strcpy(dHostName, hostName(dIp, TRUE));

   if (noIpflag) return skip(p, hLen - nSkipped);

   printf("%s", terseFlag? "  IP:\t": "IP Header\n");

   if (terseFlag) {
      printf(
         "%s -> %s hlen=%d TOS=%02X dgramlen=%d id=%04X\n",
         sHostName, dHostName, hLen, (uint2)servType, dgramLen, id
      );
      printf(
         "\tMF/DF=%s/%s frag=%d TTL=%d proto=%s cksum=%04X\n",
         (flags & MF) == MF? "1": "0", (flags & DF) == DF? "1": "0",
         flags & FRAGOFF, ttl, ipProto(proto), cksum
      );
   }

   else {
      printf("\tVersion:\t\t\t4\n\tHeader Length:\t\t\t%d bytes\n", hLen);
      printf("\tService Type:\t\t\t0x%02X\n", (uint2)servType);
      printf("\tDatagram Length:\t\t%d bytes\n", dgramLen);
      printf("\tIdentification:\t\t\t0x%04X\n", id);
      printf(
         "\tFlags:\t\t\t\tMF=%s DF=%s\n",
         (flags & MF) == MF? on: off, (flags & DF) == DF? on_e: off_e
      );
      printf("\tFragment Offset:\t\t%d\n", flags & FRAGOFF);
      printf("\tTTL:\t\t\t\t%d\n", ttl);
      printf("\tEncapsulated Protocol:\t\t%s\n", ipProto(proto));
      printf("\tHeader Checksum:\t\t0x%04X\n", cksum);
      printf("\tSource IP Address:\t\t%s", sIp);
      if (!noHostNames) printf(" (%s)", hostName(sIp, FALSE));
      printf("\n\tDestination IP Address:\t\t%s", dIp);
      if (!noHostNames) printf(" (%s)", hostName(dIp, FALSE));
      putchar('\n');
   }

   if (hLen > IPHDRLEN) {
      if (!terseFlag) printf("\t<Options not displayed>\n");
      p = skip(p, hLen - IPHDRLEN);
   }

   return p;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Decode the packet chunk in the buffer.                                   */
/*                                                                          */
/****==========------------------------------------------------==========****/

static void showPkt (reg char *p) {

   char *warnMsg = "<*** No decode support for encapsulated protocol ***>";


   prSep();
   printf("Packet %d\n", ++nPktsShown);

   p = showHdr(p);

   switch (etherType) {
    case ETHER_PROTO_ARP:
      p = showArp(p);
      break;
    case ETHER_PROTO_RARP:
      p = showRarp(p);
      break;
    case ETHER_PROTO_IP:
      p = showIp(p);
      switch (proto) {
       case TCP:
	 p = showTcp(p);
	 p = showData(p);
	 break;
       case UDP:
	 p = showUdp(p);
	 p = showData(p);
	 break;
       case ICMP:
	 p = showIcmp(p);
	 p = showData(p);
	 break;
       default:
	 printf("\t%s\n", warnMsg);
	 nextPkt();                    /* Doesn't return                    */
      }
      break;
    default:
      if (!minHdrDecodeFlag) printf("\t%s\n", warnMsg);
      nextPkt();
      break;
   }

   /* "tcpdump" sometimes displays data at the end of a packet which, given */
   /* the recorded Datagram Length, don't belong to the packet.             */
   if (*p) {
      if (sFlag) printf("\t<*** Spurious data at end: \"%s\" ***>\n", p);
      nextPkt();
   }
   /* Note that if getPkt() returns here, then the line read isn't the      */
   /* start of a new packet, i.e. there's spurious data.                    */
   if ( (p = getPkt()) ) {
      if (sFlag) printf("\t<*** Spurious data at end: \"%s\" ***>\n", p);
      nextPkt();
   }

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Decode the RARP data.                                                    */
/*                                                                          */
/* This function and showArp() could be merged into one.                    */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *showRarp (char *p) {

   uint1 hLen;
   uint2 hType;
   uint2 op;
   uint1 pLen;
   uint2 pType;
   char sEtherAddr[ETHER_ADDRLEN+1];   // Sender Ethernet address
   char sEtherName[MAX_HOSTNAMELEN+1]; // Sender Ethernet name
   char sHostName[MAX_HOSTNAMELEN+1];  // Sender hostname
   char sIpAddr[IP_ADDRLEN+1];         // Sender IP address
   char tEtherAddr[ETHER_ADDRLEN+1];   // Target Ethernet address
   char tEtherName[MAX_HOSTNAMELEN+1]; // Target Ethernet name
   char tHostName[MAX_HOSTNAMELEN+1];  // Target hostname
   char tIpAddr[IP_ADDRLEN+1];         // Target IP address
   uint2 nSkipped;


   hType      = getWord(&p); nSkipped = sizeof(hType);
   pType      = getWord(&p); nSkipped = sizeof(pType);
   hLen       = getByte(&p); nSkipped = sizeof(hLen);
   pLen       = getByte(&p); nSkipped = sizeof(pLen);
   op         = getWord(&p); nSkipped = sizeof(op);
   (void)strcpy(sEtherAddr, etherAddr(0, &p)); nSkipped += 6;
   (void)strcpy(sIpAddr, ipAddr(&p));          nSkipped += 4;
   (void)strcpy(tEtherAddr, etherAddr(0, &p)); nSkipped += 6;
   (void)strcpy(tIpAddr, ipAddr(&p));          nSkipped += 4;

   (void)strcpy(sEtherName, etherName(sEtherAddr, TRUE));
   (void)strcpy(tEtherName, etherName(tEtherAddr, TRUE));
   (void)strcpy(sHostName, hostName(sIpAddr, TRUE));
   (void)strcpy(tHostName, hostName(tIpAddr, TRUE));

   if (minHdrDecodeFlag) {
      switch (op) {
       case RARP_REQ:
	 printf(
	    "%s asks for its %s address\n",
	    sEtherName, pType == ARP_PROTO_IP? "Ethernet": unknown
	 );
	 break;
       case RARP_RSP:
	 printf(
	    "%s says to %s its %s address is %s\n",
	    sHostName, tEtherName,
	    pType == ARP_PROTO_IP? "Ethernet": unknown, tHostName
	 );
	 break;
      }
      return p;
   }

   if (terseFlag) {
      printf(
	 "RARP:\thtype=%s ptype=%s hlen=%d plen=%d op=%s\n",
	 hType == ARP_HW_ETHER? "Ethernet": unknown,
	 pType == ARP_PROTO_IP? "IP": unknown,
	 hLen, pLen, op == RARP_REQ? "request": "response"
      );
      printf(
	 "\tsender-MAC-addr=%s sender-IP-address=%s\n",
	 sEtherName, sHostName
      );
      printf(
	 "\ttarget-MAC-addr=%s target-IP-address=%s\n",
	 tEtherName, tHostName
      );
   }

   else {
      printf("RARP Header\n");
      printf(
	 "\tHardware Type:\t\t\t%s\n",
	 hType == ARP_HW_ETHER? "Ethernet": unknown
      );
      printf(
	 "\tProtocol Type:\t\t\t%s\n",
	 pType == ARP_PROTO_IP? "IP": unknown
      );
      printf("\tHardware Address Length:\t%d bytes\n", hLen);
      printf("\tProtocol Address Length:\t%d bytes\n", pLen);
      printf(
	 "\tOperation:\t\t\tRARP %s\n",
	 op == RARP_REQ? "request": "response"
      );
      printf("\tSender Hardware Address:\t%s", sEtherAddr);
      if (!noEtherNames) printf(" (%s)", etherName(sEtherAddr, FALSE));
      printf("\n\tSender IP Address:\t\t%s", sIpAddr);
      if (!noHostNames) printf(" (%s)", hostName(sIpAddr, FALSE));
      printf("\n\tTarget Hardware Address:\t%s", tEtherAddr);
      if (!noEtherNames) printf(" (%s)", etherName(tEtherAddr, FALSE));
      printf("\n\tTarget IP Address:\t\t%s", tIpAddr);
      if (!noHostNames) printf(" (%s)", hostName(tIpAddr, FALSE));
      putchar('\n');
   }

   return p;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Decode the TCP header.                                                   */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *showTcp (char *p) {

   uint4 ack;
   uint2 advert;
   uint2 cksum;
   uint2 dPort;
   char dPortName[MAX_PORTNAMELEN+1];
   uint4 expect;
   uint2 flags;
   uint2 hLen;
   uint2 nSkipped;
   uint4 seq;
   uint2 sPort;
   char sPortName[MAX_PORTNAMELEN+1];
   uint2 urgPtr;


   sPort  = getWord(&p);     nSkipped  = sizeof(sPort);
   dPort  = getWord(&p);     nSkipped += sizeof(dPort);
   seq    = getLongWord(&p); nSkipped += sizeof(seq);
   ack    = getLongWord(&p); nSkipped += sizeof(ack);
   flags  = getWord(&p);     nSkipped += sizeof(flags);
   advert = getWord(&p);     nSkipped += sizeof(advert);
   cksum  = getWord(&p);     nSkipped += sizeof(cksum);
   urgPtr = getWord(&p);     nSkipped += sizeof(urgPtr);

   hLen = (flags >> 12 & 0x0F) * 4;
   dataLen -= hLen;

   (void)strcpy(sPortName, portName(sPort, "tcp", TRUE));
   (void)strcpy(dPortName, portName(dPort, "tcp", TRUE));

   if (minHdrDecodeFlag) {
      printf(
	 "%s.%s -> %s.%s over TCP\n",
	 sHostName, sPortName, dHostName, dPortName
      );
      return skip(p, hLen - nSkipped);
   }

   if (trackFlag) {
      expect = seq + dataLen;
      if ((flags & SYN) == SYN || (flags & FIN) == FIN) expect++;
   }

   if (terseFlag) {
      printf(
	 " TCP:\tport %s -> %s seq=%010lu", sPortName, dPortName, (u_long)seq
      );
      if (trackFlag) printf(" (expect=%010lu)", (u_long)expect);
      printf(" ack=%010lu\n", (u_long)ack);
      printf(
         "\thlen=%d (data=%u) UAPRSF=%s%s%s%s%s%s",
         hLen, dataLen,
         (flags & URG) == URG? "1": "0", (flags & ACK) == ACK? "1": "0",
         (flags & PSH) == PSH? "1": "0", (flags & RST) == RST? "1": "0",
         (flags & SYN) == SYN? "1": "0", (flags & FIN) == FIN? "1": "0"
      );
      printf(" wnd=%d cksum=%04X urg=%d\n", advert, cksum, urgPtr);
   }

   else {
      printf("TCP Header\n");
      printf("\tSource Port:\t\t\t%d", sPort);
      if (!noPortNames) printf(" (%s)", portName(sPort, "tcp", FALSE));
      printf("\n\tDestination Port:\t\t%d", dPort);
      if (!noPortNames) printf(" (%s)", portName(dPort, "tcp", FALSE));
      printf("\n\tSequence Number:\t\t%010lu\n", (u_long)seq);
      if (trackFlag) printf("\tExpect peer ACK:\t\t%010lu\n", (u_long)expect);
      printf("\tAcknowledgement Number:\t\t%010lu\n", (u_long)ack);
      printf("\tHeader Length:\t\t\t%d bytes (data=%u)\n", hLen, dataLen);
      printf(
         "\tFlags:%s%s%s%s%s%s\n%s%s%s%s%s%s\n",
         "\t\t\t\tURG=",   (flags & URG) == URG? on: off,
         " ACK=",          (flags & ACK) == ACK? on: off,
         " PSH=",          (flags & PSH) == PSH? on_e: off_e,
         "\t\t\t\t\tRST=", (flags & RST) == RST? on: off,
         " SYN=",          (flags & SYN) == SYN? on: off,
         " FIN=",          (flags & FIN) == FIN? on_e: off_e
      );
      printf("\tWindow Advertisement:\t\t%d bytes\n", advert);
      printf("\tChecksum:\t\t\t0x%04X\n", cksum);
      printf("\tUrgent Pointer:\t\t\t%d\n", urgPtr);
   }

   if (hLen > TCPHDRLEN) {
      if (!terseFlag) printf("\t<Options not displayed>\n");
      p = skip(p, hLen - TCPHDRLEN);
   }

   return p;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Decode the UDP header.                                                   */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *showUdp (char *p) {

   uint2 cksum;
   uint2 dgramLen;
   uint2 dPort;
   char dPortName[MAX_PORTNAMELEN+1];
   uint2 nSkipped;
   uint2 sPort;
   char sPortName[MAX_PORTNAMELEN+1];


   sPort    = getWord(&p); nSkipped  = sizeof(sPort);
   dPort    = getWord(&p); nSkipped += sizeof(dPort);
   dgramLen = getWord(&p); nSkipped += sizeof(dgramLen);
   cksum    = getWord(&p); nSkipped += sizeof(cksum);

   /* The size of the IP data field should equal the UDP packet length.     */
   if (dataLen != dgramLen) {
      printf("\t<*** Packet length corrupt ***>\n");
      nextPkt();                       /* Doesn't return                    */
   }
   dataLen -= UDPHDRLEN;

   (void)strcpy(sPortName, portName(sPort, "udp", TRUE));
   (void)strcpy(dPortName, portName(dPort, "udp", TRUE));

   if (minHdrDecodeFlag) {
      printf(
	 "%s.%s -> %s.%s over UDP\n",
	 sHostName, sPortName, dHostName, dPortName
      );
      return p;                        /* Header is read; nothing to skip   */
   }

   if (terseFlag)
      printf(
         " UDP:\tport %s -> %s hdr=%u data=%u\n",
         sPortName, dPortName, UDPHDRLEN, dataLen
      );
   else {
      printf("UDP Header\n");
      printf("\tSource Port:\t\t\t%d", sPort);
      if (!noPortNames) printf(" (%s)", portName(sPort, "udp", FALSE));
      printf("\n\tDestination Port:\t\t%d", dPort);
      if (!noPortNames) printf(" (%s)", portName(dPort, "udp", FALSE));
      printf(
         "\n\tDatagram Length:\t\t%u bytes (Header=%u, Data=%u)\n",
         dgramLen, UDPHDRLEN, dataLen
      );
      printf("\tChecksum:\t\t\t0x%04X\n", cksum);
   }

   return p;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Skip over un-interesting bytes.                                          */
/*                                                                          */
/****==========------------------------------------------------==========****/

static char *skip (char *p, uint2 nBytes) {

   for ( ; nBytes > 0; nBytes--) (void)getByte(&p);
   return p;

}


/****==========------------------------------------------------==========****/
/*                                                                          */
/* Give a summary of usage.                                                 */
/*                                                                          */
/****==========------------------------------------------------==========****/

static void usage () {

#if !defined(MAY_NOT_MODIFY)
   printf("\nCopyright (c) 1996, 1997, 1998 I.T. NetworX Ltd.  ");
   printf("All rights reserved.\n");
   printf("mailto:mike@NetworX.ie\n\n");
#endif
   printf("tcpshow -- decode a tcpdump(1) savefile, giving a fully\n");
   printf("           decoded display of Ethernet, ARP, RARP, IP, ICMP,\n");
   printf("           UDP and TCP headers and an ASCII display of\n");
   printf("           the application data.\n\n");
   printf("Version %4.2f\n\n", VERSION);
   printf("Usage: tcpshow [ options ... ] [ expr ]\n");
   printf("\nwhere options are as follows\n");
   printf("\t-b\t\tdo not break/wrap long lines\n");
   printf("\t-sb\t\tshow breaks (show where we broke a line)\n");
   printf("\t-w width\tset pagewidth to \"width\" columns (used by -b)\n");
   printf("\t-noLink\t\tdon't decode link header (Ethernet header)\n");
   printf("\t-noIp\t\tdon't decode IP header\n");
   printf("\t-noHostNames\tdon't map IP addresses to host names\n");
   printf("\t-fqdn\t\tshow host names as fully-qualified\n");
#if !defined(NOETHERNAMES)
   printf("\t-noEtherNames\tdon't map Ethernet addresses to host names\n");
#endif
   printf("\t-noPortNames\tdon't map port numbers to names\n");
   printf("\t-noData\t\tdon't show data (show headers only)\n");
   printf("\t-minHdrDecode\tshow only a minimal header decode\n");
   printf("\t-track\t\ttrack sequence numbers (show next-expected ACK)\n");
   printf("\t-terse\t\tshow header decode in compact format (default)\n");
   printf("\t-verbose\tshow header decode in expanded format\n");
   printf("\t-cooked\t\tdon't run tcpdump to pre-process the input\n");
   printf("\t-pp\t\tpoint-to-point link (no Ethernet header available)\n");
   printf("\t-s\t\tdisplay hex dump of spurious data at packet-end\n");
   printf("\t-h\t\tdisplay this help summary\n\n");
   printf("expr is a tcpdump(1) expression, and is only valid when ");
   printf("the -cooked\noption is not used.\n\n");
   printf("Input is from stdin, ");
   printf("which must be a raw tcpdump(1) data file (savefile),\n");
   printf("unless the -cooked option is used, in which case stdin ");
   printf("must be in the\nformat produced by tcpdump -lenx.\n\n");
   printf("Output is to stdout.\n\n");
   printf("tcpdump(1) must be on your PATH unless -cooked is used.\n\n");

   exit(0);

}
