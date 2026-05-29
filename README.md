# GrayVideo Enhanced Pro

A professional-grade real-time video processing application built with Python and OpenCV. Process live video streams from webcams, professional cameras, or video files with advanced filters, brightness/contrast adjustments, and recording capabilities.

![Version](https://img.shields.io/badge/version-2.1-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ Features

- **🎨 Real-time Filters**: 8 professional filters including Grayscale, Sepia, Sketch, Invert, Blur, Canny Edge Detection, and Cartoon effects
- **🎚️ Live Adjustments**: Dynamic control over brightness and contrast in real-time
- **📹 Dynamic Recording**: Record processed video with all filters and adjustments applied
- **📸 Auto-Snapshots**: Save individual frames to a dedicated `snapshots/` folder
- **📱 Source Flexibility**: Support for webcams, professional cameras, and video files
- **⚡ Performance Optimization**: Frame resizing and FPS limiting for smooth processing on any hardware
- **🎯 Pro HUD**: Modern overlay with FPS monitoring, filter status, adjustment levels, and recording indicator
- **🔒 Clean Code**: Type hints, comprehensive docstrings, and detailed logging throughout

## System Requirements

- **Python**: 3.7 or higher
- **OS**: Windows, macOS, or Linux
- **Camera**: USB webcam or integrated camera (or video file)
- **Disk Space**: 500MB for dependencies, additional space for video recording

## Dependencies

- `opencv-python>=4.5.0` - Video processing and computer vision
- `numpy>=1.19.0` - Numerical computing library

## Installation

### Step 1: Clone or Download
```bash
cd GrayVedio
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Quick Start

Run the script with default settings (uses your primary webcam):
```bash
python video_processor.py
```

## Advanced Usage

### Using a Different Camera
```bash
python video_processor.py --source 1
```

### Processing a Video File
```bash
python video_processor.py --source input.mp4 --output output.avi
```

### Recording Processed Output
```bash
python video_processor.py --output my_recording.avi
```

### Limiting Frame Rate (for low-end hardware)
```bash
python video_processor.py --fps 30
```

### Resizing Frames for Performance
```bash
python video_processor.py --scale 0.5    # Half resolution
python video_processor.py --scale 2.0    # Double resolution
```

### Complete Example with All Options
```bash
python video_processor.py --source video.mp4 --output processed.avi --fps 30 --scale 0.75
```

## Keyboard Controls

### Navigation
| Key | Action |
|-----|--------|
| **q** | Exit application |
| **r** | Reset all settings to defaults |
| **h** | Display this help text |

### Filters
| Key | Filter |
|-----|--------|
| **n** | Normal (no filter) |
| **g** | Grayscale - Classic black and white |
| **e** | Sepia - Vintage warm tone |
| **k** | Sketch - Hand-drawn pencil effect |
| **i** | Invert - Negative color mode |
| **b** | Blur - Gaussian blur effect |
| **c** | Canny - Edge detection |
| **o** | Cartoon - Stylized rendering |

### Adjustments
| Key | Action |
|-----|--------|
| **[** / **]** | Decrease / Increase Brightness (-100 to +100) |
| **-** / **=** | Decrease / Increase Contrast (0.1x to 3.0x) |

### Capture
| Key | Action |
|-----|--------|
| **s** | Save current frame to `snapshots/` directory |

## Troubleshooting

### Camera Not Detected
- Ensure your camera is connected and not in use by another application
- Try specifying a different camera index: `python video_processor.py --source 1`
- On some systems, you may need to grant camera permissions to the terminal

### Video File Playback Error
- Verify the file path is correct and the file exists
- Check that the file format is supported by OpenCV (MP4, AVI, MOV, etc.)
- Ensure the file is not corrupted or currently open in another application

### Recording Fails
- Ensure the output directory exists and you have write permissions
- Check available disk space (video files can be large)
- Try using a different output format (e.g., `.avi` instead of `.mp4`)

### Performance Issues (Low FPS)
- Use frame resizing: `--scale 0.5` for half resolution
- Limit frame rate: `--fps 30`
- Close other applications consuming CPU/GPU resources
- Check camera driver is up-to-date

### Black/Empty Window
- Wait a moment for the camera to initialize
- Try a different camera index
- On Linux, you may need to install: `sudo apt-get install libsm6 libxext6`

## Command Line Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `--source` | str | Camera index (0, 1, etc.) or video file path. Default: 0 |
| `--output` | str | Path to save processed video. Default: None (no recording) |
| `--fps` | int | Target frame rate in Hz. Default: None (unlimited) |
| `--scale` | float | Frame resize factor (0.25-3.0). Default: 1.0 (no resize) |

## Performance Tips

1. **For Low-End Hardware**: Use `--scale 0.5 --fps 15` for smooth operation
2. **For High-Quality Recording**: Use `--fps 30 --scale 1.0` for standard quality
3. **For Real-Time Processing**: Leave `--fps` unlimited and adjust `--scale` as needed
4. **File Format**: AVI format (`--output file.avi`) is faster than MP4 but larger file size
- Try specifying a different camera index: `python video_processor.py --source 1`
- On Windows, check Device Manager for camera conflicts

### Video File Not Found
- Use the absolute file path: `python video_processor.py --source "C:/path/to/video.mp4"`
- Check that the file format is supported by OpenCV (MP4, AVI, MOV, etc.)

### Performance Issues
- Close other applications to free up system resources
- Try reducing video resolution by editing the source video file
- Use simpler filters (Grayscale, Normal) instead of complex ones (Cartoon, Sketch)

### Recording Issues
- Ensure you have write permissions in the project directory
- Try using a different output format: `--output output.avi` instead of `.mp4`
- Free up disk space if the output file won't be created

## Project Structure

```
GrayVedio/
├── video_processor.py    # Main application with type hints & logging
├── requirements.txt      # Python dependencies
└── README.md            # Documentation
```

## Code Improvements (v2.0)

✅ **Type Hints** - Full type annotations for better IDE support
✅ **Docstrings** - Comprehensive documentation for all classes and methods
✅ **Logging** - Structured logging throughout the application
✅ **Constants** - Magic numbers extracted to named configuration constants
✅ **Error Handling** - Improved exception handling with custom messages
✅ **Code Organization** - Cleaner structure following PEP 8 guidelines
✅ **Better Arguments** - Detailed help text and usage examples

## Development

### Extending the Application

To add new filters, modify the `apply_filter()` method in the `VideoProcessor` class:

```python
elif self.filter_mode == 'your_filter':
    # Your filter implementation
    return processed_frame
```

Then add a keyboard shortcut in the `run()` method:

```python
elif key == ord('x'):  # Choose your key
    self.filter_mode = 'your_filter'
```

### Code Quality Standards

- All functions and classes have type hints
- Comprehensive docstrings follow Google style
- Configuration values are defined as constants
- Logging is used instead of print statements
- Error handling provides meaningful messages

## License

MIT - See LICENSE file for details

## Contributing

Found a bug or want to improve the project? Feel free to submit issues or pull requests!

