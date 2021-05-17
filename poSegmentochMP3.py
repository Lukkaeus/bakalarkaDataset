import csv
from pydub import AudioSegment
import json
import re

list_of_starts = []
list_of_ends = []
list_of_sentences = []
list_of_waw = []

times_of_starts = []
times_of_ends = []

list_of_timestamps_from_Json = []


# rozparsuje waw súbor na intervaly uvedené v list_of_timestamps, a vytvorí prislúchajúce waw file ku každemu intervalu
def parse_wav(recording_name, audio_file):
    audio = AudioSegment.from_wav(audio_file)
    list_of_timestamps = list_of_timestamps_from_Json

    start = 0
    part = 1
    for idx, t in enumerate(list_of_timestamps):
       # idx > 800 znamená že chceme vytvoriť 401 segmentov (1 segment predstavuje prepis jednej vety)
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
        # print("split at [ {}:{}] ms".format(start, end))
        audio_chunk = audio[start:end]
        audio_chunk.export(
            "E:\\Bakalarka dataset\\Rozparsovane\\clips" + '\\' + "part_" + str(part) + "_" + recording_name,
            format="wav")
        list_of_waw.append("part_" + str(part) + "_" + recording_name)
        part += 1
        start = end  # pydub works in millisec


# načíta hodnoty z JSON, start a end time kazdeho cas.useku a ulozi ich do list_of_starts a list_of_ends
def load_from_json():
    file = open("E:/Bakalarka dataset/Rozparsovane/S01.json", 'r', encoding="utf-8")
    json_objekt = json.load(file)
    for x in json_objekt:
        # print(x["end_time"]["original"])
        # print(x["start_time"]["original"])
        list_of_starts.append(x["start_time"]["original"])
        list_of_ends.append(x["end_time"]["original"])

        # zbaví sa textu medzi [ ]
        t = (x["words"])
        t = re.sub(r'\[.*?\]', '', t)
        list_of_sentences.append(t)

    print("All was loaded from your json file")

# vytvárame 2 nové listy, time_of_starts a time_of_ends, ktoré obsahujú časy začiatkov a koncov časových segmentov v sekundách (originálny časový formát bol xx:yy:zz)
def change_to_seconds():
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

# pomocná metoda pre metodu change_to_seconds
def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

# vytvárame list pre metódu parse_wav, kedže na vstupe vyžaduje list vo formáte kde nasleduju začiatky a konce jednotlivých segmentov za sebou
def make_timestamps_list():
    for i in range(len(times_of_starts)):
        if i > 0:
            list_of_timestamps_from_Json.append(times_of_starts[i])
        list_of_timestamps_from_Json.append(times_of_ends[i])
    # print(list_of_timestamps_from_Json)

# vytvorenie tsv súborov s hlavičkou vyžadovanou Mozilla Deepspeech
def create_tsv_files(fileName):
    with open('E:/Bakalarka dataset/Rozparsovane' + '/' + fileName, 'wt') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(
            ['client_id', 'path', 'sentence', 'up_votes', 'down_votes', 'age', 'gender', 'accent', 'locale', 'segment'])

# zapisujeme do už vytvorených tsv súborov, do druhého a tretieho stlpca...... druhý stlpec názov mp3, tretí stlpec prepis vety
def make_tsv(fileName, fromIDX, toIDX):
    with open('E:/Bakalarka dataset/Rozparsovane' + '/' + fileName, 'a') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        # client_id	path	sentence	up_votes	down_votes	age	gender	accent	locale	segment
        # tsv_writer.writerow(['client_id', 'path', 'sentence', 'up_votes', 'down_votes', 'age', 'gender', 'accent', 'locale', 'segment'])
        for i in range(toIDX):
            if i < fromIDX:
                continue
            tsv_writer.writerow(['', list_of_waw[i], list_of_sentences[i]])

# metóda pre spracovanie zadaných nahrávok
def do_all_recordings():
    recording_name = "S01_P01.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_P01.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")
    print(len(list_of_waw))
    print(len(list_of_sentences))

    recording_name = "S01_P02.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_P02.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_P03.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_P03.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_P04.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_P04.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U01.CH1.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U01.CH1.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U01.CH2.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U01.CH2.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U01.CH3.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U01.CH3.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U01.CH4.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U01.CH4.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U02.CH1.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U02.CH1.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U02.CH2.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U02.CH2.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U02.CH3.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U02.CH3.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U02.CH4.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U02.CH4.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U03.CH1.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U03.CH1.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U03.CH2.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U03.CH2.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U03.CH3.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U03.CH3.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U03.CH4.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U03.CH4.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U04.CH1.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U04.CH1.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U04.CH2.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U04.CH2.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U04.CH3.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U04.CH3.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U04.CH4.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U04.CH4.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U05.CH1.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U05.CH1.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U05.CH2.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U05.CH2.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U05.CH3.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U05.CH3.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U05.CH4.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U05.CH4.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U06.CH1.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U06.CH1.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U06.CH2.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U06.CH2.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U06.CH3.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U06.CH3.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")

    recording_name = "S01_U06.CH4.mp3"
    audio_file = "E:\\Bakalarka dataset\\CHiME5\\audio\\eval\\S01_U06.CH4.wav"
    parse_wav(recording_name, audio_file)
    print(recording_name + " bola spracovaná ")



load_from_json()
change_to_seconds()
make_timestamps_list()
create_tsv_files("train.tsv")
create_tsv_files("dev.tsv")
create_tsv_files("test.tsv")
do_all_recordings()


