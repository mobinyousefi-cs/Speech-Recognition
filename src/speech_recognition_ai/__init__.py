#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: Python Speech Recognition — AI Toolkit
File: __init__.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-10-25
Updated: 2025-10-25
License: MIT License (see LICENSE file for details)
===========================================================================

Description:
Package init for the speech recognition toolkit.

===========================================================================
"""

from .recognize import transcribe  # re-export for convenience

__all__ = ["transcribe"]