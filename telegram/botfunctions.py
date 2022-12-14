import sys
sys.path.append(".")
from vt import Virustotal

vtapi = Virustotal()

def uploadfile(file):
    hash = vtapi.upload_file(file)
    return hash

def counttests(obj):
    dcount = 0
    ucount = 0
    ncount = 0
    detected = []
    undetected = []
    notsupported = []
    dresult = []

    for ele in obj.results:
        if ele.category == "malicious":
            dcount += 1
            detected.append(ele.engine_name)
            dresult.append(ele.result)

        elif ele.category == "undetected":
            ucount += 1
            undetected.append(ele.engine_name)

        else:
            ncount += 1
            notsupported.append(ele.engine_name)

    return dcount,ucount,ncount,detected,undetected,notsupported,dresult

def cleaninfo(hash):
    obj = vtapi.file_info(hash)
    if obj == None:
        print("File does not Exist")
        return None,None,None, None

    D,U,N,DL,UL,NL,DR = counttests(obj)
    
    fronttext = f'š§¬ **Detections**: __{D} / {D+U}__\
        \n\nš **File Name**: __{obj.filename}__\
        \nš **File Type**: __{obj.type_description} ({obj.file_type_info["file_type"]})__\
        \nš **File Size**: __{pow(2,-20)*obj.size:.2f} MB__\
        \nā± **Times Submited**: __{obj.times_submitted}__\
        \n\nš¬ **First Analysis**\nā¢ __{obj.first_submission_date}__\
        \nš­ **Last Analysis**\nā¢ __{obj.last_modification_date}__\
        \n\nš **Magic**\nā¢ __{obj.magic}__'
        #\n\nāļø [Link to VirusTotal](https://virustotal.com/gui/file/{hash})'

    testtext = '**ā - Malicious\nā - UnDetected\nā ļø -  Not Suported**\nāāāāāāāāāā\n'
    for ele in DL:
        testtext = f'{testtext}ā {ele}\n'
    for ele in UL:
        testtext = f'{testtext}ā {ele}\n'
    for ele in NL:
        testtext = f'{testtext}ā ļø {ele}\n'  

    signatures = ''
    for i in range(len(DR)):
        signatures = f'{signatures}ā {DL[i]}\
    \nā° {DR[i]}\n'
    
    if D == 0:
        signatures = "ā Your File is Safe"
        
    link = f'https://virustotal.com/gui/file/{hash}'
    return fronttext,testtext,signatures,link
