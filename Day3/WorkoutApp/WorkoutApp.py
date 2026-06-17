# ============================================
# WORKOUT TIMER APP WITH VOICE COACHING
# ============================================
# This program runs a set of timed workout tasks,
# greets the user, gives countdown updates, and
# provides encouragement for each exercise.
# It tries to use a voice plugin when available and
# caches generated speech sound files.

import os
import sys
import time
import math
import platform
import random
import base64
import shutil
import subprocess

from workout_config import DEFAULT_EXERCISE_COUNT, DEFAULT_REST, MIN_REST, MESSAGES, WORKOUT_TASKS


class VoiceCoach:
    """Optional voice coach that speaks text and caches sound files."""

    CACHE_DIR = "sound_cache"

    def __init__(self):
        self.engine = None
        self.use_win_sound = False
        self.have_winsound = False
        self.use_local_tts = False
        self.use_ssml = False
        self.voice_available = False
        self.use_aws_polly = False
        self.polly_voice = "Joanna"
        self.polly_client = None

        if platform.system() == "Windows":
            try:
                import winsound  # type: ignore
                self.have_winsound = True
            except ImportError:
                self.have_winsound = False

        self.engine = None
        if platform.system() == "Windows" and self._local_tts_available():
            self.use_local_tts = True
            self.use_ssml = True
            self.voice_available = True
        else:
            try:
                import pyttsx3

                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 145)  # somewhat upbeat spoken rate
                self.engine.setProperty("volume", 1.0)
                self.voice_available = True
            except Exception:
                self.engine = None
                if self._local_tts_available():
                    self.use_local_tts = True
                    self.use_ssml = platform.system() == "Windows"
                    self.voice_available = True
                else:
                    if platform.system() != "Windows":
                        try:
                            import boto3

                            self.polly_client = boto3.client("polly")
                            self.use_aws_polly = True
                            self.use_ssml = True
                            self.voice_available = True
                        except Exception:
                            self.use_aws_polly = False
                            self.voice_available = False
                            print("Optional voice module pyttsx3 not installed or unavailable. Running in text-only mode.")
                    else:
                        try:
                            import winsound

                            self.use_win_sound = True
                            self.voice_available = True
                        except ImportError:
                            self.use_win_sound = False
                            self.voice_available = False
                            print("Optional voice module pyttsx3 not installed or unavailable. Running in text-only mode.")

        if self.voice_available:
            os.makedirs(self.CACHE_DIR, exist_ok=True)
            if self.use_local_tts:
                print("Voice backend: Windows PowerShell local TTS.")
            elif self.engine is not None:
                print("Voice backend: pyttsx3.")
            elif self.use_aws_polly:
                print("Voice backend: AWS Polly.")
            elif self.have_winsound:
                print("Voice backend: Windows beep fallback.")

    def _local_tts_available(self):
        """Return True if a local OS text-to-speech command is available."""
        if sys.platform.startswith("win"):
            return shutil.which("powershell") is not None
        if sys.platform == "darwin":
            return shutil.which("say") is not None
        return shutil.which("espeak") is not None or shutil.which("spd-say") is not None

    def _escape_ssml_text(self, text):
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )

    def _build_ssml(self, message):
        safe_text = self._escape_ssml_text(message)
        return (
            "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>"
            f"<prosody rate='medium' pitch='+50%'>"
            f"{safe_text}"
            "</prosody></speak>"
        )

    def _powershell_encoded_command(self, script):
        encoded = base64.b64encode(script.encode('utf-16-le')).decode('ascii')
        return encoded

    def _speak_local(self, message):
        """Speak a message using a platform-native TTS command."""
        try:
            if sys.platform.startswith("win"):
                if self.use_ssml:
                    ssml = self._build_ssml(message)
                    script = (
                        "Add-Type -AssemblyName System.Speech; "
                        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                        "$s.SetOutputToDefaultAudioDevice(); "
                        "$s.Rate = 0; $s.Volume = 100; "
                        "$xmlText = @'\n"
                        f"{ssml}\n"
                        "'@; "
                        "$s.SpeakSsml($xmlText)"
                    )
                else:
                    safe_message = message.replace("'", "''")
                    script = (
                        "Add-Type -AssemblyName System.Speech; "
                        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                        "$s.SetOutputToDefaultAudioDevice(); "
                        "$s.Rate = 0; $s.Volume = 100; "
                        f"$s.Speak('{safe_message}')"
                    )
                encoded = self._powershell_encoded_command(script)
                subprocess.run([
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-EncodedCommand",
                    encoded,
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif sys.platform == "darwin":
                subprocess.run(["say", message], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                if shutil.which("espeak"):
                    subprocess.run(["espeak", message], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                elif shutil.which("spd-say"):
                    subprocess.run(["spd-say", message], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    raise RuntimeError("No local TTS command available")
        except Exception as exc:
            print(f"Local TTS failed: {exc}")
            print(f"[VOICE] {message}")

    def _cache_path(self, cache_key, extension="mp3"):
        safe_key = "".join(c for c in cache_key if c.isalnum() or c in "-_ ").rstrip()
        return os.path.join(self.CACHE_DIR, f"{safe_key}.{extension}")

    def _play_audio_file(self, file_path):
        """Play an audio file using the OS default player."""
        try:
            if sys.platform.startswith("win"):
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["afplay", file_path])
            else:
                subprocess.Popen(["xdg-open", file_path])
        except Exception:
            print(f"Unable to play audio file: {file_path}")

    def _speak_with_polly(self, message, sound_file):
        """Use AWS Polly to generate a cached audio file and play it."""
        try:
            if self.use_ssml:
                response = self.polly_client.synthesize_speech(
                    Text=self._build_ssml(message),
                    TextType="ssml",
                    OutputFormat="mp3",
                    VoiceId=self.polly_voice,
                )
            else:
                response = self.polly_client.synthesize_speech(
                    Text=message,
                    OutputFormat="mp3",
                    VoiceId=self.polly_voice,
                )
            audio_stream = response.get("AudioStream")
            if audio_stream is None:
                raise RuntimeError("AWS Polly returned no audio stream.")

            with open(sound_file, "wb") as out_file:
                out_file.write(audio_stream.read())

            self._play_audio_file(sound_file)
        except Exception as exc:
            print(f"AWS Polly voice failed: {exc}")
            print(f"[VOICE] {message}")

    def speak(self, message, cache_key=None):
        """Speak a message using cached audio if possible, otherwise fallback."""
        if not message:
            return

        if self.engine is not None:
            if cache_key:
                sound_file = self._cache_path(cache_key, extension="wav")
                if not os.path.exists(sound_file):
                    try:
                        self.engine.save_to_file(message, sound_file)
                        self.engine.runAndWait()
                    except Exception:
                        self.engine.say(message)
                        self.engine.runAndWait()
                        return

                try:
                    if platform.system() == "Windows":
                        import winsound

                        winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
                        return
                    self.engine.say(message)
                    self.engine.runAndWait()
                except Exception:
                    self.engine.say(message)
                    self.engine.runAndWait()
            else:
                self.engine.say(message)
                self.engine.runAndWait()

        elif self.use_local_tts:
            self._speak_local(message)

        elif self.use_aws_polly:
            sound_file = self._cache_path(cache_key or f"polly_{hash(message)}", extension="mp3")
            if not os.path.exists(sound_file):
                self._speak_with_polly(message, sound_file)
            else:
                self._play_audio_file(sound_file)

        elif self.have_winsound:
            import winsound

            try:
                winsound.Beep(1000, 200)
            except Exception:
                try:
                    winsound.MessageBeep(winsound.MB_OK)
                except Exception:
                    print(f"[VOICE] {message}")
            else:
                print(f"[VOICE] {message}")
        else:
            print(f"[VOICE] {message}")

    def beep(self):
        """Play a short beep if available."""
        if self.have_winsound:
            import winsound

            try:
                winsound.Beep(1000, 200)
            except Exception:
                try:
                    winsound.MessageBeep(winsound.MB_OK)
                except Exception:
                    print("*beep*")
        else:
            print("*beep*")


def welcome_user():
    """Greet the user and get their name."""
    print(MESSAGES["welcome_title"])
    print(MESSAGES["welcome_text"])
    print()
    user_name = input("What is your name? ").strip() or "Athlete"
    return user_name


def get_workout_tasks():
    """Return a copy of workout tasks from config."""
    return [task.copy() for task in WORKOUT_TASKS]


def randomize_workout_tasks(all_tasks, count=DEFAULT_EXERCISE_COUNT):
    """Return a random sample of workout tasks without asking the user to choose."""
    if count >= len(all_tasks):
        return all_tasks

    selected = random.sample(all_tasks, count)
    print("\n" + MESSAGES["session_prompt"])
    for task in selected:
        print(f"  - {task['name']} ({task['duration']} seconds)")
    print(MESSAGES["random_selection"].format(count=len(selected)))
    return selected


def get_rest_duration():
    """Ask the user for break time between exercises and return a valid integer."""
    user_input = input(MESSAGES["rest_prompt"].format(default_rest=DEFAULT_REST)).strip()
    if not user_input:
        return DEFAULT_REST
    try:
        rest_time = int(user_input)
        if rest_time < MIN_REST:
            print(MESSAGES["too_short_rest"].format(default_rest=DEFAULT_REST))
            return DEFAULT_REST
        return rest_time
    except ValueError:
        print(MESSAGES["invalid_rest"].format(default_rest=DEFAULT_REST))
        return DEFAULT_REST


def countdown(seconds, voice_coach, message_prefix="Time remaining", voice_updates=True):
    """Countdown loop that prints the remaining seconds more accurately."""
    if not voice_updates:
        print(f"{message_prefix}: {seconds}s")
        time.sleep(seconds)
        print("".ljust(40), end="\r")
        return

    start_time = time.monotonic()
    end_time = start_time + seconds
    last_remaining = None
    while True:
        now = time.monotonic()
        remaining = max(0, math.ceil(end_time - now))
        if remaining != last_remaining:
            if remaining % 5 == 0 or remaining <= 5:
                voice_coach.speak(
                    f"{message_prefix} {remaining} seconds",
                    cache_key=f"countdown_{message_prefix.replace(' ', '_')}_{remaining}",
                )
            print(f"{message_prefix}: {remaining}s", end="\r", flush=True)
            last_remaining = remaining
        if remaining == 0:
            break
        time.sleep(0.25)
    print("".ljust(40), end="\r")


def perform_exercise(task, voice_coach, user_name, rest_duration):
    """Run a single timed exercise with greeting, countdown, encouragement, and custom rest time."""
    name = task["name"]
    duration = task["duration"]
    encouragement = task["encouragement"]

    print("\n----------------------------------------")
    print(f"{user_name}, get ready for: {name}")
    voice_coach.speak(f"Get ready for {name}. Start strong, {user_name}!", cache_key=f"ready_{name}")
    time.sleep(2)

    for prep in range(3, 0, -1):
        print(f"Starting in {prep}...")
        voice_coach.beep()
        time.sleep(1)

    print(f"Go! {name} for {duration} seconds!")
    voice_coach.speak(f"Go! {name} for {duration} seconds.", cache_key=f"go_{name}")

    encouragement_times = set()
    if duration >= 10:
        encouragement_times.add(duration // 2)

    start_time = time.monotonic()
    end_time = start_time + duration
    last_remaining = None

    while True:
        now = time.monotonic()
        remaining = max(0, math.ceil(end_time - now))
        if remaining != last_remaining:
            if remaining in encouragement_times:
                voice_coach.speak(encouragement, cache_key=f"encourage_{name}_{remaining}")
            if remaining % 5 == 0 or remaining <= 5:
                voice_coach.speak(
                    str(remaining),
                    cache_key=f"time_{name.replace(' ', '_')}_{remaining}",
                )
            if remaining <= 5 and remaining > 0:
                voice_coach.beep()
            print(f"{name} - {remaining:2d}s left", end="\r", flush=True)
            last_remaining = remaining
        if remaining == 0:
            break
        time.sleep(0.25)

    print("".ljust(80), end="\r")
    print(f"{name} complete! Take a quick break.")
    voice_coach.speak(f"Great job, {user_name}! {name} complete.", cache_key=f"complete_{name}")
    if rest_duration > 0:
        print(f"Rest for {rest_duration} seconds.")
        countdown(rest_duration, voice_coach, message_prefix="Rest time remaining", voice_updates=False)


def run_workout_session():
    """Start the workout session with the full exercise list."""
    voice_coach = VoiceCoach()
    user_name = welcome_user()

    print()
    print(MESSAGES["voice_enabled"] if voice_coach.voice_available else MESSAGES["voice_disabled"])
    print()
    voice_coach.speak(f"Welcome {user_name}! Let's begin your workout.", cache_key="welcome")

    all_tasks = get_workout_tasks()
    selected_tasks = randomize_workout_tasks(all_tasks)
    rest_duration = get_rest_duration()

    print(MESSAGES["session_summary"].format(count=len(selected_tasks), rest=rest_duration))
    voice_coach.speak(MESSAGES["session_summary"].format(count=len(selected_tasks), rest=rest_duration), cache_key="session_summary")

    for task in selected_tasks:
        perform_exercise(task, voice_coach, user_name, rest_duration)

    print("\n" + MESSAGES["workout_complete"])
    voice_coach.speak(MESSAGES["workout_complete"], cache_key="workout_complete")


if __name__ == "__main__":
    run_workout_session()
