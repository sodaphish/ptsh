CC=gcc
CFLAGS=-Wall -g
SRCS=inotify_test.c inotify_utils.c event_queue.c

.o.c:
	$(CC) $(CFLAGS) -c $<

all: inotify_test

inotify_test: inotify_utils.o inotify_test.o event_queue.o
	$(CC) $(CFLAGS) inotify_utils.o inotify_test.o event_queue.o -o inotify_test

clean:
	rm -f *.o *.bak inotify_test
