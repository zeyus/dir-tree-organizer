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
    return os.path.getctime(file)

