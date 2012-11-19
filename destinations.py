import time,os

def getTwoLevelDest(filename,dest,date):
    return os.path.join(dest,time.strftime('%Y',date),time.strftime('%m',date)+'_'+time.strftime('%d',date),filename)


def getThreeLevelDest(filename,dest,date):
    return os.path.join(dest,time.strftime('%Y',date),time.strftime('%m',date),time.strftime('%d',date),filename)
