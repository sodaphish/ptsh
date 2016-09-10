/*
 * a loadable kernel module (lkm) to watch syscalls that match a template
 * written in C... mmm... 
 */
#include <linux/module.h>
#include <linux/kernel.h>


int init_module()
{
  return 0;
}


void cleanup_module()
{
}

