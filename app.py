from Tkinter import *
import gen
import time
import fluidsynth
import numpy as np
import pyaudio

class App:
	def __init__(self, master):

		frame = Frame(master)
		frame.pack()

		self.label = Label(frame, text='Welcome to Trash(tm)')
		self.label.pack()

		self.w = Scale(frame, from_=0, to=8, orient=HORIZONTAL)
		self.w.pack()

		self.e = Entry(frame)
		self.e.pack()

		self.e.focus_set()

		self.hi_there = Button(frame, text="Make Trash", command=self.swag)
		self.hi_there.pack()

	def swag(self):
		while(True):
			self.sound()

	def sound(self):

		if len(self.e.get()) > 0:
			gen2.setSeed(self.e.get())

		rhythm = None
		if self.w.get() > 0:
			rhythm = gen2.generateRhythmByNotes(self.w.get())
		else:
			# rhythm = gen2.generateRhythm(np.random.randint(5,7))
			rhythm = gen2.generateRhythmByNotes(np.random.randint(6,9))

		CHORDS = 'AFCG'

		notes = gen2.generateNotes(CHORDS, rhythm, 4)
		bass = gen2.getBass(CHORDS)

		pa = pyaudio.PyAudio()
		strm = pa.open(
		    format = pyaudio.paInt16,
		    channels = 2, 
		    rate = 44100, 
		    output = True)

		s = []
		fl = fluidsynth.Synth()


		TSSS = [1,1,1,0,0,0,1,0,1,1,1,0,0,1,0,1]
		CLAP = [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0]
		BEAT = [1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0]

# 39 clap
# 42 tss
# 88 thud
		prevBass = False
		for i in range(len(notes)*2):
			note = notes[i%len(notes)]

			sfid = fl.sfload("Full Grand Piano.sf2")
			fl.program_select(0, sfid, 0, 0)
			if i%8 == 0:
				fl.noteon(0, bass[(i%32)/8], 50)
				if prevBass:
					fl.noteoff(0, prevBass)
				prevBass = bass[(i%32)/8]

			sfid = fl.sfload("percussion/Angular Pop1 Set.sf2")
			fl.program_select(0, sfid, 0, 0)

			if TSSS[i%len(TSSS)]:
				fl.noteon(0, 42, 50)
			else:
				fl.noteoff(0, 42)
			if CLAP[i%len(CLAP)]:
				fl.noteon(0, 39, 80)
			else:
				fl.noteoff(0, 39)
			if BEAT[i%len(BEAT)]:
				fl.noteon(0, 88, 120)
			else:
				fl.noteoff(0, 88)

			sfid = fl.sfload("arctic.sf2")
			fl.program_select(0, sfid, 0, 0)
			if note:
				if i < len(notes):
					print ' ' * (note-50) + '*'
				fl.noteon(0, note, 50)
				s = np.append(s, fl.get_samples(44100/4))
				# fl.noteoff(0, note)
				# s = np.append(s, fl.get_samples(0))
			else:
				s=np.append(s, fl.get_samples(44100/4))
				if i < len(notes):
					print '\n'

		print '\n\n\n'
		a = s[:]

		###SET2###

		rhythm = gen2.generateRhythmByNotes(np.random.randint(3,5))
		notes = gen2.generateNotes(CHORDS, rhythm, 5)	
		for i in range(len(notes)*2):
			note = notes[i%len(notes)]

			sfid = fl.sfload("Full Grand Piano.sf2")
			fl.program_select(0, sfid, 0, 0)
			if i%8 == 0:
				fl.noteon(0, bass[(i%32)/8], 50)
				if prevBass:
					fl.noteoff(0, prevBass)
				prevBass = bass[(i%32)/8]

			sfid = fl.sfload("percussion/Angular Pop1 Set.sf2")
			fl.program_select(0, sfid, 0, 0)

			if TSSS[i%16]:
				fl.noteon(0, 42, 50)
			else:
				fl.noteoff(0, 42)
			if CLAP[i%16]:
				fl.noteon(0, 39, 80)
			else:
				fl.noteoff(0, 39)
			if BEAT[i%16]:
				fl.noteon(0, 88, 120)
			else:
				fl.noteoff(0, 88)

			sfid = fl.sfload("arctic.sf2")
			fl.program_select(0, sfid, 0, 0)
			if note:
				if i < len(notes):
					print ' ' * (note-50) + '*'
				fl.noteon(0, note, 50)
				s = np.append(s, fl.get_samples(44100/4))
				# fl.noteoff(0, note)
				# s = np.append(s, fl.get_samples(0))
			else:
				if i < len(notes):
					print '\n'
				s=np.append(s, fl.get_samples(44100/4))

		s = np.append(s, a)

		fl.delete()

		samps = fluidsynth.raw_audio_string(s)

		print 'Starting playback'
		strm.write(samps)

root = Tk()
root.wm_title("Trash v4.20")

app = App(root)

root.mainloop()