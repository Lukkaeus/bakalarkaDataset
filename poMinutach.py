from pydub import AudioSegment

# files_path = ''
# file_name = ''
# 
# startMin = 9
# startSec = 50
# 
# endMin = 13
# endSec = 30
# 
# # Time to miliseconds
# startTime = startMin*60*1000+startSec*1000
# endTime = endMin*60*1000+endSec*1000
# 
# # Opening file and extracting segment
# song = AudioSegment.from_mp3( files_path+file_name+'.mp3' )
# extract = song[startTime:endTime]
# 
# # Saving
# extract.export( file_name+'-extract.mp3', format="mp3")

from pydub import AudioSegment
import math

#https://stackoverflow.com/questions/37999150/how-to-split-a-wav-file-into-multiple-wav-files

class SplitWavAudioMubin():
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '\\' + filename

        self.audio = AudioSegment.from_wav(self.filepath)

    def get_duration(self):
        return self.audio.duration_seconds

    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export("E:\\Bakalarka dataset\\Rozparsovane\\clips" + '\\' + split_filename, format="wav")

    def multiple_split(self, min_per_split):
        total_mins = math.ceil(self.get_duration() / 60)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i + min_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')

# E:\Bakalarka dataset\CHiME5\audio\eval
folder = 'E:\\Bakalarka dataset\\CHiME5\\audio\\eval'
file = 'S01_P01.wav'
split_wav = SplitWavAudioMubin(folder, file)
split_wav.multiple_split(min_per_split=1)