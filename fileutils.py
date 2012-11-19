import destinations,imageutils, os, time

DEST_FORMAT_PARSER = {2: destinations.getTwoLevelDest, 3: destinations.getThreeLevelDest}


def getDestPath(src, dest, format=2, nometa=False):
    f, file_extension = os.path.splitext(src)

    if not nometa and file_extension.lower() in imageutils.IMAGE_EXTENSIONS:
        date = imageutils.getCreatedDate(src)
    else:
        date = getCreatedDate(src)

    final_destination = DEST_FORMAT_PARSER[format](os.path.basename(src), dest, time.gmtime(date))

    return final_destination




def getCreatedDate(file):
    ctime = os.path.getctime(file)
    mtime = os.path.getmtime(file)
    return min(mtime,ctime)

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def get_count(start_path = '.'):
    total_count = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            total_count += 1
    return total_count