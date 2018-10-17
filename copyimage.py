from shutil import copyfile
import os
filetemp = "frame00000.jpg"
for y in range(97,100):
    for x in range(97,123):
        copyfile(filetemp, os.path.splitext(filetemp)[0] + str(chr(y)) + str(chr(x)) + ".jpg")
