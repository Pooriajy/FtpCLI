import ftplib
import os
from colorama import Fore as c
import getpass

server = '10.1.1.113'
user = input("Username: ")
password = getpass.getpass()

dir=''
buffer = 8192
ftp = ftplib.FTP(server)
print(ftp.login(user=user,passwd=password))
print(ftp.getwelcome())
# ftp.debug(1)

class FtpUploadTracker: #thanks to user cmd from stackoverflow
    sizeWritten = 0
    totalSize = 0
    lastShownPercent = 0

    def __init__(self, totalSize):
        self.totalSize = totalSize

    def handle(self, block):
        self.sizeWritten += buffer
        percentComplete = round((self.sizeWritten / self.totalSize) * 100)

        if (self.lastShownPercent != percentComplete):
            self.lastShownPercent = percentComplete
            print(f'\t{str(percentComplete)} %',end='\r')




def uploaddir():
    files = os.listdir('.')[1:]

    for file in files:
        f = open(file, mode='rb')
        upt = FtpUploadTracker(int(os.path.getsize(file)))
        print(c.YELLOW)
        print(f'\tUploading: ' + file, end='\r')
        ftp.storbinary('STOR ' + file, f, buffer,upt.handle)
        f.close()
    print(c.RESET)

def uploadfile(file):
    try:
        f = open(file,mode='rb')
        upt = FtpUploadTracker(int(os.path.getsize(file)))
        print(c.YELLOW)
        print(f'\tUploading: ' + file)
        ftp.storbinary('STOR ' + file, f, buffer, upt.handle)
        f.close()
        print(c.RESET)
    except Exception as e:
        print(c.RED)
        print(e)
        print(c.RESET)

def getlist(path):
    print(ftp.dir(path))

while True:
    try:
        print(c.GREEN)
        x = input(">>")
        print(c.RESET)
        if x == 'exit':
            break
        elif x == 'uploadir':
            uploaddir()
        elif x.startswith("upload "):
            files = x.split(" ")
            files = files[1:]
            for file in files:
                uploadfile(file)
        elif x.startswith('buffer'):
            bf = x.split(' ')
            buffer = int(bf[1])
        elif x.startswith('cd '):
            dir = x.split(" ")[1]
            ftp.cwd(dir)
        elif x.startswith('ls'):
            if x == 'ls':
                ftp.cwd(".")
            else:
                dir = x.split(" ")[1]
                ftp.cwd(dir)
            files = []
            try: #thanks to William Keller from stackoverflow
                files = ftp.nlst()
            except ftplib.error_perm as resp:
                if str(resp) == "550 No files found":
                    print("No files in this directory")
                else:
                    raise
            for f in files:
                print(f)
        else:
            try:
                ftp.sendcmd(x)
            except:
                pass
    except Exception as e:
        print(c.RED)
        print(e)
        print(c.RESET)

ftp.quit()
