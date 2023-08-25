import pickle
from feature_extraction import feature_extraction
import warnings
from subprocess import Popen, PIPE
import pathlib
import time
warnings.filterwarnings("ignore")

def ats(file):
    cmd = '"'+str(pathlib.Path(__file__).parent.absolute())+'/sigcheck64.exe" -vs  "{0}" -nobanner'.format(file)
    stdout = Popen(cmd, shell=True, stdout=PIPE).stdout
    output = stdout.readlines()
    str_output=output[10].decode()
    __splited__ = str_output.split(":")[1]
    try:
        if eval(__splited__) > 0.0:
            return True
        return False
    except:
        time.sleep(15)
        return ats(file)
file = "D:\\downloads\\2023-08-08\\669d6aa22582ece6305d4347a31cd25bb2f01075749de0fa7438a04725f02cd1.pdf"
clf = pickle.load(open('pdfanalysis\Malicious_pdf_detection\pdfmodel.plk','rb'))
fea = feature_extraction(file)
res =  clf.predict_proba(fea)[0][1]*100 
print(fea,res)
print(ats(file))
if res >=50:
    print('Malware')
elif res > 10 :
    if ats(file):
        print('Malware')
    else:
        print('Not Malware')
else:
    print('Not malware')
