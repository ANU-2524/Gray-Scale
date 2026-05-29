# Example Usage Guide for GrayVideo Enhanced

This guide shows practical examples of how to use GrayVideo Enhanced in different scenarios.

## Quick Start Examples

### 1. Simple Webcam Processing
The most basic usage - just open your webcam:
```bash
python video_processor.py
```

### 2. Use a Specific Camera
If you have multiple cameras connected:
```bash
python video_processor.py --source 0  # First camera
python video_processor.py --source 1  # Second camera
python video_processor.py --source 2  # Third camera, etc.
```

### 3. Process a Video File
Convert a video file with filters:
```bash
python video_processor.py --source "path/to/video.mp4"
```

### 4. Record Webcam Output
Record your webcam stream with filters applied:
```bash
python video_processor.py --output "my_recording.avi"
```

### 5. Process and Record
Apply filters to a video file and save the result:
```bash
python video_processor.py --source "input.mp4" --output "output.avi"
```

## Performance Optimization Examples

### For Low-End Hardware
Reduce resolution to 50% and limit to 15 FPS:
```bash
python video_processor.py --scale 0.5 --fps 15
```

### For Better Performance on Standard Hardware
Use 75% resolution with 30 FPS:
```bash
python video_processor.py --scale 0.75 --fps 30
```

### High-Quality HD Processing
Process at full resolution with 30 FPS:
```bash
python video_processor.py --fps 30 --scale 1.0
```

### Ultra-High Frame Rate (60 FPS)
For smooth high-speed recording:
```bash
python video_processor.py --fps 60 --scale 0.75
```

## Content Creator Scenarios

### Scenario 1: Record High-Quality Sepia-Filtered Vlog
```bash
python video_processor.py --source 0 --output "vlog_session.avi" --fps 30
```
Then press **e** while running to apply the Sepia filter.

### Scenario 2: Test Filters on Video File
```bash
python video_processor.py --source "input_video.mp4" --fps 30
```
Press different filter keys (g, e, k, i, b, c, o) to test each one in real-time.

### Scenario 3: Create Artistic Video Recording
```bash
python video_processor.py --output "artistic.avi" --fps 30
```
- Press **o** for Cartoon effect
- Press **]** to increase brightness for artistic look
- Press **s** to save individual frames as snapshots

### Scenario 4: Create Edge-Detected Video
```bash
python video_processor.py --source "input.mp4" --output "edges.avi"
```
Then press **c** for Canny edge detection while processing.

## Advanced Recording Examples

### Scenario 5: Multi-Resolution Recording Comparison
Record the same scene at different resolutions:
```bash
# Full resolution
python video_processor.py --output "full_resolution.avi" --scale 1.0

# Half resolution (smaller file)
python video_processor.py --output "half_resolution.avi" --scale 0.5

# Double resolution (requires good hardware)
python video_processor.py --output "high_resolution.avi" --scale 1.5
```

### Scenario 6: Time-Lapse Style Processing
Process a video file at lower FPS to simulate time-lapse:
```bash
python video_processor.py --source "video.mp4" --output "timelapse.avi" --fps 10
```

### Scenario 7: Continuous Live Recording with Snapshots
Record live camera feed and save key frames:
```bash
python video_processor.py --source 0 --output "live_record.avi"
```
Press **s** to capture snapshots during recording (saved in `snapshots/` folder).

## Filter-Specific Examples

### Grayscale Video Creation
```bash
python video_processor.py --source "color_video.mp4" --output "grayscale.avi"
```
Then press **g** immediately to apply and record grayscale.

### Sketch-Effect Video
```bash
python video_processor.py --source "input.mp4" --output "sketch_effect.avi" --fps 24
```
Press **k** to apply sketch filter, then let it record.

### Cartoon-Effect Video
```bash
python video_processor.py --output "cartoon_recording.avi"
```
Press **o** for cartoon effect and record your own video.

### Sepia Tone Processing
```bash
python video_processor.py --source "old_video.mp4" --output "vintage.avi"
```
Press **e** for sepia tone for a vintage look.

## Workflow Examples

### Workflow 1: Process Video and Save Multiple Versions
```bash
# Create normal version
python video_processor.py --source "original.mp4" --output "processed.avi"

# Create half-resolution version
python video_processor.py --source "original.mp4" --output "processed_hd.avi" --scale 1.5

# Create mobile-friendly version
python video_processor.py --source "original.mp4" --output "processed_mobile.avi" --scale 0.5
```

### Workflow 2: Quality Testing
```bash
# Test on low-end system
python video_processor.py --fps 15 --scale 0.5

# Test on standard system
python video_processor.py --fps 30 --scale 0.75

# Test on high-end system
python video_processor.py --fps 60 --scale 1.0
```

### Workflow 3: Camera Calibration
Check different cameras:
```bash
python video_processor.py --source 0  # Built-in camera
python video_processor.py --source 1  # USB camera
python video_processor.py --source 2  # External camera
```

## Tips and Tricks

### Tip 1: Save Snapshot Library
While recording, periodically press **s** to save artistic snapshots:
```bash
python video_processor.py --source 0 --output "recording.avi"
```
Create a gallery by pressing **s** at interesting moments (files saved in `snapshots/`).

### Tip 2: Adjust in Real-Time
While running, you can:
- Adjust brightness: **[** or **]**
- Adjust contrast: **-** or **=**
- Switch filters: **g, e, k, i, b, c, o, n**
- Reset all: **r**
- Help: **h**

### Tip 3: Record and Review
1. Record with `--output recording.avi`
2. Stop recording (press **q**)
3. Playback: `python video_processor.py --source recording.avi`
4. Review output and adjust settings
5. Re-record if needed

### Tip 4: Performance Tuning
If you're getting low FPS:
1. Try reducing resolution: `--scale 0.5`
2. Limit frame rate: `--fps 20`
3. Both together: `--scale 0.5 --fps 20`

## System Requirements by Use Case

### Casual Webcam Preview
- Resolution: 640x480 (no resizing needed)
- FPS: 24-30
- Command: `python video_processor.py`

### HD Recording
- Resolution: 1280x720 or 1920x1080
- FPS: 24-30
- Command: `python video_processor.py --fps 30`

### Low-End Device (Raspberry Pi, Old Laptop)
- Resolution: 320x240 (0.5 scale)
- FPS: 15
- Command: `python video_processor.py --scale 0.5 --fps 15`

### 4K Processing (High-End Only)
- Resolution: 3840x2160 or reduced
- FPS: 30
- Command: `python video_processor.py --fps 30 --scale 1.0`

python video_processor.py --source "raw_footage.mp4"
```
- Press 'g' for Grayscale effect
- Press 'c' for Canny Edge detection
- Press 'b' for Blur effect
- Use '[' and ']' to adjust brightness

### Scenario 3: Privacy Protection
Blur video for privacy/security purposes:
```bash
python video_processor.py --source "meeting_video.mp4" --output "blurred_output.avi"
```
Press 'b' to enable Blur filter for the entire video

### Scenario 4: Photography/Snapshot Session
Capture individual frames from video:
```bash
python video_processor.py --source 0
```
Press 's' to save each snapshot to the `snapshots/` folder

### Scenario 5: Batch Processing with Different Effects
Process the same video multiple times with different filters:
```bash
# Record with Grayscale
python video_processor.py --source "source.mp4" --output "output_bw.avi"

# Then record again with different filter...
python video_processor.py --source "source.mp4" --output "output_sepia.avi"
```

## Keyboard Shortcut Reference

Keep these shortcuts handy while using the app:

| Task | Keys |
|------|------|
| Change Filters | 'n' (normal), 'g' (grayscale), 'e' (sepia), 'k' (sketch), etc. |
| Adjust Brightness | '[' (decrease), ']' (increase) |
| Adjust Contrast | '-' (decrease), '=' (increase) |
| Save Frame | 's' |
| Reset Settings | 'r' |
| Quit | 'q' |

## Tips & Tricks

1. **Quick Reset**: Press 'r' to reset brightness, contrast, and filter
2. **Smooth Transitions**: Adjust brightness/contrast gradually using [ ] and - = keys
3. **Preview Before Recording**: Always preview a filter by pressing the key first
4. **Efficient Storage**: Blur filter (press 'b') can reduce video file size
5. **Performance**: Use simpler filters like Grayscale for better performance

## Troubleshooting Tips

If your camera doesn't work:
- Close any other camera applications
- Try a different camera index (--source 1, --source 2, etc.)
- Restart the application

If recording fails:
- Ensure the output directory is writable
- Check that you have enough disk space
- Try a different video format or filename

## File Output

### Snapshot Files
Saved to `snapshots/` directory with timestamp naming:
```
snapshots/capture_20240525_143022.png
snapshots/capture_20240525_143045.png
```

### Video Recordings
Saved to your specified output path:
```
session_output.avi
my_recording.avi
processed_video.avi
```

---

For more information, see [README.md](README.md)
