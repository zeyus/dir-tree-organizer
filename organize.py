#!/usr/bin/python
import argparse, os, fileutils, imageutils, shutil, sys
from sys import exit
import signal

files_copied = 0
files_failed = 0
files_ignored = 0

def signal_handler(signal, frame):
    sys.stdout.write('\nProcess interrupted %d files copied, %d files failed, %d files ignored\n'%(files_copied,files_failed,files_ignored))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


parser = argparse.ArgumentParser(description='Reorganize files into a date folder structure')
parser.add_argument('source', help='Source path')
parser.add_argument('dest', help='Destination path')
parser.add_argument('-f','--format', help='Y/M/D (3) or Y/M_D (2)', default=2, type=int,choices=fileutils.DEST_FORMAT_PARSER.keys())
parser.add_argument('-n','--nometa', help='do not use exif/raw metadata to calculate creation date', default=False, action='store_true')
parser.add_argument('-s','--skiperror', help='do not exit on copy failure', default=False, action='store_true')
parser.add_argument('-p','--showprogress', help='Show progress updates', default=False, action='store_true')
parser.add_argument('-i','--ignorehidden', help='ignore hidden (.) files', default=False, action='store_true')
parser.add_argument('-d','--delete', help='delete source', default=False, action='store_true')
parser.add_argument('-e', '--exclude', help='file extension(s) to exclude including dot (e.g. .jpg)', nargs='*')
parser.add_argument('-m', '--minsize',help='define minimum filesize in KB (may slow down copy)', type=int)

args = parser.parse_args()

if not os.path.isdir(args.source) or not os.path.isdir(args.dest):
    exit('Please ensure your source and destination are valid directories')

args.source = os.path.abspath(args.source)
args.dest = os.path.abspath(args.dest)






if args.showprogress:
    sys.stdout.write("Getting initial file count...")
    total_files = fileutils.get_count(start_path=args.source)
    sys.stdout.write("%d files found to copy\n"%total_files)

sys.stdout.write("Organizing directory tree from %s to %s\n"%(args.source,args.dest))

if args.minsize:
    args.minsize*=1024

for root, dirs, files in os.walk(args.source):
    for f in files:
        src = os.path.join(root, f)
        file_name, file_extension = os.path.splitext(os.path.basename(src))

        if args.ignorehidden and f.startswith('.') or (args.exclude and file_extension in args.exclude):
            files_ignored += 1
            continue

        if args.minsize and os.path.getsize(src) < args.minsize:
            files_ignored += 1
            continue

        dest = fileutils.getDestPath(src=src, dest=args.dest, format=args.format, nometa=args.nometa)
        append = 0
        while os.path.exists(dest):
            append += 1

            dest = os.path.join(os.path.dirname(dest), file_name + '_' + str(append) + file_extension)
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
        try:
            if not args.delete:
                shutil.copy2(src,dest)
            else:
                shutil.move(src,dest)
            files_copied += 1
            if args.showprogress:
                percentage = int(100 * float(files_copied)/float(total_files))
                sys.stdout.write("Files copied: %d of %d (%d%%)              \r" %(files_copied,total_files,percentage))
                sys.stdout.flush()

        except (IOError, os.error) as copyerror:
            files_failed += 1
            if not args.skiperror:
                exit('Error copying file: %s'%copyerror)


sys.stdout.write("\nComplete. %d files copied, %d files failed, %d files ignored\n"%(files_copied,files_failed, files_ignored))