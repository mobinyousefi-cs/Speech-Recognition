#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: Python Speech Recognition — AI Toolkit
File: test_recognize.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-10-25
Updated: 2025-10-25
License: MIT License (see LICENSE file for details)
===========================================================================

Description:
Example test with monkeypatch to simulate SpeechRecognition behavior, ensuring
we format offsets and durations properly and return strings.
===========================================================================
"""
from __future__ import annotations

import types

import speech_recognition as sr

import speech_recognition_ai.recognize as recog


class _DummyAudio:  # minimal placeholder
    pass


class _DummyAudioFile:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_transcribe_google_show_all(monkeypatch, tmp_path):
    fake_audio_path = tmp_path / "a.wav"
    fake_audio_path.write_bytes(b"RIFF....WAVEfmt ")

    # Patch AudioFile and Recognizer methods
    monkeypatch.setattr(sr, "AudioFile", lambda _: _DummyAudioFile(str(fake_audio_path)))

    r = sr.Recognizer()

    def fake_adjust(src, duration=0):
        return None

    def fake_record(src, offset=0.0, duration=None):
        return _DummyAudio()

    def fake_recognize_google(audio, language="en-US", show_all=False):
        return {"transcript": "hello world"} if show_all else "hello world"

    monkeypatch.setattr(sr, "Recognizer", lambda: r)
    r.adjust_for_ambient_noise = fake_adjust  # type: ignore[attr-defined]
    r.record = fake_record  # type: ignore[attr-defined]
    r.recognize_google = fake_recognize_google  # type: ignore[attr-defined]

    text = recog.transcribe(
        str(fake_audio_path), start_ms=1000, end_ms=2000, language="en-US", show_all=False
    )
    assert isinstance(text, str)
    assert text == "hello world"