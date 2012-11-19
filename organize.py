#!/usr/bin/python
import argparse, os, fileutils, imageutils, shutil, sys
from sys import exit



parser = argparse.ArgumentParser(description='Reorganize files into a date folder structure')
parser.add_argument('source', help='Source path')
parser.add_argument('dest', help='Destination path')
parser.add_argument('-f','--format', help='Y/M/D (3) or Y/M_D (2)', default=2, type=int,choices=fileutils.DEST_FORMAT_PARSER.keys())
parser.add_argument('-n','--nometa', help='do not use exif/raw metadata to calculate creation date', default=False, action='store_true')
parser.add_argument('-s','--skiperror', help='do not exit on copy failure', default=False, action='store_true')
parser.add_argument('-p','--showprogress', help='Show progress updates', default=False, action='store_true')
parser.add_argument('-i','--ignorehidden', help='ignore hidden (.) files', default=False, action='store_true')
parser.add_argument('-d','--delete', help='delete source', default=False, action='store_true')

args = parser.parse_args()

if not os.path.isdir(args.source) or not os.path.isdir(args.dest):
    exit('Please ensure your source and destination are valid directories')

args.source = os.path.abspath(args.source)
args.dest = os.path.abspath(args.dest)

files_copied = 0
files_failed = 0


sys.stdout.write("Organizing directory tree from %s to %s\n"%(args.source,args.dest))


for root, dirs, files in os.walk(args.source):
    for f in files:
        if args.ignorehidden and f.startswith('.'):
            continue
        src = os.path.join(root, f)
        dest = fileutils.getDestPath(src=src, dest=args.dest, format=args.format, nometa=args.nometa)
        append = 0
        while os.path.exists(dest):
            append += 1
            file_name, file_extension = os.path.splitext(os.path.basename(src))
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
                sys.stdout.write("Files copied: %d        \r" %files_copied)
                sys.stdout.flush()

        except (IOError, os.error) as copyerror:
            files_failed += 1
            if not args.skiperror:
                exit('Error copying file: %s'%copyerror)


sys.stdout.write("\nComplete. %d files copied, %d files failed"%(files_copied,files_failed))