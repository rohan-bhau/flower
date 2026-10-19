#!/usr/bin/env python3
"""
flower.py — Exact Oil Pastel Flower Bouquet
"""

import os
import sys

# Auto-fallback to local .venv if system python doesn't have required packages
try:
    import cv2
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(script_dir, ".venv", "bin", "python3")
    if os.path.exists(venv_python) and sys.executable != venv_python:
        os.execv(venv_python, [venv_python] + sys.argv)
    else:
        raise

import time
import base64
import tempfile

# Suppress all Qt/Wayland warning logs
os.environ["QT_LOGGING_RULES"] = "*=false"
os.environ["OPENCV_LOG_LEVEL"] = "OFF"
import numpy as np

from canvas_data import ANIM_STREAM_B64


def load_animation_frames():
    """Decodes the in-memory animation stream into clean frame buffers."""
    raw_bytes = base64.b64decode(ANIM_STREAM_B64)
    fd, tmp_path = tempfile.mkstemp(suffix=".mp4")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(raw_bytes)

        cap = cv2.VideoCapture(tmp_path)
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()
        return frames
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def main():
    print("🎨 Rendering Oil Pastel Flower Bouquet (Duration: ~10.9s)...")
    frames = load_animation_frames()

    if not frames:
        print("Error: Could not decode animation stream.")
        sys.exit(1)

    h, w = frames[-1].shape[:2]
    window_title = "Oil Pastel"

    # WINDOW_GUI_NORMAL removes Qt toolbars (save, arrows, zoom)
    # leaving only the native OS window header with minimize, maximize, and close
    cv2.namedWindow(window_title, cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow(window_title, w, h)

    # 10s+ duration: 228 frames * 48ms = ~10.94 seconds
    delay_ms = 48

    for frame in frames:
        cv2.imshow(window_title, frame)
        key = cv2.waitKey(delay_ms)

        # Check if user closed window by clicking [X] during animation
        try:
            if cv2.getWindowProperty(window_title, cv2.WND_PROP_VISIBLE) < 1:
                cv2.destroyAllWindows()
                sys.exit(0)
        except Exception:
            sys.exit(0)

        # If user pressed any key, skip directly to completion
        if key != -1:
            break

    # Display final crystal-clear upright artwork
    final_frame = frames[-1]
    cv2.imshow(window_title, final_frame)
    print("Press any key or click [X] on the 'Oil Pastel' window to close...")

    # Hold final frame until user presses any key OR clicks the [X] close button
    while True:
        try:
            if cv2.getWindowProperty(window_title, cv2.WND_PROP_VISIBLE) < 1:
                break
        except Exception:
            break
        key = cv2.waitKey(100)
        if key != -1:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
