import speech_recognition as sr
import os
from pydub import AudioSegment
import ffmpeg
from threading import Thread
import time
import shutil
import numpy as np

def get_length_audio(audio):
	length = ffmpeg.probe(audio)['format']['duration']
	return float(length)


def cutting_original_audio(audio, cut_dir):
	length = get_length_audio(audio)
	split_size = 60
	nums = round(length/split_size)

	new_audio_file = []
	for i in range(nums):
		new_audio_file.append(os.path.join(cut_dir, f'aud2-{i}.wav'))
		os.system(f'ffmpeg -ss {i*split_size} -t {split_size} -i {audio} -ab 256k {new_audio_file[i]}')

	return new_audio_file

def save_file(result, file):
	with open(file,"w") as f:
	    f.write(result)


class SpeechToText(Thread):
    def __init__(self, number, audio_name, txt_dir):
        """Инициализация потока"""
        Thread.__init__(self)
        self.number = number
        self.audio_name = audio_name
        self.txt_dir = txt_dir

    def run(self):
        """Запуск потока"""
        print(f'start reading {self.audio_name}')
        start_time = time.time()
        r = sr.Recognizer()
        with sr.AudioFile(self.audio_name) as source:
        	audio_rec = r.record(source)

        txt_file = os.path.join(self.txt_dir, f'{self.number}.txt')
        result = '{}'.format(r.recognize_google(audio_rec, language="ru"))
        save_file(result, txt_file)
        
        print("--- {} seconds ---".format(time.time() - start_time))
        print(f"/nЗакончил считывание {self.audio_name}/n")


def main(audio_files, txt_dir):
    threads = []
    for num, audio_name in enumerate(audio_files):
        threads.append(SpeechToText(num, audio_name, txt_dir))
        threads[num].start()
    return threads


def run():
	audio_dir = 'audio'
	cut_dir = os.path.join(audio_dir, 'cut_dir')
	txt_dir = 'txt'

	if os.path.isdir(cut_dir):
		shutil.rmtree(cut_dir)
	if os.path.isdir(txt_dir):
		shutil.rmtree(txt_dir)
	os.mkdir(cut_dir)
	os.mkdir(txt_dir)

	audio_file = os.path.join(audio_dir, 'aud2.wav')

	new_audio_files = cutting_original_audio(audio_file, cut_dir)

	threads = main(new_audio_files, txt_dir)
	for thr in threads:
		thr.join()