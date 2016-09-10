/*
  LCAP:  Linux Kernel Capability Remover
  Copyright (C) 1999  spoon@ix.netcom.com
  Copyright (C) 2000  spoon@ix.netcom.com
  
  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA
*/

/* $Id: lcap.c,v 1.13 2001/03/05 22:53:27 spoon Exp $ */

#include <stdio.h>
#include <linux/capability.h>
#include <errno.h>
#include <string.h>
#include <getopt.h>
#include <stdlib.h>
#include <ctype.h>

#define PROC_CAP "/proc/sys/kernel/cap-bound"

#ifdef LIDS
  #define PROC_LIDS "/proc/sys/lids"
#endif

typedef __u32 kernel_cap_t;

#define CAP_FULL_SET (~0)
#define CAP_TO_MASK(flag) (1 << (flag))
#define cap_raise(cap, flag)  (cap |= CAP_TO_MASK(flag))
#define cap_lower(cap, flag)  (cap &= ~CAP_TO_MASK(flag))
#define cap_raised(cap, flag) (cap & CAP_TO_MASK(flag) & CAP_FULL_SET)

#ifdef LIDS
  #define lids_raise(lidsnum) lids_set(lidsnum, 1)
  #define lids_lower(lidsnum) lids_set(lidsnum, 0)
#endif

  static char *thecaps[] =
    {
    "CAP_CHOWN",            "chown(2)/chgrp(2)",
    "CAP_DAC_OVERRIDE",     "DAC access",
    "CAP_DAC_READ_SEARCH",  "DAC read",
    "CAP_FOWNER",           "owner ID not equal user ID",
    "CAP_FSETID",           "effective user ID not equal owner ID",
    "CAP_KILL",             "real/effective ID not equal process ID",
    "CAP_SETGID",           "setgid(2)",
    "CAP_SETUID",           "set*uid(2)",
    "CAP_SETPCAP",          "transfer capability",
    "CAP_LINUX_IMMUTABLE",  "immutable and append file attributes",
    "CAP_NET_BIND_SERVICE", "binding to ports below 1024",
    "CAP_NET_BROADCAST",    "broadcasting/listening to multicast",
    "CAP_NET_ADMIN",        "interface/firewall/routing changes",
    "CAP_NET_RAW",          "raw sockets",
    "CAP_IPC_LOCK",         "locking of shared memory segments",
    "CAP_IPC_OWNER",        "IPC ownership checks",
    "CAP_SYS_MODULE",       "insertion and removal of kernel modules",
    "CAP_SYS_RAWIO",        "ioperm(2)/iopl(2) access",
    "CAP_SYS_CHROOT",       "chroot(2)",
    "CAP_SYS_PTRACE",       "ptrace(2)",
    "CAP_SYS_PACCT",        "configuration of process accounting",
    "CAP_SYS_ADMIN",        "tons of admin stuff",
    "CAP_SYS_BOOT",         "reboot(2)",
    "CAP_SYS_NICE",         "nice(2)",
    "CAP_SYS_RESOURCE",     "setting resource limits",
    "CAP_SYS_TIME",         "setting system time",
    "CAP_SYS_TTY_CONFIG",   "tty configuration",
    NULL, NULL,
    };

  #ifdef LIDS
    static char *lidscaps[] =
      {
      "LIDS_INIT",     "lock_init_children",     "protect init children",
      "LIDS_FIREWALL", "lock_ip_firewall_rules", "lock IP firewall rules",
      "LIDS_MODULE",   "lock_modules",           "disallow insetion and "
                                                 "removal of kernel modules",
      "LIDS_MOUNT",    "lock_mount",             "disallow mount/umount "
                                                 "filesystems",
/*      "LIDS_RELOAD",   "reload_conf",            "reload configuration",*/
      NULL, NULL,
      };
  #endif /* LIDS */

  static void usage(const char *argv0)
    {
    fprintf(stderr, "Usage: %s [-h]\n", argv0);
    fprintf(stderr, "       -h = you're looking at it\n");
    fprintf(stderr, "Usage: %s [-v[v]] -c cap\n", argv0);
    fprintf(stderr, "       -v = verbose mode\n");
    fprintf(stderr, "       -c = return 1 if capability is set, 0 if not\n");
    fprintf(stderr, "       cap = capability to check\n");
    fprintf(stderr, "Usage: %s [-v[v]] [-z] cap ...\n", argv0);
    fprintf(stderr, "       -v = verbose mode\n");
    fprintf(stderr, "       -z = zero out capability set\n");
    fprintf(stderr, "       cap = with -z, capabilities to not zero out\n");
    fprintf(stderr, "       cap = without -z, capabilities to zero out\n");
    };

  static void listcaps(const kernel_cap_t caps)
    {
    int index=0;

    printf("Current capabilities: 0x%08X\n", caps);
    while (thecaps[index*2] != NULL)
      {
      printf("  %2d) %c%-25s", index, cap_raised(caps, index) ? '*' : ' ',
             thecaps[index*2]);
      if ((index) % 2)
        printf("\n");
      index++;
      };
    printf("\n");
    printf("    * = Capabilities currently allowed\n");
    };

  #ifdef LIDS
    void lids_set(int lidsnum, int value)
      {
      FILE *fptr;
      char file[PATH_MAX];

      snprintf(file, PATH_MAX, "%s/%s", PROC_LIDS, lidscaps[lidsnum*3+1]);
      if ((fptr=fopen(file, "w")) == NULL)
        {
        perror(file);
        exit(errno);
        };
      fprintf(fptr, "%d", value);
      fclose(fptr);
      };

    int lids_raised(int lidsnum)
      {
      FILE *fptr;
      int lids;
      char file[PATH_MAX];

      snprintf(file, PATH_MAX, "%s/%s", PROC_LIDS, lidscaps[lidsnum*3+1]);
      if ((fptr=fopen(file, "r")) == NULL)
        {
        perror(file);
        exit(errno);
        };
      fscanf(fptr, "%d", &lids);
      fclose(fptr);
      
      return(lids);
      };

    static void listlids()
      {
      int index=0;

      while (lidscaps[index*3] != NULL)
        {
        printf("      %c%-25s", 
               lids_raised(index) ? '*' : ' ', lidscaps[index*3]);
        if ((index) % 2)
          printf("\n");
        index++;
        };
      printf("    * = Functionality currently set\n");
      };
  #endif /* LIDS */

int main(int argc, char *argv[])
  {
  kernel_cap_t caps=0;
  FILE *fptr;
  int index;
  int option;
  short checkflag=0, errorflag=0, verboseflag=0, zeroflag=0;

  /* open the /proc file */
  if ((fptr=fopen(PROC_CAP, "r")) == NULL)
    {
    perror(PROC_CAP);
    exit(errno);
    };
  /* snag the current setting */
  fscanf(fptr, "%d", &caps);
  fclose(fptr);

  while ((option=getopt(argc, argv, "chvz")) != -1)
    {
    switch (option)
      {
      case 'c':
        checkflag = 1;
        break;
      case 'v':
        verboseflag++;
        break;
      case 'z':
        zeroflag = 1;
        break;
      case 'h':
      default:
        errorflag = 1;
        break;
      };
    };

  if (((checkflag) && (optind+1 != argc)) ||
      ((argc == optind) && (argc > 1)) ||
      (errorflag))
    {
    usage(argv[0]);
    exit(1);
    };

  if (argc == 1)
    {
    listcaps(caps);
    #ifdef LIDS
      printf("\n");
      listlids();
    #endif
    exit(0);
    };

  if (verboseflag >= 1)
    {
    printf("Current capabilities: 0x%08X\n", caps);
    };

  if (checkflag)
    {
    int capnum=-1;
    #ifdef LIDS
      short islids=0;
    #endif
    char *capstr=NULL, *capdescstr=NULL;

    if (isdigit(argv[optind][0]))
      {
      capnum = (int)strtol(argv[optind], (char **)NULL, 10);
      capstr = thecaps[capnum*2];
      capdescstr = thecaps[capnum*2+1];
      }
    else
      {
      int jndex=0;

      while (thecaps[jndex] != NULL)
        {
        if (!strcmp(argv[optind], thecaps[jndex]))
          {
          capnum = jndex/2;
          capstr = thecaps[jndex];
          capdescstr = thecaps[jndex+1];
          };
        jndex += 2;
        };

      #ifdef LIDS
        jndex = 0;

        while (lidscaps[jndex] != NULL)
          {
          if (!strcmp(argv[optind], lidscaps[jndex]))
            {
            capnum = jndex/3;
            capstr = lidscaps[jndex];
            capdescstr = lidscaps[jndex+2];
            islids = 1;
            };
          jndex += 3;
          };
      #endif
      };

    if (capnum == -1)
      {
      fprintf(stderr, "    %s: invalid capability\n", argv[2]);
      exit(1);
      };

    #ifdef LIDS
      if (!islids)
        {
    #endif
        if (verboseflag >= 1)
          {
          printf("  %2d) %c%-25s\n", capnum,
                 cap_raised(caps, capnum) ? '*' : ' ', thecaps[capnum*2]);
          printf("    * = Capability currently allowed\n");
          };
        exit(cap_raised(caps,capnum) ? 1 : 0);
    #ifdef LIDS
        }
      else
        {
        short raised;

        raised = lids_raised(capnum) ? 1 : 0;
        if (verboseflag >= 1)
          {
          printf("       %c%-25s\n", raised ? 1 : 0, lidscaps[capnum*3]);
          printf("    * = Capability currently allowed\n");
          };
        exit(raised);
        };
    #endif
    };

  if (verboseflag >= 1)
    {
    if (zeroflag)
      printf("  Setting");
    else
      printf("  Removing");
    printf(" capabilities:\n");
    };

  if (zeroflag)
    {
    caps = 0;
    };

  for (index=optind; index < argc; index++)
    {
    int capnum=-1;
    #ifdef LIDS
      short islids=0;
    #endif
    char *capstr=NULL, *capdescstr=NULL;

    if (isdigit(argv[index][0]))
      {
      capnum = (int)strtol(argv[index], (char **)NULL, 10);
      capstr = thecaps[capnum*2];
      capdescstr = thecaps[capnum*2+1];
      }
    else
      {
      int jndex=0;

      while (thecaps[jndex] != NULL)
        {
        if (!strcmp(argv[index], thecaps[jndex]))
          {
          capnum = jndex/2;
          capstr = thecaps[jndex];
          capdescstr = thecaps[jndex+1];
          };
        jndex += 2;
        };

      #ifdef LIDS
        jndex = 0;

        while (lidscaps[jndex] != NULL)
          {
          if (!strcmp(argv[optind], lidscaps[jndex]))
            {
            capnum = jndex/3;
            capstr = lidscaps[jndex];
            capdescstr = lidscaps[jndex+2];
            islids = 1;
            };
          jndex += 3;
          };
      #endif
      };

    if (capnum == -1)
      {
      fprintf(stderr, "    %s: invalid capability\n", argv[index]);
      exit(1);
      };

    #ifdef LIDS
      if (!islids)
        {
    #endif
        if (verboseflag >= 1)
          printf("    %2d) %-22s %s\n", capnum, capstr, capdescstr);

        if (zeroflag)
          cap_raise(caps, capnum);
        else
          cap_lower(caps, capnum);
    #ifdef LIDS
        } 
      else
        {
        if (verboseflag >= 1)
          printf("        %-22s %s\n", capstr, capdescstr);
        if (zeroflag)
          lids_lower(capnum);
        else
          lids_raise(capnum);
        };
    #endif
    };

  if (verboseflag >= 2)
    {
    listcaps(caps);
    #ifdef LIDS
      printf("\n");
      listlids();
    #endif
    };

  /* open the /proc file */
  if ((fptr=fopen(PROC_CAP, "w")) == NULL)
    {
    perror(PROC_CAP);
    exit(errno);
    };
  /* write the new setting */
  fprintf(fptr, "0x%x", caps);
  fclose(fptr);

  return(0);
  };

