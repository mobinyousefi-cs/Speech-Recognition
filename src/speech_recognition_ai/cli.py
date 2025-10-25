#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: Python Speech Recognition — AI Toolkit
File: cli.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-10-25
Updated: 2025-10-25
License: MIT License (see LICENSE file for details)
===========================================================================

Description:
Command-line interface (CLI) for transcribing audio files.

Usage:
    sr-cli transcribe path/to/audio.wav --start-ms 0 --end-ms 10000 --noise-seconds 0.5
===========================================================================
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .recognize import transcribe


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sr-cli", description="Speech recognition CLI (Google backend)")
    sub = p.add_subparsers(dest="command", required=True)

    t = sub.add_parser("transcribe", help="Transcribe an audio file")
    t.add_argument("path", type=Path, help="Path to audio file (WAV/AIFF/FLAC)")
    t.add_argument("--start-ms", type=int, default=None, help="Start offset in ms")
    t.add_argument("--end-ms", type=int, default=None, help="End offset in ms")
    t.add_argument("--language", type=str, default="en-US", help="Language code, e.g., en-US, fa-IR")
    t.add_argument("--backend", type=str, default="google", help="Backend: google (default)")
    t.add_argument(
        "--noise-seconds",
        type=float,
        default=0.0,
        help="Ambient noise calibration window in seconds (0 to disable)",
    )
    t.add_argument(
        "--energy-threshold",
        type=int,
        default=None,
        help="Fixed energy threshold; if set, calibration is skipped",
    )
    t.add_argument(
        "--show-all",
        action="store_true",
        help="Print raw response if backend supports it (Google returns JSON-like dict)",
    )
    t.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON with fields: text, backend, language, start_ms, end_ms",
    )

    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "transcribe":
        if not args.path.exists():
            parser.error(f"File not found: {args.path}")

        try:
            text = transcribe(
                str(args.path),
                start_ms=args.start_ms,
                end_ms=args.end_ms,
                language=args.language,
                backend=args.backend,
                noise_seconds=args.noise_seconds,
                energy_threshold=args.energy_threshold,
                show_all=args.show_all,
            )
        except Exception as e:  # noqa: BLE001
            print(f"ERROR: {e}", file=sys.stderr)
            return 2

        if args.json:
            payload = {
                "text": text,
                "backend": args.backend,
                "language": args.language,
                "start_ms": args.start_ms,
                "end_ms": args.end_ms,
            }
            print(json.dumps(payload, ensure_ascii=False))
        else:
            print(text)

        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())