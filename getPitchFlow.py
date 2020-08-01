import parselmouth

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#sns.set()  # Use seaborn's default style to make attractive graphs

# Plot nice figures using Python's "standard" matplotlib library
#snd = parselmouth.Sound("number/test/6-1.wav")


def getPitchFlow(snd):
    pitch = snd.to_pitch()



    pitch_values = pitch.selected_array['frequency']
    for i in range(len(pitch_values)):  # 100Hz 이하 pitch제거
        if (pitch_values[i] < 100):
            pitch_values[i] = 0
    start = 0
    while pitch_values[start] == 0:
        start += 1
    end = len(pitch_values) - 1
    while pitch_values[end] == 0:
        end -= 1;

    pitchsize = end - start + 1
    pitchsize = int(pitchsize / 4)
    pitchtime = [start, start + pitchsize, start + (pitchsize * 2), start + (pitchsize * 3), end]
    pitchtime_values = [pitch_values[pitchtime[0]], pitch_values[pitchtime[1]], pitch_values[pitchtime[2]],
                        pitch_values[pitchtime[3]], pitch_values[pitchtime[4]]]
    result = [pitchtime_values[1] - pitchtime_values[0], pitchtime_values[2] - pitchtime_values[1],
              pitchtime_values[3] - pitchtime_values[2], pitchtime_values[4] - pitchtime_values[3]]

    if(result[0] > 0 and result[1] >0 and result[2] >0 and result[3] <0 ) :
        return 1
    elif (result[0] > 0 and result[1] <0 and result[2] <0 and result[3] > 0 ) :
        return 2
    elif (result[0] > 0 and result[1] >0 and result[2] < 0 and result[3] <0 ) :
        return 6
    else :
        print ("ERROR : GET PITCH FLOW ")
        return -1

# 1 : + + + -   2 : + - - +   6 : + + - -


