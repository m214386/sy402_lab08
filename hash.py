import os
import hashlib

f = open("hashedData.txt","a")

rootDirectory = "/"
unhashable = ["/bin","/dev","/proc","/run","/sys","/tmp","/var/lib","/var/run"]

for root, dirs, files in os.walk(rootDirectory):
    if root not in unhashable:
        if subdir not in unhashable:
            f.write(subdir) # prints list of subdirectories
            f.write("/n")
    for name in files:
        f.write(name+"\n")
        f.write(os.stat(name).st_atime)
        f.write("\n")
        with open(name,"rb") as unhashedFile:
            bytes = unhashedFile.read()
            hashedFile = hashlib.sha256(bytes).hexdigest()
            f.write(hashedFile)

f.close()
