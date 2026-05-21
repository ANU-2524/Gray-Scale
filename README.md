# GrayVedio

A simple real-time grayscale video processing tool using OpenCV.

## Features
- Real-time webcam feed in grayscale.
- Capture and save frames as images with timestamped filenames.
- Record the grayscale stream to a video file.
- Command-line interface for easy configuration.

## Requirements
- Python 3.x
- OpenCV (`opencv-python`)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the script with default settings:
```bash
python grayyyVedioo.py
```

### Options
- `--camera`: Specify the camera index (default is 0).
- `--output`: Path to save the recorded grayscale video (e.g., `output.avi`).

Example - Record to a file:
```bash
python grayyyVedioo.py --output output.avi
```

### Controls
While the application is running, focus on the video window:
- Press **'s'** to save the current frame as a `.png` file.
- Press **'q'** to quit the application.

## License
MIT

