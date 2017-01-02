# MIDI_Improvisor
A mini beat generator that improvises melodies modeled on a directed graph of melodic transitions.

## Contents
Recieves a string to seed decision making. The program then generates a four chord melody by navigating a directed cyclic graph of melodic transitions randomly. Outputs as a MIDI file or live playback.

## Prerequisites
* Python 2.7
* Python MIDI library
* Fluidsynth
* Numpy

## Optional
* Tkinter, for basic UI
* PyAudio, for live audio playback
