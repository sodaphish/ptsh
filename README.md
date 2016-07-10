# PTSH
the pentester's shell

PTSH is a shell written in python, with the intention of providing extensions beyond what a traditional shell provides, such as logging, workspaces, database for tracking various findings, as well as replacements for some tools to integrate their data collection into the database.   And most importantly, the ability to provide reports of those activities as well as logs to support that report.

Currently all code is being kept in the dev tree until we hit the first milestone.

#Roadmap
- version 0.0.0 (we are here)
  - infrastructure to facilitate all the future features
  - fleshing out the necessary bits of splib that facilitate things
- version 0.1.0
  - support for workspaces
  - database integration for targets, notes, etc.
  - intercept for nmap, host and traceroute
  - automatic expansion of built-in variables before passthru to shell
- version 0.2.0
  - command-line switching to override config settings
  - automated diff of files opened in text editors
  - output intercepts for hping, zmap, dig, whois, and ping utilities
- version 0.3.0 
  - support for plugins/modules that can be run and pass data back ino the database
  - intercepts for openvas/nessus and (TODO)
  - introduction of reporting
- version 0.4.0
  - support for multiple users (collaboration)
  - reporting to be robust -- outputting a themable HTML report with a timeline hyper-linked to specific results, all nicely bundled into a zip file.

  
Core features of PTSH are the ability to automatically capture output of command-line tools and import that information into a database (so we can leverage the data without re-writing every tool), and a pluggable framework to expand functionality at will (intercepts are ultimately just plugins), and most importantly the ability to cogently produce a report of the activities 