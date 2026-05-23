# GrayVideo Enhanced Pro

A highly sophisticated real-time video processing tool using OpenCV with advanced filters, recording capabilities, and manual image adjustments.

## Features
- **Real-time Filters**: Toggle between multiple professional filters:
  - **Grayscale**: Classic black and white.
  - **Sepia**: Vintage warm tone.
  - **Sketch**: Hand-drawn pencil effect.
  - **Invert**: Negative color mode.
  - **Blur**: Gaussian blur for privacy or aesthetics.
  - **Canny**: High-contrast edge detection.
  - **Cartoon**: Stylized cartoonish rendering.
- **Manual Adjustments**: Dynamic Control over **Brightness** and **Contrast** in real-time.
- **Dynamic Recording**: Record the video stream with all filters and adjustments applied.
- **Auto-Snapshots**: Save individual processed frames to a dedicated `snapshots/` folder.
- **Source Flexibility**: Supports webcams, professional cameras, and video files.
- **Pro HUD**: Modern overlay with FPS monitoring, active filter status, adjustment levels, and a blinking recording indicator.

## Requirements
- Python 3.x
- Dependencies: `opencv-python`, `numpy`

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the script:
```bash
python video_processor.py
```

### Options
- `--source`: Camera index (e.g., `0`) or path to a video file (e.g., `input.mp4`).
- `--output`: Path to save the recorded video (e.g., `session_output.avi`).

### Comprehensive Controls
| Key | Action |
|-----|--------|
| **'q'** | Quit Application |
| **'s'** | Save Frame (Snapshot) |
| **'r'** | Reset All Filters & Adjustments |
| **'n'** | Toggle Normal Mode (No Filter) |
| **'g'** | Grayscale Filter |
| **'e'** | Sepia Filter |
| **'k'** | Sketch Filter |
| **'i'** | Invert Filter |
| **'b'** | Blur Filter |
| **'c'** | Canny Edge Filter |
| **'o'** | Cartoon Filter |
| **'[' / ']'** | Decrease / Increase Brightness |
| **'-' / '='** | Decrease / Increase Contrast |

## License
MIT

