# GrayVideo Enhanced

A sophisticated real-time video processing tool using OpenCV.

## Features
- **Real-time Filters**: Switch between Grayscale, Sepia, Sketch, Invert, and Normal modes on the fly.
- **Dynamic Recording**: Record the video stream even while switching filters.
- **Frame Capture**: Save individual processed frames with a single keystroke.
- **Source Flexibility**: Use your webcam or process existing video files.
- **Performance Monitoring**: Real-time FPS display.

## Requirements
- Python 3.x
- Dependencies (OpenCV, NumPy)

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
- `--source`: Camera index (e.g., `0`) or path to a video file (e.g., `input_video.mp4`). Default is `0`.
- `--output`: Path to save the recorded video (e.g., `output.avi`).

Example - Process a video file and record:
```bash
python video_processor.py --source input.mp4 --output processed.avi
```

### Controls
While the application is running, use these keys:
- **'q'**: Quit application.
- **'s'**: Save current frame as `.png`.
- **'g'**: Grayscale mode.
- **'e'**: Sepia mode.
- **'k'**: Sketch mode.
- **'i'**: Invert mode.
- **'n'**: Normal (original) mode.

## License
MIT

