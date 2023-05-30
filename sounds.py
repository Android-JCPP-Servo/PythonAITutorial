"""
SOUNDS
This file is to help organize audio for SOC
"""
# Import sound player modules
from pydub import AudioSegment
from pydub.playback import play

# Method for playing R4-P17 greeting
def play_greeting():
    droid_greet = AudioSegment.from_wav("./sound_effects/p17_greet.wav")
    play(droid_greet)

# Method for playing R4-P17 response
def play_response():
    droid_res = AudioSegment.from_wav("./sound_effects/p17_process_1.wav")
    play(droid_res)

# Method for playing R4-P17 response #2
def play_response_2():
    droid_res_2 = AudioSegment.from_wav("./sound_effects/p17_process_2.wav")
    play(droid_res_2)

# Method for playing R4-P17 command
def play_command():
    droid_command = AudioSegment.from_wav("./sound_effects/p17_command.wav")
    play(droid_command)

# Method for playing R4-P17 rejection
def play_rejection():
    droid_reject = AudioSegment.from_wav('./sound_effects/p17_reject.wav')
    play(droid_reject)

# Method for playing R4-P17 goodbye
def play_goodbye():
    droid_bye = AudioSegment.from_wav("./sound_effects/p17_bye.wav")
    play(droid_bye)

# Method for playing R4-P17 acknowledgement
def play_acknowledge():
    droid_acknowledge = AudioSegment.from_wav("./sound_effects/p17_acknowledge.wav")
    play(droid_acknowledge)