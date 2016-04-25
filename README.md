# PTSH
the pentester's shell

PTSH is a shell written in python, with the intention of providing extensions beyond what a traditional shell provides, such as logging, workspaces, database for tracking various findings, as well as replacements for some tools to integrate their data collection into the database. 

Currently all code is being kept in the dev tree until we hit the first milestone.

## Roadmap
- version 0.1.0
  - support for workspaces
  - database integration
  - quick and dirty portscanner
- version 0.2.0
  - more sophisticated portscanner
  - diff of files opened in text editors
  - TTL expired traceroute
- version 0.3.0 
  - support for plugins/modules that can be run and pass data back ino the database 