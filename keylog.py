from pynput import keyboard
from midiutil import MIDIFile
import datetime

# Basic Alpha Numeric Key map

key_template = {

    'a' : {'pitch' : 0, 'volume' : 100},
    'b' : {'pitch' : 5, 'volume' : 100},
    'c' : {'pitch' : 11, 'volume' : 100},
    'd' : {'pitch' : 15, 'volume' : 100},
    'e' : {'pitch' : 21, 'volume' : 100},
    'f' : {'pitch' : 25, 'volume' : 100},
    'g' : {'pitch' : 31, 'volume' : 100},
    'h' : {'pitch' : 35, 'volume' : 100},
    'i' : {'pitch' : 41, 'volume' : 100},
    'j' : {'pitch' : 45, 'volume' : 100},
    'k' : {'pitch' : 51, 'volume' : 100},
    'l' : {'pitch' : 55, 'volume' : 100},
    'm' : {'pitch' : 61, 'volume' : 100},
    'n' : {'pitch' : 65, 'volume' : 100},
    'o' : {'pitch' : 71, 'volume' : 100},
    'p' : {'pitch' : 75, 'volume' : 100},
    'q' : {'pitch' : 81, 'volume' : 100},
    'r' : {'pitch' : 85, 'volume' : 100},
    's' : {'pitch' : 91, 'volume' : 100},
    't' : {'pitch' : 95, 'volume' : 100},
    'u' : {'pitch' : 101, 'volume' : 100},
    'v' : {'pitch' : 105, 'volume' : 100},
    'w' : {'pitch' : 111, 'volume' : 100},
    'x' : {'pitch' : 115, 'volume' : 100},
    'y' : {'pitch' : 121, 'volume' : 100},
    'z' : {'pitch' : 125, 'volume' : 100},
    '0' : {'pitch' : 2, 'volume' : 100},
    '1' : {'pitch' : 4, 'volume' : 100},
    '2' : {'pitch' : 6, 'volume' : 100},
    '3' : {'pitch' : 8, 'volume' : 100},
    '4' : {'pitch' : 12, 'volume' : 100},
    '5' : {'pitch' : 14, 'volume' : 100},
    '6' : {'pitch' : 16, 'volume' : 100},
    '7' : {'pitch' : 18, 'volume' : 100},
    '8' : {'pitch' : 22, 'volume' : 100},
    '9' : {'pitch' : 24, 'volume' : 100},
    'Key.space' : {'pitch' : 0, 'volume' : 0},
    'Key.enter' : {'pitch' : 0, 'volume' : 0}
    }

#---------------------------------------------------------------

note  = []  # MIDI note number
durations  = []  # MIDI note duration in beat
volume   = 100  # 0-127, as per the MIDI standard
track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 190   # In BPM

# __init__(self, numTracks=1, removeDuplicates=True, deinterleave=True, adjust_origin=None, file_format=1)
MyMIDI = MIDIFile(1, True, True, False, 1)
MyMIDI.addTempo(track, time, tempo)

print('Listening ...')
print('Press esc key to stop the listener')

def lookKey(key):
    for k,v in key_template.items():
        if key in k:
            if k != 'Key.space':
                note.append(v['pitch'])
                #durations.append(end-start)

def on_release(key):

    if key == keyboard.Key.esc:
        for i, pitch in enumerate(note):
            MyMIDI.addNote(track, channel, pitch, time + i*duration, duration, volume)

        t = datetime.datetime.now()
        name = str(t.year)+""+str(t.month)+""+str(t.day)+""+str(t.hour)+""+str(t.minute)+""+str(t.second)
        
        with open(name+".mid", "wb") as output_file:
                MyMIDI.writeFile(output_file)
                print("\nQuitting keylogger")
                return False

    else:
        try:
            #print('alphanumeric key {0} pressed'.format(key.char))
            k = format(key.char)
            lookKey(k)

        except AttributeError:
            #print('special key {0} pressed'.format(key))
            k = format(key)
            lookKey(k)


with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
