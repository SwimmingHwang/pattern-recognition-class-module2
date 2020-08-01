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



def getF1Max(snd,pitch_start_time, pitch_end_time) :

    #formang setting
    formant=snd.to_formant_burg(max_number_of_formants=4)
    time_step=formant.get_time_step()
    first_time=formant.get_time_from_frame_number(1)
    nof=formant.get_number_of_frames()
    formant_time=[]
    F1_values=[]
    time=first_time
    for i in range(nof):
        formant_time.append(time)
        F1_values.append(formant.get_value_at_time(1,time,"HERTZ"))
        time=time+time_step
    df_formant=df(data={'time' : formant_time,'F1':F1_values})
    #pitch가 정의된 구간으로 formant값 정의
    df_formant = df_formant[df_formant.time > pitch_start_time]
    #print(df_formant)
    #데이터의 75%가 이 값보다 작거나 같음.
    #사실상  max가 아니라 75의 max
    return df_formant['F1'].quantile(.75)
    #return df_formant['F1'].max()



def getF1MaxDiv(snd,start_point, end_point ):

    F1maxVal = getF1Max(snd, start_point, end_point)
    print("F1maxVal : ", F1maxVal)
    if (F1maxVal > 600):
        return "high"
    else:
        return "low"



