import os
from gtts import gTTS

text = "Mohamed Ali is the greatest!!"
tts = gTTS(text=text, lang='en')
tts.save("speech.mp3")
print("Saved speech.mp3")

# Auto-play the generated MP3 on Windows
try:
    os.startfile("speech.mp3")
except AttributeError:
    # Fallback for non-Windows platforms
    import subprocess
    import sys
    if sys.platform == "darwin":
        subprocess.run(["open", "speech.mp3"] , check=False)
    else:
        subprocess.run(["xdg-open", "speech.mp3"], check=False)
