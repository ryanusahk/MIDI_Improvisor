import midi
import numpy as np

def export(name, sequence):
	pattern = midi.Pattern()
	track = midi.Track()
	pattern.append(track)

	tickID = 0
	for note in sequence:

		if note:
			on = midi.NoteOnEvent(tick=tickID, velocity=120, pitch=note)
			track.append(on)
			off = midi.NoteOffEvent(tick=tickID+110, pitch=note)
			track.append(off)
		else:
			on = midi.NoteOffEvent(tick=tickID)
			track.append(on)
			off = midi.NoteOffEvent(tick=tickID+110)
			track.append(off)
	eot = midi.EndOfTrackEvent(tick=1)
	track.append(eot)
	midi.write_midifile(name + ".mid", pattern)

def getEdges():
	c0 = [1, 2, 4, 6, 7]
	c1 = [2, 4]
	c2 = [3, 4]
	c3 = [4]
	c4 = [6, 7]
	c5 = [6]
	c6 = [4, 5, 7]
	c7 = [4, 6, 7, 8, 9, 11]
	c8 = [7, 9]
	c9 = [7, 8, 9, 10, 11]
	c10 = [9, 11]
	c11 = [7, 9, 10, 11, 12]
	c12 = [11, 13]
	c13 = [14]
	c14 = [13, 11]
 
	edges = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14]

	adjustedEdges = []
	for i in range(len(edges)):
		newArray = []
		for elem in edges[i]:
			newArray.append(elem-i)
		adjustedEdges.append(newArray)
	return adjustedEdges

def centeredScale(letter, startOctave):
	scale = []
	A = 'CDEFGAB'
	start = A.find(letter)
	for i in range(15):
		letter = A[(start+i) % len(A)]
		octave = startOctave + (start+i)/len(A)
		scale.append(eval('midi.' + str(letter) + '_' + str(octave)))
	return scale

def step(currNoteID, edges):
	nextSteps = edges[currNoteID]
	return currNoteID + nextSteps[np.random.randint(len(nextSteps))]

def generateNotes(chords, rhythm, startOctave):
	startNotes = [4, 7, 9]

	midi_sequence = []

	for key in chords:

		currNote = startNotes[np.random.randint(len(startNotes))]
		path = []

		for i in range(8):
			if rhythm[i]:
				path.append(currNote)
				currNote = step(currNote, getEdges())
			else:
				path.append(False)

		scale = centeredScale(key, startOctave)
		for n in path:
			if n:
				midi_sequence.append(scale[n])
			else:
				midi_sequence.append(False)
	return midi_sequence

def generateRhythm(fraction):
	rhythm = []
	for i in range(8):
		hit = np.random.randint(fraction)
		rhythm.append(hit > 0)
	return rhythm

def getBass(chords):
	midivalues = []
	for c in chords:
		midivalues.append(eval('midi.' + c + '_4'))
	return midivalues

def generateRhythmByNotes(numnotes):
	rhythm = ([True] * numnotes) + ([False] * (8-numnotes))
	np.random.shuffle(rhythm)
	# rhythm = [True, False, True, True, True, True, True, True]
	return rhythm

def setSeed(string):
	np.random.seed(seed=hash(string)%4294967295)

# def getPercussion(zzzzzzz)

# rhythm = generateRhythm(6)
# export('top', generateNotes('AFCG', rhythm, 4))

# rhythm = generateRhythmByNotes(7)
# export('mid', generateNotes('AFCG', rhythm, 5))




