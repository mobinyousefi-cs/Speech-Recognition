#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: Python Speech Recognition — AI Toolkit
File: test_audio_dummy.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-10-25
Updated: 2025-10-25
License: MIT License (see LICENSE file for details)
===========================================================================

Description:
Sanity tests that do not require actual audio or network.
===========================================================================
"""

from speech_recognition_ai import transcribe


def test_transcribe_unsupported_backend_raises(tmp_path):
    p = tmp_path / "silent.wav"
    p.write_bytes(b"\x52\x49\x46\x46")  # not a real wave, just to hit SR error path later
    try:
        transcribe(str(p), backend="not-a-backend")
    except ValueError as e:
        assert "Unsupported backend" in str(e)
    else:  # pragma: no cover - make sure we fail if no error
        assert False