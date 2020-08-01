import parselmouth

import glob
import os

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
from pandas import DataFrame as df
import statistics


from parselmouth.praat import call
from scipy.stats.mstats import zscore
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


from getPitchSection import *


#4개 포먼트가 모두 정의된 포먼트 얻기 (pitch가 정의되지 않은 구간도 포함 ) - 피치시작 포먼트 시작 구간 구하기 위해
def getFormant_all(snd,pitch_start_time, pitch_end_time) :
    # formang setting
    formant = snd.to_formant_burg(max_number_of_formants=4)
    time_step = formant.get_time_step()
    first_time = formant.get_time_from_frame_number(1)
    nof = formant.get_number_of_frames()
    formant_time = []

    F1_values = []
    F2_values = []
    F3_values = []
    F4_values = []

    time = first_time

    for i in range(nof):
        formant_time.append(time)

        F1_values.append(formant.get_value_at_time(1, time, "HERTZ"))
        F2_values.append(formant.get_value_at_time(2, time, "HERTZ"))
        F3_values.append(formant.get_value_at_time(3, time, "HERTZ"))
        F4_values.append(formant.get_value_at_time(4, time, "HERTZ"))
        time = time + time_step

    df_formant = df(data={'time': formant_time, 'F1': F1_values, 'F2': F2_values, 'F3': F3_values, 'F4': F4_values})
    print("time size : "  ,df_formant['time'].size)
    # F1 F2 F3 F4 중 하나라도 undefined 이면 필터링하기
    df_formant = df_formant.dropna()
    return df_formant



#pitch 정의구간으로 필터링한 포먼트 얻기
def getFormant(snd,pitch_start_time, pitch_end_time) :

    #formang setting
    formant=snd.to_formant_burg(max_number_of_formants=4)
    time_step=formant.get_time_step()
    first_time=formant.get_time_from_frame_number(1)
    nof=formant.get_number_of_frames()
    formant_time=[]

    F1_values=[]
    F2_values = []
    F3_values = []
    F4_values = []

    time=first_time

    for i in range(nof):
        formant_time.append(time)

        F1_values.append(formant.get_value_at_time(1,time,"HERTZ"))
        F2_values.append(formant.get_value_at_time(2, time, "HERTZ"))
        F3_values.append(formant.get_value_at_time(3, time, "HERTZ"))
        F4_values.append(formant.get_value_at_time(4, time, "HERTZ"))
        time=time+time_step

    df_formant=df(data={'time' : formant_time,'F1':F1_values ,'F2':F2_values ,'F3':F3_values ,'F4':F4_values })

    #pitch가 정의된 구간으로 formant값 정의
    df_formant = df_formant[df_formant.time > pitch_start_time]

    #F1 F2 F3 F4 중 하나라도 undefined 이면 필터링하기
    df_formant = df_formant.dropna()
    return df_formant


    #return df_formant['F'].quantile(.75)
    #return df_formant['F1'].max()

def getFrontorEnd(df_formant):
    if(round(df_formant['time'].values[df_formant['time'].size-1],1)==0.5):
        return "end"
    else :
        return"front"

def getDiffF2F3(snd,pitchSec):
    df_snd = getFormant(snd,pitchSec[0],pitchSec[1])
    res = df_snd['F3'].mean() - df_snd['F2'].mean()
    return res

def getDiffF2F1(snd,pitchSec) :
    df_snd = getFormant(snd,pitchSec[0],pitchSec[1])
    res = df_snd['F2'].mean() - df_snd['F1'].mean()
    return res
