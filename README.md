# Mac Thump Mourner

A small Python prank script that makes your Mac **play a mourn sound when you hit/tap it**.

The script listens to microphone input and detects a loud "thump". When detected, it plays a sound using `afplay`.

## Requirements

- Python 3
- macOS
- Python packages:
  - sounddevice
  - numpy

Install dependencies:

```bash
pip install sounddevice numpy

