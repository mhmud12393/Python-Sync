# Sync 2
  A program that synchronizes two folders: source and replica. The program should maintain a full, identical copy of destination folder at replica folder.

  Commands(CMD): 
  python Sync.py -s C:....\source -r C:....\replica -i 10  -l C:....\Log_file.txt
    
  -s = Source Folder
  -r = Replica Folder
  -i = Interval
  -l = Log File

Requirements:

1. Synchronization must be one-way: after the synchronization content of the replica folder
should be modified to exactly match content of the source folder;

2. Synchronization should be performed periodically;

3. File creation/copying/removal operations should be logged to a file and to the console
output;

4. Folder paths, synchronization interval and log file path should be provided using the
command line arguments. 
