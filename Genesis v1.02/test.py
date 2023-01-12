from tkinter import *
from main import *
import tkinter as tk
from tkinter import filedialog
from pygame import mixer
import pyaudio
import numpy as np
import struct
import wave
import sys
import matplotlib.pyplot as plt

CHUNK = 1024

class MP:
    def __init__(self, win):
        win.geometry('400x600')
        win.title('Music Player')
        win.resizable(0, 0)

        self.play_restart = tk.StringVar()
        self.pause_resume = tk.StringVar()

        self.play_restart.set('Play')
        self.pause_resume.set('Pause')

        load_button = Button(win, text='Load', width=10, font=('Arial', 20), command=self.load)
        load_button.place(x=100, y=50, anchor='center')

        play_button = Button(win, textvariable=self.play_restart, width=10, font=('Arial', 20), command=self.play)
        play_button.place(x=100, y=100, anchor='center')

        pause_button = Button(win, textvariable=self.pause_resume, width=10, font=('Arial', 20), command=self.pause)
        pause_button.place(x=100, y=150, anchor='center')

        stop_button = Button(win, text='Stop', width=10, font=('Arial', 20), command=self.stop)
        stop_button.place(x=100, y=200, anchor='center')

        self.music_file = False
        self.playing_state = False

    ##loading works
    def load(self):
        self.music_file = filedialog.askopenfilename()
        print('Loaded: ', self.music_file)
        self.play_restart.set('Play')

    ##since the loop is a while pausing stops the stream 
    def play(self):
        if self.music_file:
            ##mixer.init()
            ##mixer.music.load(self.music_file)
            ##mixer.music.play()
            fig,ax = plt.subplots()
            x = np.arange(0, 2*CHUNK, 2)
            line, = ax.plot(x, np.random.rand(CHUNK),'r')
            ax.set_ylim(-60000, 60000)
            ax.set_xlim(0, CHUNK)
            fig.show()

            
            with wave.open(self.music_file, 'rb') as wf:
                p = pyaudio.PyAudio()
                global stream
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                       channels=wf.getnchannels(),
                                       rate=wf.getframerate(),
                                       output=True)
                while len(data:= wf.readframes(CHUNK)):
                    ##print(data)
                    stream.write(data)
                    dataInt=struct.unpack(str(2*CHUNK) + 'h', data)
                    ##print(len(dataInt))
                    ##print(dataInt[0])
                    RunAnimation(dataInt[700])
                    line.set_ydata(dataInt[:CHUNK])
                    fig.canvas.draw()
                    fig.canvas.flush_events()

            self.playing_state = False
            self.play_restart.set('Restart')
            self.pause_resume.set('Pause')

    ##pause stops the stream no way to get it to return to playing
    def pause(self):
        if not self.playing_state:
            ##mixer.music.pause()
            stream.stop_stream()
            self.playing_state = True
            self.pause_resume.set('Resume')
        else:
            ##mixer.music.unpause()
            stream.start_stream()
            
            self.playing_state = False
            self.pause_resume.set('Pause')

    ##stop does nothing
    def stop(self):
        mixer.music.stop()

root = Tk()
MP(root)
root.mainloop()
