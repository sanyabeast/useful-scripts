import random
import time
from music21 import *
import music21

def generateBlues(length):
    """
    Generates a blues sequence of the specified length.
    """
    sc = music21.scale.WeightedHexatonicBlues('C')
    melody = stream.Stream()

    for i in range(length):
        # Choose a random pitch from the scale
        pitch = random.choice(sc.pitches)

        # Add a quarter note with the pitch to the melody
        melody.append(note.Note(pitch, quarterLength=1))

    # Add a backing track with chords
    chords = harmony.getChordSymbolFigureFromChord(chord.Chord('C7'))
    for i in range(length):
        harmonyPart = stream.Part()
        chordSymbol = harmony.ChordSymbol(chords)
        harmonyPart.append(chordSymbol)
        melody.insert(i, harmonyPart)

    # Play the melody and chords
    player = music21.midi.realtime.StreamPlayer(melody)
    player.play()

if __name__ == '__main__':
    generateBlues(12)