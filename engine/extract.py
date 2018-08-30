# -*- coding: utf-8 -*-
import json
import sys,os
sys.path.append("../")  
import config
import re
import jieba
import jieba.analyse
import textwrap
from functools import reduce


def clear_up(file_name):
    
    data_collection=[]
    with open(file_name) as file:
        for line in file:
            data_collection.append(json.loads(line))
    _load_dicts()
    documents = []

    for data in data_collection:

        ID = data["_id"]

        text_body = _get_cleaned_text(data)
        
        jybg = json.loads(data["original_jybg_data"])["jybg"]
        if len(jybg)!=0:
            name = _get_name(jybg[0])
            date = _get_date(jybg[0])
        
        #jyxm = _get_value(dicts[0],text_body)[0]
        jyxm = _get_jybg(data)[0]
        #tags = _get_value(dicts[0],text_body)[1]
        tags = _get_jybg(data)[1]
        tags = _get_tag(text_body, tags)

        document = {}
        document["id"] = ID
        document["name"] = name
        document["date"] = date
        document["text_body"] = text_body
        document["tags"] = tags
        document["jyxm"] = jyxm

        documents.append(document)

    _dump(documents)

def refresh():
    '''refresh after updating dictionaries.
    '''
    _load_dicts()
    clear_up()


def exist(term):
    status = False
    with open(config.path["check_terms"],'r') as file:
        for line in file:
            if term in line:
                status = True
                return status

def _load_dicts():

    global userDict
    global mediDict
    global checkDict
    global stopDict

    userDict = open(config.path["userdict"],'r')
    mediDict = open(config.path["medi"],'r')
    checkDict = open(config.path["check_terms"],'r')
    stopDict = open(config.path["stop_words"],'r')


def _dump(documents):
    
    try:
        with open('../data/medical_records.json', 'w') as json_file:
            json_file.write(json.dumps(documents,ensure_ascii = False))
        print("SUCEEDED CLEARING UP.")

    except:
        print("FAILED CLEARING UP JSON...")
    
    finally:
        print("DUMPING COMPELETED.")


def _get_cleaned_text(data):
    '''
    A list of readable strings for rechecking terms
    '''
    #================helper function=====================
    def _getStr(num):
    
        raw = data["dzbl"][num]["txt_record"]
        chunk = raw.replace("&nbsp;","")
        reg = re.compile('<[^>]*>')
        chunk = reg.sub('',chunk)
        chunk = textwrap.fill(chunk, width=10000)
        
        return chunk

    #==================main function=======================

    text = ""
    for i in range(0,len(data["dzbl"])):
        text = text + _getStr(i) +"\n\n"

    return text


def _get_name(jybg):

    name = jybg["patient_name"]
    return name


def _get_date(jybg):
    
    date = jybg["req_time"]
    return date
    

def _float(s):
    '''changes string to float
    '''
    #=================helper functions=======================
    def _char2num(s):
        return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]
    
    def _str2int(s):
        return reduce(lambda x,y:x*10+y,map(_char2num,s))
    
    def _intLen(i):
        return len('%d'%i)
    
    def _int2dec(i):
        return i/(10**_intLen(i))

    #========================================
    return reduce(lambda x,y:x+_int2dec(y), map(_str2int,s.split('.')))

    
def _divide_Text(text):
    '''
    returns the divided text
    '''
    jieba.load_userdict(medi)
    jieba.load_userdict(userdict)
    seg_list = jieba.cut(text, cut_all=False)
    return seg_list


def _is_uchar(uchar):
    '''
    checks if a char is chi/eng/num
    '''
    # if chinese
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    # if num
    if uchar >= u'\u0030' and uchar<=u'\u0039':
            return False        
    # if eng
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
            return False
    
    return False


def _get_value(dict,text_body):

    '''
    documents checks and values of the patient. data stored in the form of 

        jyxm = {"term1":[ [num1(float) , prop1(str)],
                          [num2(float) , prop2(str)],
                                  ...
                        ];
                "term2":[ [num1(float) , prop1(str)],
                          [num2(float) , prop2(str)],
                                  ...   
                        ];
                "term3":[ [num1(float) , prop1(str)],
                          [num2(float) , prop2(str)],
                                      ...          
                        ];  
              }
    '''

    terms=[]

    file = open(dict,'r')
    for line in file:
        if len(line)>1:
            terms.append(line.replace("\n",''))

    #for putting into tag[]
    termlist = []
    #检验项目
    jyxm={}
    #number values
    numPattern = re.compile(r'[0-9.]+')
    #positive/negative
    propPattern = re.compile(r'[\(（][阴性]*[阳性]*[\)）]')
    #categories names that don't have values
    catPattern = re.compile("[:：](.*?)[:：]")

    # loop thru all terms in the provided list
    for term in terms:
        
        time = text_body.count(term)
        termPattern = re.compile(re.escape(term))

        #if the term appears for more than once
        if time>=1:
            termlist.append(term)
            # check if the term is a category
            firstIndex = text_body.find(term)
            followingTerm = catPattern.search(text_body[firstIndex+1:]).group()
            FTcleaned = followingTerm.replace("：","").replace(":","").replace(" ","")

            # if the term is not a category, then get its corresponding value
            if not FTcleaned in terms:
                # document the value
                values=[]

                for match in re.finditer(termPattern,text_body):
                    
                    value = []
                    index = match.span()[1]
                    num = numPattern.search(text_body[index+1:])
                    prop = propPattern.search(text_body[index+1:])
                    
                    if num:
                        value.append(float(num.group()))
                    if prop:
                        value.append(prop.group())
                    if value and not value in values:
                        values.append(value)
                        
                if values!=[]:        
                    jyxm[term] = values

    return [jyxm,termlist]        


def _get_tag(text,tags):
    '''
    extract tags from the cleaned text
    '''   
    jieba.analyse.set_stop_words(config.path["check_terms"])

    n = len(text)//5
    res = jieba.analyse.extract_tags(text, topK=n)
    
    for tag in res:
        # get rid of numbers and engs and 1-digi-long chars
        if _is_uchar(tag) and len(tag)>2 and tag not in tags:
            tags.append(tag)
   
    #userdict
    for line in userDict:
        userTerm = line.replace("\n",'')
        if len(line)>1 and text.count(userTerm)>1 and not userTerm in tags:
            tags.append(userTerm)
    
    #mediDict
    for line in mediDict:
        mediTerm = line.replace("\n",'')
        if len(line)>1 and text.count(mediTerm)>1 and not mediTerm in tags:
            tags.append(mediTerm)
            
    #stop
    for line in stopDict:
        stopTerm = line.replace("\n",'')
        if stopTerm in tags:
            tags.remove(stopTerm)

    return tags


def _get_jybg(data):
    
    # for extracting numerical results
    numPattern = re.compile(r'[0-9]+[.]?[0-9]+')
    termlist = []

    #检验报告
    jybg = data["jybg"]
    result = {}

    for time in range(0,len(jybg)):
        jyxm = jybg[time]["lDetails"]
        for i in range(0,len(jyxm)):
            if "report_result" in jyxm[i]:
                termlist.append(jyxm[i]['item_name'])
                report_result = jyxm[i]['report_result']
                value = numPattern.search(report_result)
                if value:
                    if "阴性" in report_result:
                        result[jyxm[i]['item_name']] = -float(value.group())
                    else:
                        result[jyxm[i]['item_name']] = float(value.group())
                else: 
                    pass

    return [result,termlist]
