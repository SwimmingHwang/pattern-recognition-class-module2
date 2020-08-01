import os
from pandas import DataFrame as df

from getFormant import *
from getPitchFlow import *
from getPitchSection import*
from getInterval_PandF import *
from getF1Max import *
from getIntensity import *
def main():

    #C:\Users\Hwang\Desktop\sound\testsound

    #C:\Users\Hwang\Desktop\sound\0.5sec_test\0.5
    # C:\Users\Hwang\Desktop\sound\0.5sec_test\1
    # C:\Users\Hwang\Desktop\sound\0.5sec_test\2.0

    #C:\Users\Hwang\Desktop\sound\test\test1
    #C:\Users\Hwang\Desktop\sound\test\test2
    #C:\Users\Hwang\Desktop\sound\test\test3
    path_dir = "C:\\Users\\Hwang\\Desktop\\sound\\p\\"
    file_list = os.listdir(path_dir)

    #list - soundlist
    #dictionary - soundinfo
    soundlist=[]


    for idx,item in enumerate(file_list):
        print("----------"+item+"----------")

        # group
        # F1max and interval_PandF
        # [0] 9
        # [1] high and vowal  0
        # [2] low and consonant 7
        # [3] low and vowel 1 2 5 6
        # [4] high and consonant 3 4 8

        #Initialize
        soundinfo = {'file_name':item ,'pitchSection' : [None,None] ,'diffF2F3' : None,
                     'interval_PandF': None ,'F1max' : None ,'diffF2F1' : None,
                     'group' : None , 'answer' :None}

        soundlist.append(soundinfo)
        snd = parselmouth.Sound(path_dir+soundlist[idx]['file_name'])

        sound_start_time = getIntensity(snd)

        #continue
        #RETURN 9
        #F2와 F3의 차이가 2000보다 큰 수

        soundlist[idx]['pitchSection']=getPitchSection(snd)
        soundlist[idx]['diffF2F3']=getDiffF2F3(snd,soundlist[idx]['pitchSection'])

        if(soundlist[idx]['diffF2F3']>1900):
            soundlist[idx]['group']=0
            soundlist[idx]['answer'] = 9
        print("F2와 F3의 차이 :" ,soundlist[idx]['diffF2F3'])


        #RETURN 0 7
        # 모음 높은 group
        df_formant = getFormant_all(snd,soundlist[idx]['pitchSection'][0],soundlist[idx]['pitchSection'][1])
        if(getFrontorEnd(df_formant)=="front"):
            print("FRONT")
            soundlist[idx]['interval_PandF'] = getInterval_PandF(snd,soundlist[idx]['pitchSection'][0],soundlist[idx]['pitchSection'][1],1)
            print("Pitch시작과 포먼트 시작점의 차이 : ", soundlist[idx]['interval_PandF'])
        else :
            print("EMD")
            soundlist[idx]['interval_PandF'] = getInterval_PandF(snd,soundlist[idx]['pitchSection'][0],soundlist[idx]['pitchSection'][1],2)
            print("Pitch시작과 포먼트 시작점의 차이 : ", soundlist[idx]['interval_PandF'])

        soundlist[idx]['F1max'] = getF1MaxDiv(snd,soundlist[idx]['pitchSection'][0],soundlist[idx]['pitchSection'][1])
        print("F1 최댓값의 높은그룹 or낮은 그룹 : ",   soundlist[idx]['F1max'] )


        #grouping
        if(soundlist[idx]['interval_PandF'] < 2.5 and soundlist[idx]['F1max'] =="high" and soundlist[idx]['answer'] == None) :# 모음(vowel) 높 0
            soundlist[idx]['group'] =  1
            soundlist[idx]['answer'] = 0
        elif (soundlist[idx]['interval_PandF'] < 2.5 and soundlist[idx]['F1max'] =="low" and soundlist[idx]['answer'] == None): # 모음 낮 1256
            soundlist[idx]['group'] = 3
        elif (soundlist[idx]['interval_PandF'] >=2.5 and soundlist[idx]['F1max'] =="low" and soundlist[idx]['answer'] == None): # 자음 낮 7
            soundlist[idx]['group'] = 2
            soundlist[idx]['answer'] = 7
        elif (soundlist[idx]['interval_PandF'] >=2.5 and soundlist[idx]['F1max'] =="high" and soundlist[idx]['answer'] == None): # 자음 높 348
            soundlist[idx]['group'] = 4


        # RETURN 5
        soundlist[idx]['pitchSection'] = getPitchSection(snd)
        soundlist[idx]['diffF2F1'] = getDiffF2F1(snd, soundlist[idx]['pitchSection'])

        if (soundlist[idx]['diffF2F1'] < 800 and soundlist[idx]['group']==3 and soundlist[idx]['answer'] == None):
            soundlist[idx]['answer'] = 5
        print("F2와 F1의 차이 :", soundlist[idx]['diffF2F1'])

        # RETURN 126     348
        if(soundlist[idx]['group']==3  and soundlist[idx]['answer'] == None ) :
            soundlist[idx]['answer'] = getPitchFlow(snd)

        if(soundlist[idx]['group']==4 and soundlist[idx]['answer'] == None ) :
            var=0
            if (getFrontorEnd(df_formant) == "front"):
                val = getInterval_PandF(snd,soundlist[idx]['pitchSection'][0],soundlist[idx]['pitchSection'][1] ,1)
            else :
                val = getInterval_PandF(snd, soundlist[idx]['pitchSection'][0], soundlist[idx]['pitchSection'][1], 2)
            print(val)
            if (int(val) == 5 ) :
                soundlist[idx]['answer']= 3
            elif (int(val) == 3 ) :
                soundlist[idx]['answer']= 4
            elif (int(val) == 7 ) :
                soundlist[idx]['answer']= 8
            else :
                print("ERROR 3/4/8")
                soundlist[idx]['answer'] = -1




        # 정답 한꺼번에 출력
    for idx, item in enumerate(file_list):
        print(item," : ",soundlist[idx]['answer'] , "group : " ,soundlist[idx]['group'] )



if __name__ == "__main__":
    # execute only if run as a script
    main()