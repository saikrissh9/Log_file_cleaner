# Log_file_cleaner
Deletes old files in given path 
-----------------------------------------------
Usage: WovenCleanup.py -p <dir path> -d|D<days n |Date mm-dd-yyyy> -e<specific extensions> -n<file name keyword>
              -p : Folder path to delete files
              -d : Delete files with last modified older than given days. Default 30 days
              -D : Delete files with last modified older than given date
              -n : Delete files with given keyword in file name
              -e : Delete files end with given extensions. Multiple extensions can be given but should be separated by comma 
              -r : Delete files recursively in subfolders
              Examples: 
              WovenCleanup.py -p /home/test -d 40 -n log -e .log
              WovenCleanup.py -p /home/test -D 1-13-2022
              WovenCleanup.py -p /home/test -D 1-13-2022 -e .txt,.log -- Multiple extenstion should be separated by comma
