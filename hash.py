# MIDN 1/C Abby McGinn
# Lab08

# Professor Dias: I worked with my partner (1/C Berroteran) for several
# hours on this lab. We attempted it first without looking at your code,
# as neither of us even realized it was available. When we got stuck,
# we looked at your code for guidance. I commented specifically which
# portions we used from your code, and commented everything to show I
# understand the code. We spent a lot of time looking things up to fully
# understand what you did, and to try to do it differently.

import os
import hashlib
import datetime
import csv

rootDirectory = "/" # so it walks through every file in the system
# the list "unhashable" includes libraries we don't want to hash
# I also added directories that continued to cause errors when I was testing
unhashable = ["vmlinuz","bin","dev","proc","run","sys","tmp","var/lib","var/run"]

# checks if the hash file already exists
if os.path.isfile("hashedData.csv"):
    print("Hash file already exists. Comparing against current data.")

    # initializes a list to hold items that represent changes from the old hash data
    updateList = []

    # open the old hash file
    with open("hashedData.csv") as old_file:
        # read the lines so we can easily handle it later when comparing
        old_hash_data = old_file.readlines()

    # open the csv file for writing
    f_new = open("hashedData.csv","w")
    # walk through ALL the files
    for root, dirs, files in os.walk(rootDirectory):
        # this is how we skip the unhashable directories
        if root in unhashable:
            dirs = []
            files = []
        # walking through every file we want to hash
        for name in files:
            strAppend = os.path.join(root,name)
            hash = hashlib.sha256()
            try:
                f_file = open(strAppend,'rb')
            except:
                continue
            # we used your code as an example of using the buffer
            while True:
                # we use 4096 because Linux file systems allocate memory in a
                # directory by factors of 4096 bytes
                holder = f_file.read(4096)
                if not holder:
                    break
                hash.update(holder)
            f_file.close()

            # grab the current time (using imported lib)
            time = str(datetime.datetime.now())
            hash_update = hash.hexdigest()
            # strAppend is what we are building to append to the file
            strAppend += str(" "+hash_update)
            strAppend += str(" "+time)
            strAppend += "\n"

            # here we check to see if the hash exists in old hash data
            for line in old_hash_data:
                # if it is not in the old data, that means this file HAS been altered
                # so we want to add it to the updateList
                if hash_update not in line:
                    updateList.append(strAppend)
            f_new.write(strAppend)
        f_new.close()
        print("The following items were changed: \n")
        for update in updateList:
            print(update+"\n")

else:
    # else, we do the same process, but do not check for updates
    print("Hash file does not exist. Creating hash file.")
    f_new = open("hashedData.csv","w")
    for root, dirs, files in os.walk(rootDirectory):
        if root in unhashable:
            dirs = []
            files = []
        for name in files:
            strAppend = os.path.join(root,name)
            hash = hashlib.sha256()
            try:
                f_file = open(strAppend,'rb')
            except:
                #f_file.close()
                continue
            while True:
                holder = f_file.read(4096)
                if not holder:
                    break
                hash.update(holder)
            f_file.close()
            time = str(datetime.datetime.now())
            strAppend += str(" "+hash.hexdigest())
            strAppend += str(" "+time)
            strAppend += "\n"
            f_new.write(strAppend)
f_new.close()
