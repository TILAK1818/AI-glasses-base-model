from gtts import gTTS
from io import BytesIO

def narrate_text(description):
    tts = gTTS(description)
    audio_path = "description_audio.mp3"
    tts.save(audio_path)
    return audio_path

