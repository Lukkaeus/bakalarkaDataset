# https://stackoverflow.com/questions/51622865/break-up-a-wav-file-by-timestamp
import csv
from pydub import AudioSegment
import json

list_of_starts = []
list_of_ends = []
list_of_sentences = []
list_of_waw = []

times_of_starts = []
times_of_ends = []

list_of_timestamps_from_Json = []


# rozparsuje waw súbor na intervaly uvedené v list_of_timestamps, a vytvorí prislúchajúce waw file ku každemu intervalu
def parseWav(recording_name, audio_file):
    audio = AudioSegment.from_wav(audio_file)
    # list_of_timestamps = [1.37, 20, 30, 40, 50, 60, 70, 80, 90]  # and so on in *seconds*
    list_of_timestamps = list_of_timestamps_from_Json

    start = 0
    part = 1
    for idx, t in enumerate(list_of_timestamps):
        # nastavenia pre train,dev,test
        # #if idx == 700:
        #     make_tsv("train.tsv",0,699)
        # #if idx == 900:
        #     make_tsv("dev.tsv",700,899)
        # #if idx == 1100:
        #     make_tsv("test.tsv",900,1099)
        if idx > 800:
            make_tsv("train.tsv", 0, 300)
            make_tsv("dev.tsv", 300, 350)
            make_tsv("test.tsv", 350, 401)
            list_of_waw.clear()
            break
        # ---------------------------------------
        if (idx % 2 == 1):
            start = t * 1000
            continue

        # break loop if at last element of list
        if idx == len(list_of_timestamps):
            break

        end = t * 1000  # pydub works in millisec
        # print("splteit at [ {}:{}] ms".format(start, end))
        audio_chunk = audio[start:end]
        audio_chunk.export(
            "E:\\Bakalarka dataset\\Rozparsovane\\clips" + '\\' + "part_" + str(part) + "_" + recording_name,
            format="wav")
        list_of_waw.append("part_" + str(part) + "_" + recording_name)
        part += 1
        start = end  # pydub works in millisec


# načíta hodnoty z JSON, start a end time kazdeho cas.useku a ulozi ich do list_of_starts a list_of_ends
def loadFromJson():
    file = open("E:/Bakalarka dataset/Rozparsovane/S01.json", 'r', encoding="utf-8")
    json_objekt = json.load(file)
    for x in json_objekt:
        # print(x["end_time"]["original"])
        # print(x["start_time"]["original"])
        list_of_starts.append(x["start_time"]["original"])
        list_of_ends.append(x["end_time"]["original"])
        list_of_sentences.append(x["words"])

    # print(list_of_sentences)
    # print(list_of_ends)
    # print(list_of_starts)
    print("All was loaded from your json file")


def changeToSecond():
    for x in range(len(list_of_starts)):
        time = list_of_starts[x]
        time_in_seconds = get_sec(time)
        times_of_starts.append(time_in_seconds)

        time = list_of_ends[x]
        time_in_seconds = get_sec(time)
        times_of_ends.append(time_in_seconds)

    # print(times_of_starts)
    # print(times_of_ends)
    print("Times were converted to seconds format")


def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def make_timestamps_list():
    for i in range(len(times_of_starts)):
        if i > 0:
            list_of_timestamps_from_Json.append(times_of_starts[i])
        list_of_timestamps_from_Json.append(times_of_ends[i])
    # print(list_of_timestamps_from_Json)


# https://riptutorial.com/python/example/26946/writing-a-tsv-file
def create_tsv_files(fileName):
    with open('E:/Bakalarka dataset/Rozparsovane' + '/' + fileName, 'wt') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(
            ['client_id', 'path', 'sentence', 'up_votes', 'down_votes', 'age', 'gender', 'accent', 'locale', 'segment'])


def make_tsv(fileName, fromIDX, toIDX):
    # with open('E:/Bakalarka dataset/Rozparsovane' + '/' + fileName, 'wt') as out_file:
    with open('E:/Bakalarka dataset/Rozparsovane' + '/' + fileName, 'a') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        # client_id	path	sentence	up_votes	down_votes	age	gender	accent	locale	segment
        # tsv_writer.writerow(['client_id', 'path', 'sentence', 'up_votes', 'down_votes', 'age', 'gender', 'accent', 'locale', 'segment'])
        for i in range(toIDX):
            if i < fromIDX:
                continue
            tsv_writer.writerow(['', list_of_waw[i], list_of_sentences[i]])


def do_all_recordings():
    recording_name = "S01_P01.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_P01.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")
    print(len(list_of_waw))
    print(len(list_of_sentences))

    recording_name = "S01_P02.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_P02.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_P03.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_P03.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_P04.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_P04.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U01.CH1.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U01.CH1.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U01.CH2.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U01.CH2.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U01.CH3.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U01.CH3.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U01.CH4.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U01.CH4.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U02.CH1.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U02.CH1.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U02.CH2.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U02.CH2.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U02.CH3.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U02.CH3.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U02.CH4.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U02.CH4.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U03.CH1.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U03.CH1.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U03.CH2.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U03.CH2.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U03.CH3.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U03.CH3.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U03.CH4.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U03.CH4.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U04.CH1.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U04.CH1.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U04.CH2.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U04.CH2.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U04.CH3.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U04.CH3.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U04.CH4.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U04.CH4.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U05.CH1.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U05.CH1.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U05.CH2.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U05.CH2.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U05.CH3.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U05.CH3.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U05.CH4.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U05.CH4.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U06.CH1.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U06.CH1.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U06.CH2.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U06.CH2.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U06.CH3.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U06.CH3.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U06.CH4.wav"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U06.CH4.wav"
    parseWav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")


loadFromJson()
changeToSecond()
make_timestamps_list()
create_tsv_files("train.tsv")
create_tsv_files("dev.tsv")
create_tsv_files("test.tsv")
do_all_recordings()

# print(len(list_of_sentences))
# print(list_of_waw)
# ak idx = 500 tak len(list_of_waw) = 251
# ak idx = 1000 tak...................501
# print(len(list_of_waw))
