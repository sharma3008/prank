import time
import subprocess
import numpy as np
import sounddevice as sd

SOUND_PATH = "/Users/karthiksharmamadugula/Downloads/untitled folder 7/mourn.mp3"
SAMPLE_RATE = 44100
BLOCK_MS = 50
THRESHOLD = 0.06          # slightly more sensitive than 0.08
COOLDOWN_SEC = 1.2
DEVICE = None

block_samples = int(SAMPLE_RATE * (BLOCK_MS / 1000.0))
last_trigger = 0.0

def play_sound():
    subprocess.Popen(["afplay", SOUND_PATH])  # don't suppress output while testing

def callback(indata, frames, time_info, status):
    global last_trigger
    if status:
        print("Audio status:", status)

    rms = float(np.sqrt(np.mean(np.square(indata))))
    now = time.time()

    # print a live RMS meter (lightweight)
    print(f"\rRMS: {rms:.4f}  (threshold {THRESHOLD})   ", end="")

    if rms >= THRESHOLD and (now - last_trigger) >= COOLDOWN_SEC:
        last_trigger = now
        print(f"\nTRIGGER ✅  rms={rms:.4f}")
        play_sound()

def main():
    print("Listening for thumps... (Ctrl+C to stop)")
    print(f"Sound: {SOUND_PATH}")
    print(f"Threshold: {THRESHOLD} | Cooldown: {COOLDOWN_SEC}s | Block: {BLOCK_MS}ms")

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