import json
from pprint import pprint
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyDXDjtp2LFKmm19g5geNng4xFfpLubAECc')
# User need to input the file name
coordinate_filename = 'a json FILE'
allsubInfor_filename = 'a jSON FILE'
analysis_file = 'a Json File'
# function API
sublist=[]
def get_subInfo_by_coord():
    with open(coordinate_filename,'r',encoding='UTF-8') as getcoord:
        coord_info = json.load(getcoord)
    for i in coord_info:
        if i['coordinates'] == [0, 0]:
            continue
        else:
            tu_coord = tuple((i['coordinates'][0],i['coordinates'][1]))
            subInfo = get_sub_name(tu_coord)
def get_sub_name(sub):
    reverse_geocode_result = gmaps.reverse_geocode(sub)
    for i in reverse_geocode_result[0]['address_components']:
        if i['types'] == ['locality', 'political']:
            subname = i['long_name']
            subname = subname.upper()
            print(subname)
        else:
            subname = None
    return subname



def get_eduInfo_(what_sub_info):
    with open('education.json', 'r', encoding='UTF-8') as lovely:
        edu = json.load(lovely)
        edu_level=0
        for i in edu:
            if i.upper() == what_sub_info:
                edu_level = edu[i]
    return edu_level

def get_neg_num(what_sub_info):
    with open(analysis_file, 'r', encoding='UTF-8') as lovely:
        score = json.load(lovely)
        neg_num = 0
        for i in score:
            if i == what_sub_info:
                neg_num = score[i][1]

    return neg_num

def get_pos_num(what_sub_info):
    with open(analysis_file,'r',encoding='UTF-8') as lovely:
        score = json.load(lovely)
        pos_num = 0
        for i in score:
            if i == what_sub_info:
                pos_num=score[i][0]

    return pos_num

def get_score_(what_sub_info):
    with open(analysis_file,'r',encoding='UTF-8') as lovely:
        score = json.load(lovely)
        score_num = 0
        for i in score:
            if i == what_sub_info:
                pos_num=score[i][0]
                neg_num=score[i][1]

                if (pos_num == 0 and neg_num == 0): # 0 can not be zero... so we just ignore this situation
                    score_num = 0
                elif pos_num == neg_num:
                    score_num = 10086
                else:
                    score_num = (pos_num - neg_num)/(pos_num + neg_num)
    score_num = round(score_num,2)
    return score_num

def set_color_by_score(what_score):
    if what_score == 0:
        color = "#FFFFFF"
    elif what_score == 10086:
        color = "#FFFF00"
    elif what_score < 0:
        if what_score <= -0.8:
            color = "#9A0F0F"
        elif what_score <= -0.6:
            color = "#FF0000"
        elif what_score <= -0.3:
            color = "#C43232"
        elif what_score <=-0.000001:
            color = "#B75757"
    else:
        if what_score >0.7:
            color="#31BF14"
        elif what_score > 0.5:
            color = "#31EE0C"
        elif what_score > 0.3:
            color ="#5DEB41"
        elif what_score > 0.00001:
            color = "#90DE80"

    return color


def coord__analysis():
    postArray = []

    with open(allsubInfor_filename, 'r',encoding='UTF-8') as inputFile1:
        sub_info = json.load(inputFile1)

    with open('new_suburb.txt','r',encoding='UTF-8') as subnames:
         for lines in  subnames:
             lines = lines.rstrip(",\n")
             sublist.append(lines)
    print("Starting Analysis File...(Please Wait for a long time)")
    for i in sub_info["features"]:
        for u in sublist:
            u= u.upper()
            sub_info = i['properties']['vic_loca_2']
            i['properties'] = {"vic_loca_2":sub_info,
                               "pos":get_pos_num(sub_info),
                               "neg":get_neg_num(sub_info),
                               "score": get_score_(sub_info),
                               "color": set_color_by_score(get_score_(sub_info)),
                               "edu": get_eduInfo_(sub_info)}

            sub_info = sub_info.upper()
            if u == sub_info:
                with open('sub.json', 'a+') as f:
                    print(str(i)+",",file=f)

    with open('sub.json','r',encoding='UTF-8') as f:
        with open('new.json', 'a+') as g:
            for lin in f:
                lin = lin.replace('\'','\"')
                lin = lin.rstrip('\n')
                print(lin, file=g)



                

def set_color_by_score_v2(what_score):
    if what_score == 0:
        color = "#32FF09"
    else:
        if what_score >=0.09:
            color="#FF0909"
        elif what_score > 0.07:
            color = "#FD7004"
        elif what_score > 0.05:
            color ="#FDFD04"
        elif what_score > 0.00001:
            color = "#10BACD"

    return color



def get_score_v2_(what_score):
    with open(analysis_file,'r',encoding='UTF-8') as lovely:
        score = json.load(lovely)
        num_score = 0
        for i in score:
            if i == what_score:
                num_score = score[i]

    return num_score



def coord__analysis_v2():
    postArray = []

    with open(allsubInfor_filename, 'r',encoding='UTF-8') as inputFile1:
        sub_info = json.load(inputFile1)

    with open('new_suburb.txt','r',encoding='UTF-8') as subnames:
         for lines in  subnames:
             lines = lines.rstrip(",\n")
             sublist.append(lines)
    print("Starting Analysis File...(Please Wait for a long time)")
    for i in sub_info["features"]:
        for u in sublist:
            u= u.upper()
            sub_info = i['properties']['vic_loca_2']
            i['properties'] = {"vic_loca_2":sub_info,
                               "score": get_score_v2_(sub_info),
                               "color": set_color_by_score_v2(get_score_v2_(sub_info)),
                               "edu": get_eduInfo_(sub_info)}

            sub_info = sub_info.upper()
            if u == sub_info:
                with open('sub.json', 'a+') as f:
                    print(str(i)+",",file=f)

    with open('sub.json','r',encoding='UTF-8') as f:
        with open('new.json', 'a+') as g:
            for lin in f:
                lin = lin.replace('\'','\"')
                lin = lin.rstrip('\n')
                print(lin, file=g)



coord__analysis_v2()


def acc_all ():
    with open(analysis_file,'r',encoding='UTF-8') as lovely:
        score = json.load(lovely)
    score_num = 0
    a=0
    b=0
    c=0
    j2 = 0
    j3 = 0
    j4 = 0
    j5 = 0
    j6 = 0
    j7 = 0
    j8 = 0
    edua = []


    for i in score:
        pos_num=score[i][0]
        neg_num=score[i][1]
        if (pos_num == 0 and neg_num == 0): # 0 can not be zero... so we just ignore this situation
            score_num = 0
        elif pos_num == neg_num:
            score_num = 10086
        else:
            score_num = (pos_num - neg_num)/(pos_num + neg_num)
        score_num = round(score_num,2)
        if score_num <0:
            a=a+1
        if score_num > 0:
            b=b+1
        if score_num == 10086:
            c=c+1
        if score_num < 0:
            edua.append(get_eduInfo_(i))


    for u in edua:
        if u < 0.3:
            j2 = j2 + 1
        elif u < 0.4:
            j3 = j3 + 1
        elif u < 0.5:
            j4 = j4 + 1
        elif u < 0.6:
            j5 = j5 + 1
        elif u < 0.7:
            j6 = j6 + 1
        elif u < 0.8:
            j7 = j7 + 1
        elif u < 0.9:
            j8 = j8 + 1

    print("edu_level 20% : "+str(j2)+"edu_level 30% : "+str(j3)+"edu_level 40% : "+str(j4)+"edu_level 50% : "+str(j5)+"edu_level 60% : "+str(j6)+"edu_level 70% : "+str(j7)+"edu_level 80% : "+str(j8))
    print("支持 ："+str(a)+"反对 :" +str(b)+"中立 :" +str(c))



def acc_all_v2 ():
    with open(analysis_file,'r',encoding='UTF-8') as lovely:
        score = json.load(lovely)
    score_num = 0
    a=0
    b=0
    c=0
    j2 = 0
    j3 = 0
    j4 = 0
    j5 = 0
    j6 = 0
    j7 = 0
    j8 = 0
    edua = []


    for i in score:
        num=score[i]

        if num <0.02:
            a=a+1
        if num >= 0.02 and num <0.05:
            b=b+1
        if num >= 0.05:
            c=c+1


        if num > 0.03:
            edua.append(get_eduInfo_(i))


    for u in edua:
        if u < 0.3:
            j2 = j2 + 1
        elif u < 0.4:
            j3 = j3 + 1
        elif u < 0.5:
            j4 = j4 + 1
        elif u < 0.6:
            j5 = j5 + 1
        elif u < 0.7:
            j6 = j6 + 1
        elif u < 0.8:
            j7 = j7 + 1
        elif u < 0.9:
            j8 = j8 + 1

    print("edu_level 20% : "+str(j2)+"edu_level 30% : "+str(j3)+"edu_level 40% : "+str(j4)+"edu_level 50% : "+str(j5)+"edu_level 60% : "+str(j6)+"edu_level 70% : "+str(j7)+"edu_level 80% : "+str(j8))
    print("支持 ："+str(a)+"反对 :" +str(b)+"中立 :" +str(c))

