# 🎶 Cymatic Audio Visualization — Project Overview

## Goal:
This project aims to create a **real-time, GPU-accelerated 3D cymatic visualization** that reacts to **live music input**. It will render a **grid-like mesh** that dynamically deforms in response to the audio’s amplitude and frequency spectrum. The visualization is intended to be **displayed on a large screen**, making it suitable for **live events, performances, or installations**.

The long-term plan includes support for **MIDI input** as an additional or alternative data source to manipulate visuals.

---

## Core Features

### 🎛️ Audio-Driven Grid
- A **3D grid mesh** in the XZ plane, animated via **Y-axis displacement** based on real-time audio analysis.
- Audio features like **amplitude**, **frequency bands**, and **beat pulses** will control mesh deformation and color.
- Mesh updates and visual effects are handled on the **GPU** via custom **GLSL shaders**.

### 🎧 Real-Time Audio Input
- Captures live audio using the **`sounddevice`** library.
- Extracts meaningful features using **`librosa`** (e.g., FFT, Mel bands, volume).
- Smooths and normalizes data before passing to shaders.

### ⚙️ GPU Rendering
- Uses **ModernGL** for fast, OpenGL-based rendering in Python.
- Vertex and fragment shaders deform and color the mesh in real-time.
- Shader inputs include:
  - Time
  - Normalized audio texture (1D)
  - Optional MIDI input (future)

### 🖥️ Visual Output
- Grid visualization supports **dynamic camera movement** and can render in **fullscreen mode**.
- Visuals are optimized for **high-resolution displays** and large projection setups.
- Optional post-processing effects such as **blur**, **motion trails**, and **color grading** will be implemented later.

---

## Future Extensions

### 🔌 MIDI Control
- Add MIDI device support using `mido` or `python-rtmidi`.
- Use MIDI notes, velocities, or CC signals to trigger visual effects or override audio input.

### 🌈 Post-Processing
- Add framebuffer effects like bloom, feedback trails, and motion blur.
- Use framebuffer objects (FBOs) to layer visual complexity.

### 🧠 AI/ML Ideas
- Optional real-time music classification (genre, mood) using deep learning.
- Visual changes based on predicted musical characteristics.

---

## Development Tools

- **Language:** Python 3.11+
- **Editor:** Visual Studio Code
- **Rendering:** [`moderngl`](https://moderngl.readthedocs.io/)
- **Audio Input:** [`sounddevice`](https://python-sounddevice.readthedocs.io/)
- **Audio Analysis:** [`librosa`](https://librosa.org/)
- **Mesh/Math Utils:** `numpy`
- **MIDI Support:** (Future) `mido`, `python-rtmidi`
- **Windowing:** `moderngl-window`, `pyglet`, or `glfw` (TBD)

---

## Current Status
> ✅ Planning  
> 🔧 Initial setup pending  
> 🎨 Starting with a static grid + basic shader

---

## Usage (eventually)
```bash
python main.py
