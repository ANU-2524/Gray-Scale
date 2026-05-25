# Example Usage Guide for GrayVideo Enhanced

This guide shows practical examples of how to use GrayVideo Enhanced in different scenarios.

## Basic Usage Examples

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

## Practical Scenarios

### Scenario 1: Content Creator Recording
Record high-quality filtered content:
```bash
python video_processor.py --source 0 --output "vlog_session.avi"
```
Then press 'e' for Sepia filter or 'o' for Cartoon effect!

### Scenario 2: Video Effect Testing
Test different filters on a video file:
```bash
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
