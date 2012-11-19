Organize your files
=============

Dir-tree-organizer (it's current name) is a simple python application that is designed to do the following:

- Take a messy directory full of photos and/or other files
- Copy or move those photos into a new directory and organize it by date

Features
-------------

- Destination files organized in 3 levels YYYY/MM/DD or 2 YYYY/MM_DD (maybe with month only later)
- Ability to use EXIF data to calculate the image date
- Progress indicator of sorts (total files)
- Ability to skip specific file extensions
- Having a minimum file size

Installation
-------------

- Check out this repository to your machine. 
- Make sure you have PIL installed (`sudo pip install PIL`)
- run `python organize.py`


Usage examples
-------------

To organize all files in /mnt/disk1/messy and create a new organized version in /mnt/disk2/clean using the default 2 level format.

This also continues on errors and skips hidden files and has a progress meter:

```bash
python organize.py -s -p -i -m 150 /mnt/disk1/messy /mnt/disk2/clean
```

For more info run 

```bash
python organize.py -h
```