import getopt, sys, os, datetime, logging

cleanup_path=''
now = (datetime.datetime.now()).timestamp()
#print (now)
found_p =False
recursive=False
ext=''
name=''
cutoff_day_epoch=now - 2592000 #All files older than 30 days will get deleted in the given path by default, if not days/date not provided as commandline argument

def tool_help():
    print(
        'Usage: WovenCleanup.py -p <dir path> -d|D<days n |Date mm-dd-yyyy> -e<specific extensions> -n<file name keyword>'
        '\n-p : Folder path to delete files'
        '\n-d : Delete files with last modified older than given days. Default 30 days'
        '\n-D : Delete files with last modified older than given date'
        '\n-n : Delete files with given keyword in file name'
        '\n-e : Delete files end with given extensions. Multiple extensions can be given but should be separated by comma '
        '\n-r : Delete files recursively in subfolders'
        '\nExamples: \nWovenCleanup.py -p /home/test -d 40 '
        '\nWovenCleanup.py -p /home/test -D 1-13-2022'
        '\nWovenCleanup.py -p /home/test -D 1-13-2022 -e .txt,.log -- Multiple extenstion should be separated by comma')
    sys.exit(2)

#Create and configure logger and logs in std.log
logging.basicConfig (filename="std.log", format='%(asctime)s %(message)s')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
# Command-line arguments
try:
    options,args= getopt.getopt(sys.argv[1:], "hp:d:D:re:n:",['help','path=','days=', 'date=','recursive','ext=','name='])
    if options == []:
        tool_help()
except getopt.GetoptError:
    print('Usage: WovenCleanup.py -p <dir path> -d|D<days|Date>')
    sys.exit(2)
#print (options)
#print(args)
for option,arg in options:
    if option in ("-h", "--help"):
        tool_help()
    elif option in ("-p", "--path"):
        cleanup_path = arg
        found_p = True
        #print(option)
        if not os.path.isdir(cleanup_path):
            print("Please enter a valid path")
            sys.exit(2)
    elif option in ("-d", "--days"):
        days = arg
        cutoff_day_epoch= now - int(days)*86400
    elif option in ("-D", "--date"):
        cutoff_day_epoch = datetime.datetime.strptime(arg, "%m-%d-%Y").timestamp()
        #print(date)
    elif option in ("-r", "--recursive"):
        recursive=True
    elif option in ("-e", "--ext"):
        ext=tuple(arg.split(","))
    elif option in ("-n", "--name"):
        name=arg
        #print(name, type(name))
if not found_p:
    print('Please provide path argument to clean')
    tool_help()
logger.info(f'----------------------------------------------------------------------'
            f'\nInitiating file deletion ...\nRecursive mode enabled: {recursive}\nCleanup path given: {cleanup_path}'
            f'\nDeleting files older than: {datetime.datetime.fromtimestamp(cutoff_day_epoch)}')
 #File deletion
if recursive: #Deletes files recursively in the clean-up path
    for root,d_names,files in os.walk(cleanup_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.stat(file_path).st_mtime < cutoff_day_epoch:
                #print(file,file_path,name)
                if os.path.isfile(file_path) and file.endswith(ext) and (name in file):
                    try:
                        os.remove(file_path)
                        logger.info(f'Deleted {file_path}')
                    except OSError as e:
                        logger.error(f'Error: {file_path}, {e.strerror}')
else:  #Deletes files only in the cleanup path
    #print(os.listdir(cleanup_path))
    for file in os.listdir(cleanup_path):
        file_path = os.path.join(cleanup_path, file)
        #print(file)
        if os.stat(file_path).st_mtime < cutoff_day_epoch:
            if os.path.isfile(file_path)and file.endswith(ext) and (name in file):
                try:
                    os.remove(file_path)
                    logger.info(f'Deleted {file_path}')
                except OSError as e:
                    logger.error(f'Error: {file_path}, {e.strerror}')
