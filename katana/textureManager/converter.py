import re
import subprocess
import os

'''
Function to convert textures
@@@     input: path to file     @@@
@@@     output: file            @@@
'''
def convertTextures(textFile):
    oldFile = r'{}'.format(textFile)
    file = os.path.normpath(os.path.basename(oldFile))
    dir = os.path.dirname(oldFile)
    conv = re.sub('\.+[a-z]{3}$', '.tex',  file )
    newFile = os.path.normpath(os.path.join(dir,conv))
    cmd = 'txmake {} {}'.format(oldFile, newFile)

    subprocess.call(cmd, shell=True)

'''
Function to convert HDR maps
@@@     input: path to file     @@@
@@@     output: file            @@@
'''
def convertHdr(textFile):
    oldFile = r'{}'.format(textFile)
    file = os.path.normpath(os.path.basename(oldFile))
    dir = os.path.dirname(oldFile)
    conv = re.sub('\.+[a-z]{3}$', '.tex',  file )
    newFile = os.path.normpath(os.path.join(dir, conv))
    cmd = 'txmake -envlatl "{}" "{}"'.format(oldFile, newFile)

    subprocess.call(cmd, shell=True)

'''
Function to convert textures with UDIM
@@@     input: path to files     @@@
@@@     output: files            @@@
'''
def convertUDIM(textDir):
    dir = r'{}'.format(textDir)
    for t in os.listdir(dir):
        oldFile = os.path.normpath(os.path.join(dir, t))
        conv = re.sub('\.+[a-z]{3}$', '.tex',  t )
        newFile = os.path.normpath(os.path.join(dir, conv))
        cmd = 'txmake {} {}'.format(oldFile, newFile)

        subprocess.call(cmd, shell=True)
