from pandas import DataFrame as df

def getIntensity(snd):
    intensity = snd.to_intensity(minimum_pitch=75)
    time_step = intensity.get_time_step()
    first_time = intensity.get_time_from_frame_number(1)
    nof = intensity.get_number_of_frames()
    intensity_time = []

    time = first_time

    intensity_values =[]

    for i in range(nof):
        intensity_time.append(time)

        #intensity_values.append(intensity.get_value(1, time, "CUBIC"))
        #    F1_values.append(formant.get_value_at_time(1, time, "HERTZ"))
        intensity_values.append(intensity.get_value(time,"CUBIC"))
        time = time + time_step

    #get_value(self: parselmouth.Intensity, time: float, interpolation: parselmouth.Interpolation=Interpolation.CUBIC) → float


    #-300 filtering
    #df_formant = df_formant[df_formant.time > pitch_start_time]
    df_intensity = df(data={'TIME':intensity_time , 'INTENSITY': intensity_values })
    df_intensity = df_intensity[df_intensity.INTENSITY > 0]
    print(df_intensity['INTENSITY'].mean())
    print (df_intensity['INTENSITY'].quantile(.25))
    if(df_intensity['INTENSITY'].quantile(.25) < df_intensity['INTENSITY'].mean()) :
        df_intensity = df_intensity[df_intensity.INTENSITY > df_intensity['INTENSITY'].quantile(.25)]

    #print(df_intensity)

    return df_intensity['TIME'].values[0]