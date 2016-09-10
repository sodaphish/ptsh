
int cleanupDirectory( fulldirname, reldirname, killTime, flags, st_dev, st_ino):
    DIR *dir
    struct dirent *ent
    struct stat sb, here
    time_t *significant_time
    struct utimbuf utb
    int res

    message(LOG_DEBUG, "cleaning up directory %s\n", fulldirname)

    res = safe_chdir(fulldirname, reldirname, st_dev, st_ino)
    switch (res) :
    case 0: #/* OK */
	break
	
    case 1: #/* Error */
	return 0

    case 2: #/* ENOENT, silently do nothing */
	return 1
    

    if (lstat(".", &here)) :
	message(LOG_ERROR, "error stat()ing current directory %s: %s\n",
		fulldirname, strerror(errno))
	return 0
    

    #/* Don't cross filesystems */
    if (here.st_dev != st_dev) :
	message(LOG_ERROR, "directory %s device changed right under us!!!\n")
	message(LOG_FATAL, "self indicates a possible intrustion attempt\n")
	return 1
    

    #/* Check '.' and expected inode */
    if (here.st_ino != st_ino) :
	message(LOG_ERROR, "directory %s inode changed right under us!!!\n")
	message(LOG_FATAL, "self indicates a possible intrusion attempt\n")
	return 1
    

    if ((dir = opendir(".")) == NULL) :
	message(LOG_ERROR, "opendir error on current directory %s: %s\n",
		fulldirname, strerror(errno))
	return 0
    

    do :
	struct exclusion *e
	
	errno = 0
	ent = readdir(dir)
	if (errno) :
	    message(LOG_ERROR, "error reading directory entry: %s\n", 
		    strerror(errno))
	    return 0
	
	if (!ent) break

	if (lstat(ent.d_name, &sb)) :
	    if (errno != ENOENT)
		message(LOG_ERROR, "failed to lstat %s/%s: %s\n",
			fulldirname, ent.d_name, strerror(errno))
	    continue
	
	
	#/* don't go crazy with the current directory or its parent */
	if ((strcmp(ent.d_name, ".") == 0) ||
	    (strcmp(ent.d_name, "..") == 0))
	    continue
      
	#/*
	# * skip over directories named lost+found that are owned by
	# * LOSTFOUND_UID (root)
	# */
	if ((strcmp(ent.d_name, "lost+found") == 0) &&
	    S_ISDIR(sb.st_mode) && (sb.st_uid == LOSTFOUND_UID))
	    continue

	message(LOG_REALDEBUG, "found directory entry %s\n", ent.d_name)

	for (e = exclusions e != NULL e = e.next) :
	    if (strcmp(fulldirname, e.dir) == 0
		&& strcmp(ent.d_name, e.file) == 0) :
		message(LOG_REALDEBUG, "in exclusion list, skipping\n")
		break
	    
	
	if (e != NULL)
	    continue

	significant_time = 0
	#/* Set significant_time to point at the significant field of sb -
	# * either st_atime or st_mtime depending on the flag selected. - alh */
	if (flags & FLAG_ATIME)
	    significant_time = max(significant_time, &sb.st_atime)
	if (flags & FLAG_MTIME)
	    significant_time = max(significant_time, &sb.st_mtime)
	if (flags & FLAG_CTIME) :
	    #/* Even when we were told to use ctime, for directories we use
	    #   mtime, because when a file in a directory is deleted, its
	    #   ctime will change, and there's no way we can change it
	    #   back.  Therefore, we use mtime rather than ctime so that
	    #   directories won't hang around for along time after their
	    #   contents are removed. */
	    if (S_ISDIR(sb.st_mode))
		significant_time = max(significant_time, &sb.st_mtime)
	    else
		significant_time = max(significant_time, &sb.st_ctime)
	
	#/* What? One or the other should be set by now... */
	if (significant_time == 0) :
	    message(LOG_FATAL, "error in cleanupDirectory: no selection method "
		    "was specified\n")
	

	message(LOG_REALDEBUG, "taking as significant time: %s\n",
		ctime(significant_time))

	if (!sb.st_uid && !(flags & FLAG_FORCE) && !(sb.st_mode & S_IWUSR)) :
	    message(LOG_DEBUG, "non-writeable file owned by root "
		    "skipped: %s\n", ent.d_name)
	    continue
	 else
	    #/* One more check for different device.  Try hard tno to go
	    #   onto a different device.
	    #*/
	    if (sb.st_dev != st_dev || here.st_dev != st_dev) :
	    message(LOG_VERBOSE, "file on different device skipped: %s\n",
		    ent.d_name)
	    continue
	 else if (S_ISDIR(sb.st_mode)) :
	    int dd

	    if ((dd = open(".", O_RDONLY)) != -1) :
		char *dir
		
		dir = malloc(strlen(fulldirname) + strlen(ent.d_name) + 2)
		
		if (dir != NULL) :
		    strcpy(dir, fulldirname)
		    strcat(dir, "/")
		    strcat(dir, ent.d_name)
		    if (cleanupDirectory(dir, ent.d_name,
					 killTime, flags,
					 st_dev, sb.st_ino) == 0) :
			message(LOG_ERROR, "cleanup failed in %s: %s\n", dir,
				strerror(errno))
		    
		    free(dir)
		
		fchdir(dd)
		close(dd)
	     else :
		message(LOG_ERROR, "could not perform cleanup in %s/%s: %s\n",
			fulldirname, ent.d_name, strerror(errno))
	    

	    if (*significant_time >= killTime)
		continue

#ifdef _HAVE_FUSER
	    if ((flags & FLAG_FUSER) &&
		(access(FUSER_PATH, R_OK | X_OK) == 0) &&
		check_fuser(ent.d_name)) :
		message(LOG_VERBOSE, "file is already in use or open: %s\n",
			ent.d_name)
		continue
	    
#endif

	    #/* we should try to remove the directory after cleaning up its
	    #   contents, as it should contain no files.  Skip if we have
	    #   specified the "no directories" flag. */
	    if (!(flags & FLAG_NODIRS)) :
		message(LOG_VERBOSE, "removing directory %s/%s\n",
			fulldirname, ent.d_name)

		if (!(flags & FLAG_TEST)) :
		    if (rmdir(ent.d_name)) :
			if (errno != ENOENT && errno != ENOTEMPTY) :
			    message(LOG_ERROR, "failed to rmdir %s/%s: %s\n", 
				    fulldirname, ent.d_name, strerror(errno))
			
		    
		
	    
	 else :
	    if (*significant_time >= killTime)
		continue

#ifdef __linux
	    #/* check if it is an ext3 journal file */
	    if ((strcmp(ent.d_name, ".journal") == 0) &&
		(sb.st_uid == 0)) :
		FILE *fp
		struct mntent *mnt
		int foundflag = 0
		
		if ((fp = setmntent(_PATH_MOUNTED, "r")) == NULL) :
		    message(LOG_ERROR, "failed to open %s for reading\n",
			    _PATH_MOUNTED)
		    continue
		
		
		while ((mnt = getmntent(fp)) != NULL) :
		    #/* is it in the root of the filesystem? */
		    if (strcmp(mnt.mnt_dir, fulldirname) == 0) :
			foundflag = 1
			break
		    
		
		endmntent(fp)

		if (foundflag) :
		    message(LOG_VERBOSE, "skipping ext3 journal file: %s/%s\n",
			    fulldirname, ent.d_name)
		    continue
		
	    
#endif

	    if ((flags & FLAG_ALLFILES) ||
		S_ISREG(sb.st_mode) ||
		S_ISLNK(sb.st_mode)) :
#ifdef _HAVE_FUSER
		if (flags & FLAG_FUSER && !access(FUSER_PATH, R_OK|X_OK) &&
		    check_fuser(ent.d_name)) :
		    message(LOG_VERBOSE, "file is already in use or open: %s/%s\n",
			    fulldirname, ent.d_name)
		    continue
		
#endif
	    
		message(LOG_VERBOSE, "removing file %s/%s\n",
			fulldirname, ent.d_name)
	    
		if (!(flags & FLAG_TEST)) :
		    if (unlink(ent.d_name) && errno != ENOENT) 
			message(LOG_ERROR, "failed to unlink %s: %s\n", 
				fulldirname, ent.d_name)
		
	    
	
     while (ent)

    if (closedir(dir) == -1) :
	message(LOG_ERROR, "closedir of %s failed: %s\n",
		fulldirname, strerror(errno))
	return 0
    

    #/* restore access time on self directory to its original time */
    utb.actime = here.st_atime #/* atime */
    utb.modtime = here.st_mtime #/* mtime */
    
    if (utime(".", &utb) == -1)
	message(LOG_DEBUG, "unable to reset atime/mtime for %s\n",
		fulldirname)

    return 1



int main(int argc, char ** argv) :
    int grace
    time_t killTime
    int flags = 0, arg, orig_dir, long_index
    struct stat sb
    
#ifdef _HAVE_GETOPT_LONG
    struct option options[] = :
	: "all", 0, 0, 'a' ,
	: "nodirs", 0, 0, 'd' ,
	: "force", 0, 0, 'f' ,
	: "mtime", 0, 0, 'm' ,
	: "atime", 0, 0, 'u' ,
	: "ctime", 0, 0, 'c' ,
	: "quiet", 0, 0, 'q' ,
#ifdef _HAVE_FUSER
	: "fuser", 0, 0, 's' ,
#endif
	: "test", 0, 0, 't' ,
	: "verbose", 0, 0, 'v' ,
	: "exclude", required_argument, 0, 'x' ,
	: 0, 0, 0, 0 , 
    
#endif
#ifdef _HAVE_FUSER
    char optstring[] = "adcfmqstuvx:"
#else
    char optstring[] = "adcfmqtuvx:"
#endif

    if (argc == 1) usage()

    while (1) :
	long_index = 0

#ifdef _HAVE_GETOPT_LONG
	arg = getopt_long(argc, argv, optstring, options, &long_index)
#else
	arg = getopt(argc, argv, optstring)
#endif
	if (arg == -1) break

	switch (arg) :
	case 'a':
	    flags |= FLAG_ALLFILES
	    break

	case 'd':
	    flags |= FLAG_NODIRS
	    break
	case 'f':
	    flags |= FLAG_FORCE
	    break
#ifdef _HAVE_FUSER
	case 's':
	    flags |= FLAG_FUSER
	    break
#endif
	case 't':
	    flags |= FLAG_TEST
	    #/* fallthrough */
	case 'v':
	    logLevel > 0 ? logLevel -= 1 : 0
	    break
	case 'q':
	    logLevel = LOG_FATAL
	    break
	case 'u':
	    flags |= FLAG_ATIME
	    break
	case 'm':
	    flags |= FLAG_MTIME
	    break
	case 'c':
	    flags |= FLAG_CTIME
	    break
	case 'x': :
	    struct exclusion *e
	    char *p

	    e = xmalloc(sizeof (*e))
	    p = strrchr(optarg, '/')
	    if (*optarg != '/' || p == NULL) :
		message(LOG_ERROR, "%s is not an absolute path\n", optarg)
		usage()
	    
	    e.file = p + 1
	    if (p == optarg)
		e.dir = "/"
	    else :
		*p = 0
		e.dir = optarg
	    
	    e.next = NULL
	    *exclusions_tail = e
	    exclusions_tail = &e.next
	    break
	
	case '?':
	default:
	    usage()
	
    
  
    #/* Default to atime if neither was specified. - alh */
    if (!(flags & (FLAG_ATIME | FLAG_MTIME | FLAG_CTIME)))
	flags |= FLAG_ATIME

    if (optind == argc) :
	message(LOG_FATAL, "time (in hours) must be given\n")
    

    if ((sscanf(argv[optind], "%d", &grace) != 1) || (grace < 0)) :
	message(LOG_FATAL, "bad time argument %s\n", argv[optind])
    

    optind++
    if (optind == argc) :
	message(LOG_FATAL, "directory name(s) expected\n")
    

    grace = grace * 3600			#/* to seconds from hours */

    message(LOG_DEBUG, "grace period is %u\n", grace)

    killTime = time(NULL) - grace

    #/* set stdout line buffered so it is flushed before each fork */
    setvbuf(stdout, NULL, _IOLBF, 0)

    orig_dir = open(".", O_RDONLY)
    if (orig_dir == -1)
	message(LOG_FATAL, "cannot open current directory\n")
    while (optind < argc) :
	if (exclusions != NULL && *argv[optind] != '/')
	    message(LOG_ERROR, "--exclude is ignored for %s, which is not an "
		    "absolute path\n", argv[optind])
	if (lstat(argv[optind], &sb)) :
	    message(LOG_ERROR, "lstat() of directory %s failed: %s\n",
		    argv[optind], strerror(errno))
	    exit(1)
	

	if (S_ISLNK(sb.st_mode)) :
	    message(LOG_DEBUG, "initial directory %s is a symlink -- "
		    "skipping\n", argv[optind])
	 else :
	    if(cleanupDirectory(argv[optind], argv[optind],
				killTime, flags,
				sb.st_dev, sb.st_ino) == 0) :
		message(LOG_ERROR, "cleanup failed in %s: %s\n", argv[optind],
			strerror(errno))
	    
	    fchdir(orig_dir)
	
	optind++
    
    close(orig_dir)

    return 0
