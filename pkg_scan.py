"""File for scanning directory or file...."""

from clamEngine.connector import clamd #clamd connector
from staticanalysis.PE_main import * #ML module for static scanning...
import os
import threading
import concurrent.futures
import time
import file_type_sep
globals()['i'] = 0
def pfiles(file,dirpath):
    globals()['i']+=1
    print('[*]',globals()['i'],"Files discovered",end='\r')
    return os.path.join(dirpath, file)
def getfiles(path):
    globals()['i']=0
    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(path):
        listOfFiles += [pfiles(file,dirpath) for file in filenames]
       
        time.sleep(0.5)
    return listOfFiles

def scanfile(s,f):
    e1,e2 = concurrent.futures.ThreadPoolExecutor()
    l1 = e1.submit(isMalware,f)
    l2 = e2.submit(s.scan,f)
    result1 = l1.result()
    result2 = l2.result()
    if l1 or l2['malware']:
        return True
    else:
        return False

def scanfiles(s,i):
    #Getting files....
    f = getfiles(i)
    file_type_sep.file_ext_sep(f)
    e1 = concurrent.futures.ThreadPoolExecutor()
    print("[*]ClamAV scan started successfully...")
    e2 = concurrent.futures.ThreadPoolExecutor()
    print("[*]Static malware analyisis started successfully...")
    l1 = e1.submit(MLscanfiles,f)
    l2 = e2.submit(s.scanfiles,f,True)
    result1 = l1.result()
    result2 = l2.result()
    
    malwares = (result1 + list(set(result2) - set(result1)))
    print('The threats found are:\n')
    for file in malwares:
        print(file)
    if input("\nDo you want to delete the malwares(Y/N):").lower() == "y":
        print('[*] Deleting...',end="\r")
        for file in malwares:
            try:
                os.remove(file)
            except:
                print(file,"could not be deleted...")
        print("[*]Malwares deleted...")


def main():
    clam = clamd()
    scanfiles(clam,"D:\\downloads\\2023-08-09")

main()


