import base64
import os
import platform
import shutil
import subprocess
import sys


def powershell_encoded_command(script: str) -> str:
    return base64.b64encode(script.encode("utf-16-le")).decode("ascii")


def test_windows_tts(message: str) -> None:
    if not platform.system().startswith("Win"):
        print("Windows TTS test is only supported on Windows.")
        return

    if shutil.which("powershell") is None:
        print("PowerShell not found on PATH.")
        return

    script = (
        "Add-Type -AssemblyName System.Speech; "
        " $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        " $s.SetOutputToDefaultAudioDevice(); "
        " $s.Rate = 0; $s.Volume = 100; "
        f" $s.Speak('{message.replace("'", "''")}')"
    )

    encoded = powershell_encoded_command(script)
    cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-EncodedCommand", encoded]
    print("Running PowerShell TTS command:", " ".join(cmd))

    try:
        subprocess.run(cmd, check=True)
        print("TTS playback succeeded.")
    except subprocess.CalledProcessError as exc:
        print("PowerShell TTS failed:", exc)
    except Exception as exc:
        print("Unexpected error during PowerShell TTS:", exc)


def test_beep() -> None:
    if not platform.system().startswith("Win"):
        print("Beep test is only supported on Windows.")
        return

    try:
        import winsound
        print("Playing standard Windows beep...")
        winsound.Beep(750, 500)
        print("Beep succeeded.")
    except Exception as exc:
        print("winsound beep failed:", exc)


def main() -> None:
    print("Sound test running on:", platform.platform())
    if platform.system().startswith("Win"):
        test_beep()
        test_windows_tts("Sound test: this is a sample voice announcement.")
    else:
        print("Non-Windows platform detected. No sound test available.")


if __name__ == "__main__":
    main()
