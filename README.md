# Python Speech Recognition — AI Toolkit

A clean, production‑ready Python project that demonstrates offline audio loading and
cloud‑based speech transcription using the excellent [`SpeechRecognition`](https://pypi.org/project/SpeechRecognition/) package.

- **CLI** for quick transcriptions
- **Segment decoding** with `--start-ms` and `--end-ms`
- **Noise handling** via calibrated ambient noise (`--noise-seconds`)
- **Typed API** you can import in your notebooks or apps
- **Tests + CI + Ruff/Black**

> Author: **Mobin Yousefi** (GitHub: [github.com/mobinyousefi-cs](https://github.com/mobinyousefi-cs))

---

## 1) Quick Start

```bash
# 1) Create and activate a venv (recommended)
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install
pip install -e .

# 3) Transcribe a file (Google Web Speech API via SpeechRecognition default key)
sr-cli transcribe path/to/audio.wav

# Options
sr-cli transcribe path/to/audio.wav --start-ms 5000 --end-ms 15000 --noise-seconds 0.5
```

Supported audio containers via `SpeechRecognition.AudioFile`: **WAV (PCM/LPCM), AIFF, AIFF-C, FLAC**.

> ⚠️ For FLAC on Windows you may need a `flac` binary in `PATH`. See the
> [SpeechRecognition docs](https://pypi.org/project/SpeechRecognition/).

Sample U.S. English audio corpus: <http://www.voiptroubleshooter.com/open_speech/american.html>

---

## 2) Features

- **Segment transcription** using `offset` and `duration` (no custom slicing needed)
- **Automatic energy threshold**: `--noise-seconds` triggers `adjust_for_ambient_noise`
- **Deterministic mode**: set `--energy-threshold` to skip noise calibration
- **Pluggable backends** (Google by default). Stubs included for IBM/PocketSphinx.

---

## 3) API Usage

```python
from speech_recognition_ai.recognize import transcribe
text = transcribe(
    path="sample.wav",
    start_ms=0,
    end_ms=None,
    noise_seconds=0.5,
    backend="google",
)
print(text)
```

---

## 4) CLI

```bash
sr-cli transcribe sample.wav \
  --start-ms 0 \
  --end-ms 10000 \
  --noise-seconds 0.5 \
  --language en-US
```

Run `sr-cli --help` for all options.

---

## 5) Testing

```bash
pip install -e .
pip install pytest
pytest
```

---

## 6) Project Structure

```
python-speech-recognition-ai/
├─ src/
│  └─ speech_recognition_ai/
│     ├─ __init__.py
│     ├─ recognize.py
│     └─ cli.py
├─ tests/
│  ├─ test_audio_dummy.py
│  └─ test_recognize.py
├─ pyproject.toml
├─ README.md
├─ LICENSE
├─ .gitignore
├─ .editorconfig
└─ .github/workflows/ci.yml
```

---

## 7) Notes on Accuracy & Noise

- Real‑world audio benefits from a short calibration window (`--noise-seconds 0.3–1.0`).
- For long audios, decode in chunks with `--start-ms/--end-ms` in a loop.
- Google Web Speech API enforces length/size limits; for heavy workloads consider
  dedicated APIs (AssemblyAI, Google Cloud Speech‑to‑Text, Vosk/PocketSphinx for offline).

---

## 8) License

MIT — see `LICENSE`.