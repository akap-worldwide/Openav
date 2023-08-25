from oletools.olevba import VBA_Parser, TYPE_OLE, TYPE_OpenXML, TYPE_Word2003_XML, TYPE_MHTML
from oletools.mraptor import MacroRaptor
import time
import subprocess
import os
from shutil import copyfile
from subprocess import Popen, PIPE
import pathlib
import oletools.oleid




def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode
    except Exception as e:
        pass

def ats(file):
    cmd = '"'+str(pathlib.Path(__file__).parent.absolute())+'/sigcheck64.exe" -vs  "{0}" -nobanner'.format(file)
    stdout = Popen(cmd, shell=True, stdout=PIPE).stdout
    output = stdout.readlines()
    str_output=output[10].decode()
    __splited__ = str_output.split(":")[1]
    if 'Submitted'  in __splited__ : return True
    if eval(__splited__) > 0.0:
        return True
    return False


class Olescan:
    def __init__(self,file) -> None:
        self.vbaobj = VBA_Parser(file)
        self.file = file

    def olevbaScan(self):
            #Analyse file for warning factors...
            result = self.vbaobj.analyze_macros()
            for kw_type, keyword, description in result:
                print ('type=%s - keyword=%s - description=%s' % (kw_type, keyword, description))

    def mraptorScanisSus(self):

            #Get all modules and send it back to mraptor's undocumented class object...
            all_vba_modules = self.vbaobj.get_vba_code_all_modules()
            scan = MacroRaptor(all_vba_modules)
            scan.scan()
            if scan.suspicious:
                #retrun true
                return True
            return False
    
    def oleid(self):
        oid = oletools.oleid.OleID(self.file).check()
        if oid[-3].value == 0 and oid[-2].value == False and oid[-1].value == 0:
            return False
        return True

    def Extract_files(self):
        #copying the file to temp dir before extraction
        name = str(time.time())
        os.mkdir('temp/'+name)

        copyfile(self.file,'temp/'+name+'/'+name+'.tmp')

        cmd = 'oleobj -i "temp/{}/{}.tmp"'.format(name,name)
        return_code = execute_command(cmd)

        if return_code == 1:
             #deleting the file
            os.remove('temp/{}/{}.tmp'.format(name,name))

            files = os.listdir('temp/'+name)

            if len(files) > 0:
                ret_code = True
                
                return ret_code

        else:
            eval('1/0')

        return False       

    def Extract_rtf_files(self):
        #copying the file to temp dir before extraction
        name = str(time.time())
        os.mkdir('temp/'+name)

        copyfile(self.file,'temp/'+name+'/'+name+'.tmp')

        cmd = 'rtfobj -i "temp/{}/{}.tmp"'.format(name,name)
        return_code = execute_command(cmd)

        if return_code == 1:
             #deleting the file
            os.remove('temp/{}/{}.tmp'.format(name,name))

            files = os.listdir('temp/'+name)

            if len(files) > 0:
                ret_code = False
                #scanning files....
                for file in files:
                    if ats('temp/'+name+'/'+file):
                        ret_code = True
                    os.remove('temp/'+name+'/'+file) #Deleting files....
                
                os.rmdir('temp/'+name)
                return ret_code

        else:
            pass
        

        return False      



    def Scan(self):
        if self.oleid():
            return True 
        if self.vbaobj.detect_macros():
            if self.mraptorScanisSus():
                return True
        else:
            try:
                return self.Extract_files()
            except:
                return self.Extract_rtf_files()








