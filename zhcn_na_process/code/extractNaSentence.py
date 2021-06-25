import codecs
import os
import re
import shutil
from os import listdir
import utils

def getDir(wavePath,sid):
    path = wavePath
    for i in listdir(path):
        if sid[2:4] == i[:2]:
            return i

def str_insert(str_origin, pos, str_add):
    str_list = list(str_origin)    # 字符串转list
    str_list.insert(pos, str_add)  # 在指定位置插入字符串
    str_out = ''.join(str_list)    # 空字符连接
    return str_out

def copyWave(wavePath, newWaveFolder, sid):
    shutil.copy(os.path.join(wavePath,getDir(wavePath,sid),sid[2:]+".wav"),
                os.path.join(newWaveFolder, sid+".wav"))

def extractNaSentence(originalTrainTxt, outDataPath,wavePath):
    in_data_path = originalTrainTxt
    out_data_path = os.path.join(outDataPath,"na_result.txt")
    word_path=os.path.join(outDataPath,"na_word.txt")
    newWaveFolder = os.path.join(outDataPath,"waves")
    if not os.path.exists(newWaveFolder):
        os.mkdir(newWaveFolder)
    fs_out = open(out_data_path, "a+", encoding="utf-8")
    word_out = open(word_path, "a+", encoding="utf-8")
    target = "那"
    target_phone = []
    word_list=[]
    with codecs.open(in_data_path, "r", encoding="utf-8") as in_data:
        for line in in_data.readlines():
            if line.strip() == "":
                continue
            line_split = line.strip().split('|')
            sid = line_split[0].split('.')[0].strip()
            text = line_split[2].replace(" ", "").replace("......", "…").replace("...", "…").replace("——", "…").replace("……", "…").strip()
            text_list=list(text)
            phones = line_split[3].strip()
            phones_update = " ".join(utils.clean_phones(phones))
            target_pos = [substr.start() for substr in re.finditer(target, text.replace('那儿','义斌').replace('那么','义斌'))]
            if len(target_pos) == 0:
                continue
            copyWave(wavePath,newWaveFolder,sid[4:])
            syl_phones = []
            for phone in phones_update.split("/"):
                phone = phone.strip()
                for syl_phone in phone.split("-"):
                    syl_phone = syl_phone.strip()
                    if syl_phone.find("zzz") >= 0:
                        syl_phones.append(" ".join(syl_phone.split(' ')[:2]))
                        syl_phones.append(syl_phone.split(' ')[-1])
                    else:
                        syl_phones.append(syl_phone)
            if len(syl_phones) != len(text):
                print("%s phone and syl not consist" % sid)
            else:
                out_str = ""
                for i in range(len(target_pos)):
                    phone = syl_phones[target_pos[i]].strip()
                    word=''.join(text_list[target_pos[i]+i:target_pos[i]+i+2])
                    if word not in word_list:
                        word_list.append(word)
                        word_out.write(word+"\n")
                    text_list.insert(target_pos[i]+1+i, '{{'+phone+'}}')
                    if len(phone.split(' ')) != 3:
                        continue
                    if phone not in target_phone:
                        target_phone.append(phone)
                out_str = sid[4:] + '\t' + ''.join(text_list)
                fs_out.write(out_str+"\n")
    word_out.close()
    fs_out.close()