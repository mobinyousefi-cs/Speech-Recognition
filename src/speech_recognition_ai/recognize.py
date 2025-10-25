#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: Python Speech Recognition — AI Toolkit
File: recognize.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-10-25
Updated: 2025-10-25
License: MIT License (see LICENSE file for details)
===========================================================================

Description:
Typed recognition utilities built on top of the `SpeechRecognition` package.
Supports segment decoding, optional ambient-noise calibration, and multiple backends.

Usage:
    from speech_recognition_ai.recognize import transcribe
    text = transcribe("sample.wav", start_ms=0, end_ms=10_000, noise_seconds=0.5)

Notes:
- Supported containers: WAV (PCM/LPCM), AIFF, AIFF-C, FLAC per SpeechRecognition.AudioFile
- Default backend is Google Web Speech API (generic key). Consider limits.
===========================================================================
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import speech_recognition as sr


@dataclass
class TranscribeConfig:
    """Configuration for transcription.

    Attributes:
        language: BCP-47 language code (e.g., "en-US", "fa-IR").
        backend: Which recognizer backend to use: "google" (default).
        noise_seconds: If > 0, call `adjust_for_ambient_noise` with this duration.
        energy_threshold: If set, overrides recognizer.energy_threshold (skips calibration).
    """

    language: str = "en-US"
    backend: str = "google"
    noise_seconds: float = 0.0
    energy_threshold: Optional[int] = None


def _apply_noise_strategy(recognizer: sr.Recognizer, source: sr.AudioSource, cfg: TranscribeConfig) -> None:
    """Optionally calibrate for ambient noise or set a fixed energy threshold."""
    if cfg.energy_threshold is not None:
        recognizer.energy_threshold = cfg.energy_threshold
        return
    if cfg.noise_seconds and cfg.noise_seconds > 0:
        recognizer.adjust_for_ambient_noise(source, duration=cfg.noise_seconds)


def transcribe(
    path: str,
    *,
    start_ms: Optional[int] = None,
    end_ms: Optional[int] = None,
    language: str = "en-US",
    backend: str = "google",
    noise_seconds: float = 0.0,
    energy_threshold: Optional[int] = None,
    show_all: bool = False,
) -> str:
    """Transcribe an audio file using SpeechRecognition.

    Args:
        path: Path to audio file (WAV, AIFF/AIFF-C, or FLAC).
        start_ms: Optional start offset in milliseconds.
        end_ms: Optional end offset in milliseconds.
        language: Language code for recognition (default: "en-US").
        backend: "google" (default). Stubs exist for other providers.
        noise_seconds: Calibrate ambient noise for this many seconds.
        energy_threshold: Fixed energy threshold; if set, calibration is skipped.
        show_all: Return raw response when supported (Google returns dict).

    Returns:
        Recognized text (best hypothesis) or empty string if nothing is recognized.

    Raises:
        ValueError: If `end_ms` < `start_ms` or backend unsupported.
    """
    if start_ms is not None and end_ms is not None and end_ms < start_ms:
        raise ValueError("end_ms must be >= start_ms")

    # Convert offset/duration to seconds for SR
    offset_sec = (start_ms or 0) / 1000.0
    duration_sec = None
    if end_ms is not None:
        duration_sec = (end_ms - (start_ms or 0)) / 1000.0

    cfg = TranscribeConfig(language=language, backend=backend, noise_seconds=noise_seconds, energy_threshold=energy_threshold)

    recognizer = sr.Recognizer()

    with sr.AudioFile(path) as source:
        _apply_noise_strategy(recognizer, source, cfg)
        audio = recognizer.record(source, offset=offset_sec, duration=duration_sec)

    try:
        if cfg.backend == "google":
            # Uses the free Google Web Speech API with a default key inside SpeechRecognition.
            if show_all:
                result = recognizer.recognize_google(audio, language=cfg.language, show_all=True)
                return str(result)
            return recognizer.recognize_google(audio, language=cfg.language)
        # Future extension points (placeholders):
        elif cfg.backend == "ibm":
            raise NotImplementedError("IBM backend not wired. Provide credentials and implement.")
        elif cfg.backend == "sphinx":
            # Offline engine (requires pocketsphinx installed). Uncomment to enable.
            # return recognizer.recognize_sphinx(audio, language=cfg.language)
            raise NotImplementedError("PocketSphinx backend requires pocketsphinx; not enabled by default.")
        else:
            raise ValueError(f"Unsupported backend: {cfg.backend}")
    except sr.UnknownValueError:
        return ""  # nothing intelligible
    except sr.RequestError as e:
        # Network issues, API limits, etc.
        raise RuntimeError(f"Recognition service failed: {e}") from e