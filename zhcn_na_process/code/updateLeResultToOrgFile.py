import codecs
import utils
import os
from os import listdir
import xml.dom.minidom
import re

# Apply LE's result to train.txt
def joinLine(line_split,syl_phones,phones):
    lst=[i.replace(' ',' . ') for i in syl_phones]
    wordnumList=[]
    for i in phones.split("/"):
        zzzn=len(re.findall('zzz',i))
        wordnumList.append(len(i.split('-'))+zzzn)
    newPhone=''
    start=0
    for wordnum in wordnumList:
        end=start+wordnum
        newWord=" - ".join(lst[start:end])
        start=end
        newPhone=newPhone+ " / " + newWord

    phone_update=newPhone[3:].replace('- zzz','. zzz')
    line_split[3]=phone_update
    #     print(line_split[3])
    #     print(phone_update)
    s=""
    for i in line_split:
        s+="|"+i.strip()
    return s[1:]

def updateToTrainTxt(originalTrainTxt, outDataPath, LEResult):
    in_data_path = originalTrainTxt
    out_data_path = os.path.join(outDataPath, "train_label.txt")
    fs_out = open(out_data_path, "a+", encoding="utf-8")
    target = "那"
    mapping = utils.readjson(LEResult)
    target_phone = []
    with codecs.open(in_data_path, "r", encoding="utf-8") as in_data:
        for line in in_data.readlines():
            if line.strip() == "":
                continue
            line_split = line.strip().split('|')
            sid = line_split[0].split('.')[0].strip()[6:]
            #         print(sid)
            if sid not in mapping.keys():
                fs_out.write(line.strip()+"\n")
                continue
            text = line_split[2].replace(" ", "").replace("......", "…").replace("...", "…").replace("——", "…").replace("……", "…").strip()
            text_list=list(text)
            phones = line_split[3].strip()
            phones_update = " ".join(utils.clean_phones(phones))
            target_pos = [substr.start() for substr in re.finditer(target, text.replace('那儿','义斌').replace('那么','义斌'))]
            if len(target_pos) == 0:
                continue
            #         print(target_pos)
            syl_phones = []
            for phone in phones_update.split("/"):
                phone = phone.strip()
                for syl_phone in phone.split("-"):
                    syl_phone = syl_phone.strip()
                    if syl_phone.find("zzz") >= 0:
                        #                     print(syl_phone.split(' ')[:2])
                        syl_phones.append(" ".join(syl_phone.split(' ')[:2]))
                        syl_phones.append(syl_phone.split(' ')[-1])
                    else:
                        syl_phones.append(syl_phone)
            if len(syl_phones) != len(text):
                print("%s phone and syl not consist" % sid)
            else:
                na=0
                for target_id in target_pos:
                    syl_phones[target_id]=mapping[sid][na]
                    na+=1
                fs_out.write(joinLine(line_split,syl_phones,phones)+"\n")
    fs_out.close()
    errorLst = utils.checkDiff(in_data_path, out_data_path)
    if len(errorLst) > 0:
        print("Some error need check!")
        print(errorLst)
    else:
        print("Success!")
        print(utils.getUpdProportion(mapping))

def updateToXml(xmlPath,outDataPath, LEResult):
    xmlList=listdir(xmlPath)
    target="那"
    count=0
    mapping = utils.readjson(LEResult)
    newXmlPath = os.path.join(outDataPath, "xml")
    if not os.path.exists(newXmlPath):
        os.mkdir(newXmlPath)
    for xmlfile in xmlList:
        out_file = os.path.join(newXmlPath, xmlfile)
        count+=1
        xmlFile=os.path.join(xmlPath,xmlfile)
        DOMTree = xml.dom.minidom.parse(xmlFile)
        collection = DOMTree.documentElement
        sicltLst=collection.getElementsByTagName("si")
        for siclt in sicltLst:
            sid=siclt.getAttribute("id")
            if sid not in mapping.keys():
                continue
            newPhoneList=mapping[sid]
            sent=siclt.getElementsByTagName("sent")[0]
            text = siclt.getElementsByTagName('text')[0]
            txt=text.childNodes[0].data
            txt = txt.replace(" ", "").replace("......", "…").replace("...", "…").replace("——", "…").replace("……", "…").strip()
            target_pos = [substr.start() for substr in re.finditer(target, txt.replace('那儿','义斌').replace('那么','义斌'))]
            if len(target_pos)<=0:
                continue
            words=sent.getElementsByTagName('words')[0]
            newPhoneIndex=0
            for naIndex in target_pos:
                phoneIndex=0
                for word in words.getElementsByTagName('w'):
                    phone=word.getAttribute("p")
                    if naIndex == phoneIndex:
                        naNew=newPhoneList[newPhoneIndex].replace(" "," . ")
                        newPhone=phone.replace('n . a_h . a_l',naNew)
                        word.setAttribute("p",newPhone)
                    phoneIndex+=len(phone.split("-"))+len(re.findall('zzz',phone))
        with open(out_file,'w',encoding='utf-16') as fh:
            DOMTree.writexml(fh,encoding='utf-16')
        fh.close()

