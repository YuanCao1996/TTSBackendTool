import json
import wave
import contextlib
from os import listdir
import os

def getWaveLength(path):
    totalLength=0
    waveList=listdir(path)
    for wav in waveList:
        wavePath=os.path.join(path,wav)
        with contextlib.closing(wave.open(wavePath,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            totalLength+=duration
    return totalLength

def clean_phones(phones):
    phones = [p for p in phones.split(' ') if p != "." and p != ""]
    return phones

def readjson(LEResult):
    # 设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    mapping={}
    f = open(LEResult, encoding="utf-8")
    file = json.load(f)
    for i in file:
        #         print(i["sid"],i["phones"])
        mapping[i["sid"]]=i["phones"]
    return mapping

def checkDiff(in_data_path, out_data_path):
    f1=open(in_data_path,'r',encoding='utf-8')
    f2=open(out_data_path,'r',encoding='utf-8')
    l1=f1.readlines()
    l2=f2.readlines()
    diffLst = []
    for i in range(len(l1)):
        line1=l1[i].replace('n . a_h . a_l ','').replace( 'n . eh_h . i_l ','')
        line2=l2[i].replace('n . a_h . a_l ','').replace( 'n . eh_h . i_l ','')
        if line1!=line2:
            diffLst.append(l1[i].split("|")[0])
    f1.close()
    f2.close()
    return diffLst

def getUpdProportion(mapping):
    updateCount=0
    for i in mapping.values():
        if 'n eh_h i_l' in i:
            updateCount += 1
    return str(updateCount/len(mapping.keys())*100)[:5]+"%"