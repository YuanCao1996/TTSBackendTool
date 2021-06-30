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

def getNaWaveProportion(naWavePath):
    lst=[
        r"D:\data\prcess_audiobook\FeatureExtract\CharacterVoice\xiaotang_narrative_erhua\Data\Wave16kNormalize",
        r"D:\data\prcess_audiobook\FeatureExtract\CharacterVoice\xiaotang_youngfemale_erhua\Data\Wave16kNormalize",
        r"D:\data\prcess_audiobook\FeatureExtract\CharacterVoice\xiaotang_youngmale_erhua\Data\Wave16kNormalize",
        r"D:\data\prcess_audiobook\FeatureExtract\Xiaotang_new_recording\ErHua\Data\Wave16kNormalize",
        r"D:\data\prcess_audiobook\FeatureExtract\Xiaotang_new_recording\Mixlingual\Data\Wave16kNormalize",
        r"D:\data\prcess_audiobook\FeatureExtract\Xiaotang_new_recording\ModalParticle\Data\Wave16kNormalize",
        r"D:\data\prcess_audiobook\FeatureExtract\hmtq_erhua\Data\Wave16kNormalize",
        r"D:\data\prcess_audiobook\FeatureExtract\jczy_erhua\Data\Wave16kNormalize"
    ]
    allLength=0
    for p in lst:
        folderList=listdir(p)
        if ".wav" in folderList[0]:
            wavePath=p
            allLength+=getWaveLength(wavePath)
            print(wavePath)
        else:
            for i in folderList:
                wavePath=os.path.join(p,i)
                allLength+=getWaveLength(wavePath)
                print(wavePath)
    return str(getWaveLength(naWavePath) / allLength * 100)[:5]+"%"

def addBookId():
    #add to train.txt
    path=r"D:\data\prcess_audiobook\FeatureExtract\Xiaotang_new_recording\ModalParticle\wav_mel\mel_0.05_0.1"
    f=open(os.path.join(path,"train.txt"),"r",encoding="utf-8")
    for line in f.readlines():
        #     print(line[0:4]+"20"+line[4:])
        with open(os.path.join(path,"train_reid.txt"),"a+",encoding="utf-8") as nf:
            nf.write(line[0:4]+"25"+line[4:])
    #         nf.write(line.strip()+"|"+"1"+"|"+str(int(line[4:6]))+"\n")
    f.close()
    nf.close()
    #add to waves
    path=r"D:\data\prcess_audiobook\FeatureExtract\Xiaotang_new_recording\ModalParticle\wav_mel\mel_0.05_0.1\mels"
    fileList=listdir(path)
    for file in fileList:
        oldFile=os.path.join(path,file)
        newName=file[0:4]+"25"+file[4:]
        #     newName=file[0:4]+file[6:]
        os.rename(oldFile,os.path.join(path,newName))