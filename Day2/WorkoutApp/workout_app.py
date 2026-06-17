import datetime
import hashlib
import os
import shutil
import sys
import subprocess
import tempfile
import time
import winsound
from pathlib import Path

try:
    from gtts import gTTSMichael
    GTTS_AVAILABLE = True
except ImportError:
    gTTS = None
    GTTS_AVAILABLE = False

# Root cache directory for generated audio files
CACHE_DIR = Path(".cache")
# Cache folder for short status sound bytes
STATUS_CACHE_DIR = CACHE_DIR / "status"
# Cache folder for full workout audio files
WORKOUT_CACHE_DIR = CACHE_DIR / "workout"
# Local copy of the workout audio file
WORKOUT_FILE = Path("workout.mp3")
# Duration for each exercise block in live mode
DURATION_SECONDS = 45
# Ordered exercise sequence for the workout
EXERCISES = [
    "pressups",
    "burpees",
    "running on the spot",
    "jumping jacks",
    "mountain climbers",
]

# Mapping from workout status keys to spoken phrases
STATUS_PHRASES = {
    "hello": "Hello {name}, let's get ready to rumble!",
    "utilize": "Let's utilize your energy and focus.",
    "start_now": "Start now.",
    "ready": "Get ready for the next exercise.",
    "countdown_3": "Three.",
    "countdown_2": "Two.",
    "countdown_1": "One.",
    "go": "Go!",
    "motivate": "Go {name}, go {name}!",
    "go_michael": "Go Michael! Keep pushing!",
    "keep_going": "Keep going.",
    "exercise_complete": "Exercise complete.",
    "workout_complete": "Great work. Workout complete.",
}

# Cached lookup table for status phrase audio filenames
STATUS_PHRASE_FILES = {
    "hello": "hello.wav",
    "utilize": "utilize.wav",
    "start_now": "start_now.wav",
    "ready": "ready.wav",
    "countdown_3": "countdown_3.wav",
    "countdown_2": "countdown_2.wav",
    "countdown_1": "countdown_1.wav",
    "go": "go.wav",
    "motivate": "motivate.wav",
    "go_michael": "go_michael_gui.wav",
    "keep_going": "keep_going.wav",
    "exercise_complete": "exercise_complete.wav",
    "workout_complete": "workout_complete.wav",
}

AUDIO_CACHE = {}

# Open the generated audio file with the default system player
def open_audio_file(path: Path) -> None:
    """Open the generated audio file with the system default player."""
    if os.name == "nt":
        os.startfile(str(path))
    elif sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
    else:
        subprocess.run(["xdg-open", str(path)], check=False)


# Get the user's name from command-line arguments or prompt
def get_user_name() -> str:
    # Use command-line arguments if present, otherwise prompt the user
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()

    name = input("Enter your name for the workout: ").strip()
    return name or "Friend"


# Synthesize speech text into WAV bytes via PowerShell
def synthesize_to_wav_bytes(text: str) -> bytes:
    # Create a temporary WAV file to store synthesized speech output
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_wav.close()
    safe_text = text.replace("'", "''")

    # Use PowerShell System.Speech to generate WAV audio from text
    ps_command = (
        "Add-Type -AssemblyName System.Speech; "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$s.SetOutputToWaveFile('{temp_wav.name}'); "
        f"$s.Speak('{safe_text}'); "
        "$s.Dispose();"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_command], check=True)

    # Read the generated WAV bytes and clean up the temporary file
    with open(temp_wav.name, "rb") as fh:
        wav_bytes = fh.read()
    os.unlink(temp_wav.name)
    return wav_bytes


# Synthesize text into a WAV file using the local Windows speech engine
def synthesize_text_to_wav_file(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    safe_text = text.replace("'", "''")
    ps_command = (
        "Add-Type -AssemblyName System.Speech; "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$s.SetOutputToWaveFile('{path}'); "
        f"$s.Speak('{safe_text}'); "
        "$s.Dispose();"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_command], check=True)


# Compute the disk cache path for a status audio file
def get_status_cache_path(status: str, name: str) -> Path:
    name_hash = hashlib.sha256(name.encode("utf-8")).hexdigest()
    filename = STATUS_PHRASE_FILES.get(status, f"{status}.wav")
    cache_name = f"{Path(filename).stem}_{name_hash}.wav"
    return STATUS_CACHE_DIR / cache_name


# Load a cached status sound or generate it if missing
def load_or_create_status_bytes(status: str, name: str) -> bytes:
    # Ensure the status cache directory exists before reading or writing
    STATUS_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = get_status_cache_path(status, name)
    if cache_path.exists():
        return cache_path.read_bytes()

    # Generate and cache the WAV bytes if this status audio is new
    wav_bytes = synthesize_to_wav_bytes(STATUS_PHRASES[status].format(name=name))
    cache_path.write_bytes(wav_bytes)
    return wav_bytes


# Build the in-memory cache of status audio bytes
def build_audio_cache(name: str) -> None:
    # Preload all status audio into memory for quick playback
    AUDIO_CACHE.clear()
    for status in STATUS_PHRASES:
        AUDIO_CACHE[status] = load_or_create_status_bytes(status, name)
    print(f"Audio cache built: {len(AUDIO_CACHE)} cached audio clips ready")


# Play a cached status sound from memory
def play_status_sound(status: str) -> None:
    if status not in AUDIO_CACHE:
        return
    # Play the cached WAV bytes synchronously (blocks until audio finishes)
    winsound.PlaySound(AUDIO_CACHE[status], winsound.SND_MEMORY)


# Build the full workout narration text for the cached MP3 output
def build_workout_text(name: str) -> str:
    # Build the full workout narration text for the cached MP3 output
    lines = [
        f"Hello {name}, welcome to your 45 second workout.",
        "Let's get ready to rumble!",
        "Let's utilize your energy and focus.",
        "Start now.",
    ]

    for exercise in EXERCISES:
        lines.extend([
            f"Next exercise is {exercise}.",
            "Get ready.",
            "Three, two, one.",
            f"Go! Do {exercise} for {DURATION_SECONDS} seconds.",
            "Keep going!",
        ])

    lines.extend([
        "Great work!",
        f"Well done {name}, you finished the workout.",
        "Workout complete.",
        "You utilized your strength and endurance.",
    ])

    return " ".join(lines)


# Format the current date/time as a readable timestamp
def format_current_time() -> str:
    # Return a timestamp string for live workout logging
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


# Run the live workout loop with real-time timestamps and audio cues
def run_live_workout(name: str) -> None:
    # Run the on-screen live workout loop with time stamps and cached audio cues
    print(f"Workout start time: {format_current_time()}")
    play_status_sound("hello")
    print(f"{name}, follow the on-screen live countdown and exercise prompts.")
    play_status_sound("utilize")
    time.sleep(1)
    play_status_sound("start_now")

    for exercise in EXERCISES:
        print()
        print(f"{format_current_time()} - Next exercise: {exercise}")
        play_status_sound("ready")
        time.sleep(2)

        # Play the 3-2-1 countdown sounds before starting
        play_status_sound("countdown_3")
        time.sleep(1)
        play_status_sound("countdown_2")
        time.sleep(1)
        play_status_sound("countdown_1")
        time.sleep(1)

        play_status_sound("go")
        motivation_interval = 5  # Play motivational audio every 5 seconds
        for remaining in range(DURATION_SECONDS, 0, -1):
            print(f"{format_current_time()} - {exercise}: {remaining} seconds remaining", end="\r")
            if remaining % motivation_interval == 0:
                play_status_sound("motivate")
            elif remaining == 20:
                play_status_sound("keep_going")
            time.sleep(1)

        print()
        play_status_sound("exercise_complete")
        print(f"{format_current_time()} - {exercise} complete!")
        time.sleep(2)

    print()
    play_status_sound("workout_complete")
    print(f"{format_current_time()} - Great work, {name}! Workout complete.")


# Compute the cached workout audio path for the workout text
def get_workout_cache_path(text: str) -> Path:
    # Create the workout cache directory and return a path based on a text hash
    WORKOUT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    ext = "mp3" if GTTS_AVAILABLE else "wav"
    return WORKOUT_CACHE_DIR / f"workout_{text_hash}.{ext}"


# Build the full workout audio file and store it in the cache
def build_workout_audio(name: str) -> Path:
    workout_text = build_workout_text(name)
    workout_cache_path = get_workout_cache_path(workout_text)
    if workout_cache_path.exists():
        print(f"Using cached workout audio: {workout_cache_path}")
        return workout_cache_path

    print("Generating one workout audio file for the full session...")
    if GTTS_AVAILABLE:
        tts = gTTS(text=workout_text, lang="en")
        tts.save(str(workout_cache_path))
    else:
        synthesize_text_to_wav_file(workout_text, workout_cache_path)
    print(f"Saved cached workout audio: {workout_cache_path}")
    return workout_cache_path


# Main application entry point for the workout app
def main() -> None:
    # Entry point for the workout app
    user_name = get_user_name()
    print("Building audio cache for live cues...")
    build_audio_cache(user_name)
    print("Preparing workout audio...")
    workout_path = build_workout_audio(user_name)

    if workout_path is not None:
        if workout_path != WORKOUT_FILE:
            shutil.copy2(workout_path, WORKOUT_FILE)
        print(f"Opening workout audio file: {workout_path}")
        open_audio_file(workout_path)
        print("Workout audio generated and opened. Follow the prompts in the audio player.")
    else:
        print("Failed to generate workout audio.")


if __name__ == "__main__":
    main()
