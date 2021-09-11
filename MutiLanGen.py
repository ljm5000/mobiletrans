import os
import json
import time
import random
import argparse
from google_trans_new import google_translator  

translator =  google_translator(timeout=30)
langArray = ["en","ja","ko","de","es","fr","it","pl","ru","th","tr","vi"]
def analyzeStrings(filePath):
    with open(filePath) as f:
        array = f.readlines()
        f.close()
    print(len(array))

def cleanStr(tmp,os="ios"):
    if os == "ios":
        return tmp.replace("\"","").replace("\n","").replace(" ","").replace(";","")
    elif os == "and":
        #  <string name="about">关于</string>
        f = tmp.replace("<string name=\"","").replace("\">","=").replace("\"","").replace("\n","").replace(";","").replace("</string>","")
        return f
        
    else:
        # lang: 'English',
        return tmp.replace("\n","").replace(" ","").replace(":","=")

def getKeysFromLocalStr(tmp,os="ios"):
    total = cleanStr(tmp,os)
    array = total.split("=")
    return array[0]

def googleTrans(target,lan):
    try:
        rel = translator.translate(target,lang_tgt=lan)
        print(target,rel)
    except:
        print("get error")
        time.sleep( random.randint(1,10))
        rel = googleTrans(target,lan)
    envalue = rel
    if type(rel) == list:
        envalue = rel[0] 

    return envalue.replace(" ","")

def analyzeSimpleChinese(filePath):
    
    with open(filePath) as f:
        array = f.readlines()
        f.close()
    result = []
    result_en = []
    for tmp in array:
        if tmp.find("=") < 0:
            continue
        tarray = tmp.split("=")
        key = cleanStr(tarray[0])
        value = cleanStr(tarray[1])
        rel = {key:value}
        if value == None:
            print("get none",key,value)
            continue
        dic={}
        for lan in langArray:
            dic[key+lan] = googleTrans(value,lan)
            
        result_en.append(dic)
        
    with open("f2.json","w") as f:
        json.dump(result_en,f,indent=2,ensure_ascii = False)
        f.close()

    with open("f.json","w") as f:
        json.dump(result,f,indent=2,ensure_ascii = False)
        f.close()

def trans_to_lan(tmpDic,lan = "en",isWritten = False):
    enDic = {}
    for item in tmpDic:
        v = tmpDic[item]
        enDic[item] = googleTrans(v,lan)

    if isWritten:
        with open("en.json","w") as f:
            json.dump(enDic,f,indent=2,ensure_ascii = False)
            f.close()
    return enDic

def writeToAndroid(filepath,rel):
    for lan in rel:
        filePath = "{0}_strings.xml".format(lan)
        contents = []
        for key in rel[lan]:
            if os.path.exists(filePath):
                with open(filePath,'r') as f:
                    contents = f.readlines() 
                    f.close()
            else:
                contents = ["<resources>\n","</resources>\n"]
            
            isFindKey = False
            for line in contents:
                if len(line) > 0:
                    comp = getKeysFromLocalStr(line,"and")
                    if comp == key:
                        isFindKey = True
                        break
            
            if isFindKey:
                print("已经存在key:",key)
                continue
            index = 0
            tar_str = "<string name=\"{0}\">{1}</string>\n".format(key,rel[lan][key])
            for line in contents:
                if len(line) > 0:
                    comp = cleanStr(line,"and")
                    if comp.startswith(key[0:6]):
                        break
                index = index + 1
            if index == len(contents):
                index = len(contents) -1
            contents.insert(index,tar_str)
            f = open(filePath, "w")
            tmp = "".join(contents)
            f.write(tmp)
            f.close()

def writeToJS(path,rel):
    for lan in rel:
        filePath = os.path.join(path,"{0}.js".format(lan))
        contents = []
        for key in rel[lan]:
            if os.path.exists(filePath):
                with open(filePath,'r') as f:
                    contents = f.readlines() 
                    f.close()
            else:
                contents = ["export default {\n","}\n"]
            
            isFindKey = False
            for line in contents:
                if len(line) > 0:
                    comp = getKeysFromLocalStr(line,"h5")
                    if comp == key:
                        isFindKey = True
                        break
            
            if isFindKey:
                print("已经存在key:",key)
                continue
            index = 0
            tar_str = "{0} : '{1}',\n".format(key,rel[lan][key])
            # for line in contents:
            #     if len(line) > 0:
            #         comp = cleanStr(line,"h5")
            #         if comp.startswith(key[0:6]):
            #             break
            #     index = index + 1
            
            index = len(contents) -1
            contents.insert(index,tar_str)
            f = open(filePath, "w")
            tmp = "".join(contents)
            f.write(tmp)
            f.close()

def writeToiOS(filepath,rel):

    for lan in rel:
        filePath = "{0}/{1}.lproj/Localizable.strings".format(filepath,lan)
        for key in rel[lan]:
            with open(filePath,'r') as f:
                contents = f.readlines() 
                f.close()
            
            isFindKey = False
            for line in contents:
                if len(line) > 0:
                    comp = getKeysFromLocalStr(line)
                    if comp == key:
                        isFindKey = True
                        break
            
            if isFindKey:
                print("已经存在key:",key)
                continue
            index = 0
            tar_str = "\"{0}\" = \"{1}\";\n".format(key,rel[lan][key])
            for line in contents:
                if len(line) > 0:
                    comp = cleanStr(line)
                    if comp.startswith(key[0:6]):
                        break
                index = index + 1
            
            contents.insert(index,tar_str)
            f = open(filePath, "w")
            tmp = "".join(contents)
            f.write(tmp)
            f.close()

def beginTranslate(filepath,osType):
    armJson = "arm.json"
    with open(armJson) as f:
        chinDic = json.load(f)

    #以简体中文为入口文件->转为英文
    en_Dic = trans_to_lan(chinDic["zh"],"en",True)
    #以简体中文->转为繁体
    tradChin_Dic = trans_to_lan(chinDic["zh"],"zh-TW",False)
    
    #英文->联通所有语言
    rel = {}
    rel["zh-Hant"] = tradChin_Dic
    rel["zh-Hans"] = chinDic["zh"]
    for enKey in en_Dic:
        value = en_Dic[enKey]
        for lan in langArray:
            if lan not in rel:
                rel[lan] = {}    
            rel[lan][enKey] = googleTrans(value,lan)
    
    ##留存结果
    with open("total.json","w") as f:
        json.dump(rel,f,indent=2,ensure_ascii = False)
        f.close()
    
    if osType == "ios":
        writeToiOS(filepath,rel)

    elif osType == "and":
        writeToAndroid(filepath,rel)
    else:
        writeToJS(filepath,rel)
    

def main():
    parser = argparse.ArgumentParser(description='Search some files')
    parser.add_argument(dest='os',metavar='os')
    parser.add_argument(dest='path',metavar='path')
    args = parser.parse_args()

    if args.os == None:
        print("os can't be null")
        return

    if args.path == None:
        print("path can't be null")
        return

    print(args.os)
    
    print("start to anlayze:",args.path)
    beginTranslate(args.path,args.os)
    

if __name__ == '__main__':
    main()

    