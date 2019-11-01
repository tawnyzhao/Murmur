import numpy as np
import sys
from scipy.io.wavfile import read
import os
import re
import matplotlib.pyplot as plt

# PATH = os.cwd()
# OUTPUT_DIR = "/pi/output/"

# numpy list

np.set_printoptions(threshold=sys.maxsize)
sounds = []
channel1 = []
frame_rate = 1000
chunk_size = 1

file_list = os.listdir(".")
for file_name in file_list:
    if re.match(".*\.wav", file_name):
        sample_rate, data = read(file_name) # assuming sample rates are the same
        sounds.append(data)

for (index, sound) in enumerate(sounds):
    try:
        sound = sounds[:,0] + sounds[:,1]
    except:
        pass

    sound = sound[::len(sound)//frame_rate]
    current_loudest = 0

    for i in range(len(sound)):
        volume = sound[i][0]
        channel1.append(abs(volume))
        if abs(volume) > current_loudest:
            current_loudest = abs(volume)

num_sounds = 0
threshold = current_loudest/4

for i in range(len(channel1)):
    if abs(channel1[i]) >= threshold:
        # find when the sound goes back below the threshold
        # increment the number of num_sounds
        # continue from the new position of i, which is when the sound has gone below the threshold
        pass


print(num_sounds)

def chonk_avg(arr, chunk_size):
    #Produces a new array of the average volume in each chunk of chunk size
    #New array contains (len(arr)//chunk_size) chunks
    chonks = []
    newLen = frame_rate//chunk_size
    for i in range(newLen + 1):
        chunksum = 0
        for val in arr[i*chunk_size : i*chunk_size + chunk_size]:
            chunksum += val
        chunksum /= chunk_size
        chonks.append(chunksum)
    return chonks

def drawPlot(channelLength, channel, plotId):
    plot = plt.figure(plotId)
    plt.plot(range(channelLength + 1), channel)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.savefig('plot.png')
    return plot



g = drawPlot(frame_rate//chunk_size, channel1, 0)
f = drawPlot(frame_rate//25, chonk_avg(channel1, 25), 1)
plt.show()

# plt.plot(range(frame_rate/chunk_size + 1), channel1)

