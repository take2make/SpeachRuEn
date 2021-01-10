import speech_recognition as sr
import os
from pydub import AudioSegment
import ffmpeg
from threading import Thread
import time
import shutil

def get_length_audio(audio):
	length = ffmpeg.probe(audio)['format']['duration']
	return float(length)

def cutting_original_audio(audio, cutting_dir):
	length = get_length_audio(audio)
	split_size = 5
	nums = round(length/split_size)

	new_audio_file = []
	for i in range(nums):
		new_audio_file.append(os.path.join(cutting_dir, f'aud2-{i}.wav'))
		os.system(f'ffmpeg -ss {i*split_size} -t {split_size} -i {audio} -ab 256k {new_audio_file[i]}')

	return new_audio_file

class SpeechToText(Thread):
    def __init__(self, audio_name):
        """Инициализация потока"""
        Thread.__init__(self)
        self.audio_name = audio_name

    def run(self):
        """Запуск потока"""
        print(f'start reading {self.audio_name}')
        start_time = time.time()
        r = sr.Recognizer()
        with sr.AudioFile(self.audio_name) as source:
        	audio_rec = r.record(source)

        print(f"/n{self.audio_name} said/n", r.recognize_google(audio_rec, language="ru"))
        
        print("--- {} seconds ---".format(time.time() - start_time))
        print(f"/nЗакончил считывание {self.audio_name}/n")

def main(audio_files):
    for audio_name in audio_files:
        thread = SpeechToText(audio_name)
        thread.start()

if __name__ == "__main__":
	audio_dir = 'audio'
	cut_dir = os.path.join('audio', 'cut_dir')
	if os.path.isdir(cut_dir):
		shutil.rmtree(cut_dir)
	os.mkdir(cut_dir)

	audio_file = os.path.join(audio_dir, 'aud2.wav')

	new_audio_files = cutting_original_audio(audio_file, cut_dir)
	main(new_audio_files)