import fileutils,time
from PIL import Image
from PIL.ExifTags import TAGS
IMAGE_EXTENSIONS = ['.jpg','.jpeg', '.tiff']

try:
    from PIL import Image
except ImportError, e:
    exit('PIL module missing %s'%e)

def getCreatedDate(file):
    date_ok = False
    date = False

    try:
        exif_data = get_exif(file)
        if exif_data.get('DateTimeOriginal', False) and not date_ok:
            try:
                date = time.mktime(time.strptime(exif_data['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S'))
                date_ok = True
            except ValueError:
                pass

        if exif_data.get('DateTime',False) and not date_ok:
            try:
                date =  time.mktime(time.strptime(exif_data['DateTime'], '%Y:%m:%d %H:%M:%S'))
                date_ok = True
            except ValueError:
                pass

    except Exception, e:
        print "hi"
        print e
        pass


    if not date_ok:
        return fileutils.getCreatedDate(file)

    return date


def get_exif(file):
    ret = {}
    i = Image.open(file)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret