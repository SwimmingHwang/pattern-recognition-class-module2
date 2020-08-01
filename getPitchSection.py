import parselmouth


import numpy as np

import pandas as pd
from pandas import DataFrame as df
import statistics


def getPitchSection(snd):

    pitch = snd.to_pitch()
    #잡음 상쇄기술
    pre_emphasized_snd = snd.copy()
    pre_emphasized_snd.pre_emphasize()
    #
    pitch_time=pitch.xs()
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan

    df_pitch=df(data={'time' :pitch_time,'pitch': pitch_values})

    #nan없애기
    df_pitch=df_pitch.dropna(how='any')

    pitch_row=len(df_pitch.index)

    pitch_start_time = df_pitch['time'].values[0]
    pitch_end_time =  df_pitch['time'].values[pitch_row-1]

    return pitch_start_time, pitch_end_time