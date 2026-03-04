import time
import subprocess
import numpy as np
import sounddevice as sd
from pathlib import Path

# ====== CONFIG ======
BASE_DIR = Path(__file__).resolve().parent          # folder where this script lives
SOUND_PATH = str(BASE_DIR / "mourn.mp3")            # mourn.mp3 in same folder

SAMPLE_RATE = 44100
BLOCK_MS = 50
THRESHOLD = 0.08
COOLDOWN_SEC = 1.2
DEVICE = None
# ====================

block_samples = int(SAMPLE_RATE * (BLOCK_MS / 1000.0))
last_trigger = 0.0

def play_sound():
    subprocess.Popen(["afplay", SOUND_PATH],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)

def callback(indata, frames, time_info, status):
    global last_trigger
    if status:
        return

    rms = float(np.sqrt(np.mean(np.square(indata))))
    now = time.time()

    if rms >= THRESHOLD and (now - last_trigger) >= COOLDOWN_SEC:
        last_trigger = now
        play_sound()

def main():
    print("Listening for thumps... (Ctrl+C to stop)")
    print(f"Sound file: {SOUND_PATH}")
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        blocksize=block_samples,
        device=DEVICE,
        callback=callback,
    ):
        while True:
            time.sleep(1)

if __name__ == "__main__":
    main()