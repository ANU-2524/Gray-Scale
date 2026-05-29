# Quick Start Guide - GrayVideo Enhanced

Get up and running with GrayVideo Enhanced in 5 minutes!

## Installation (First Time Only)

### Windows
1. Download and install [Python 3.7+](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation
2. Open Command Prompt in the project folder
3. Run: `setup.bat`
4. Wait for installation to complete

### macOS/Linux
1. Open Terminal in the project folder
2. Run: `chmod +x setup.sh && ./setup.sh`
3. Wait for installation to complete

## Your First Run

### Step 1: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 2: Start the Application

```bash
python video_processor.py
```

You should see your webcam feed with a green HUD showing filters and adjustments!

## Basic Controls (Try These Now)

| Key | What It Does |
|-----|-------------|
| **g** | Black & white |
| **e** | Vintage sepia tone |
| **o** | Cartoon effect |
| **]** | Brighter |
| **=** | More contrast |
| **s** | Save frame |
| **q** | Exit |

## Next Steps

### Learn More Filters
- **n** = Normal (no filter)
- **k** = Sketch effect
- **i** = Invert colors
- **b** = Blur
- **c** = Edge detection

### Record Video
```bash
python video_processor.py --output my_video.avi
```
- Apply filters while recording!
- Press **q** to stop and save

### Process a Video File
```bash
python video_processor.py --source "my_video.mp4"
```

### Optimize for Your Hardware
```bash
# For older computers
python video_processor.py --fps 15 --scale 0.5

# For modern computers
python video_processor.py --fps 60
```

## Common Tasks

### Task 1: Record a Filtered Video
1. Run: `python video_processor.py --output output.avi`
2. Wait for camera to load
3. Press a filter key (e.g., **e** for sepia)
4. Do your thing!
5. Press **q** to finish
6. Find video in the project folder

### Task 2: Create a Black & White Video
1. Run: `python video_processor.py --source "your_video.mp4" --output "grayscale.avi"`
2. Press **g** (grayscale filter)
3. Let it finish processing
4. Find `grayscale.avi` in your folder

### Task 3: Save Snapshots
1. Run the application
2. Press **s** to save a snapshot
3. Find images in the `snapshots/` folder
4. Each snapshot gets a timestamp

## Getting Help

### In the Application
- Press **h** to see all keyboard shortcuts
- Press **r** to reset all settings to default

### From Command Line
```bash
python video_processor.py --help
```

Shows all available options and examples.

## Troubleshooting

### "Camera not found"
- Close other apps using the camera (Zoom, Skype, etc.)
- Try: `python video_processor.py --source 1` (if you have multiple cameras)

### "File not found"
- Use full path: `python video_processor.py --source "C:\Users\YourName\Videos\video.mp4"`
- Or move the file to the project folder

### Slow/Laggy
- Use: `python video_processor.py --fps 15 --scale 0.5`
- This makes it faster on older computers

### Recording Not Working
- Check you have space on your drive
- Try a different filename: `--output newfile.avi`

## Tips for Best Results

1. **Good Lighting** = Better video quality
2. **Close Other Apps** = Smoother performance
3. **Use Filters** = Press keys during recording to see effects live
4. **Adjust Brightness** = Use **[** and **]** to fine-tune
5. **Save Snapshots** = Press **s** to capture interesting moments

## Next: Learn Advanced Features

Check out these files for more:
- `EXAMPLES.md` - 20+ real-world examples
- `README.md` - Complete documentation
- `CONTRIBUTING.md` - How to add new features

---

**Questions?** Check the README.md or EXAMPLES.md for detailed guides!

Happy filtering! 🎬✨
