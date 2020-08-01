# pitch 정의 시작구간과 formant정의 시작구간 차이
# threshold = 0.025 ==> 3번째에서 반올림 X 100
# 0 1 2 3 4 5 6 7 8 9
# 0 0 0 5 3 1 0 3 7 4
# vowel 모음 / consonant 자음
from getFormant import *

def getInterval_PandF(snd ,start_time,end_time,type):
    pre_emphasized_snd = snd.copy()
    pre_emphasized_snd.pre_emphasize()
    formant=pre_emphasized_snd.to_formant_burg(max_number_of_formants=4 )
    df = getFormant_all(snd,start_time,end_time)
    if(type ==2) :
        formant_time = df['time'].values[40]
    else :
        formant_time = df['time'].values[0]
    #print(df)

    #print(formant_time)
    test_threshold = round(start_time - formant_time, 3) * 100

    print(test_threshold)
    if test_threshold >= 2.5:
        print("자음으로 시작")
    #    return consonant
    else:
        print("모음으로 시작")
    #    return vowel
    return test_threshold