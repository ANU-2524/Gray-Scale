# Changelog

All notable changes to GrayVideo Enhanced are documented in this file.

## [2.1] - 2024-05-29

### Added
- **Frame Rate Limiting**: New `--fps` command-line option to limit frame rate for performance optimization
- **Frame Resizing**: New `--scale` option to resize frames (0.25-3.0x) for performance tuning
- **Configuration Example**: `config.example.json` showing configuration possibilities for future versions
- **Setup Scripts**: Automated setup scripts for Windows (`setup.bat`) and Unix systems (`setup.sh`)
- **Enhanced Logging**: More detailed log messages for debugging and monitoring
- **Real-time Status Messages**: Immediate feedback when changing filters and adjustments
- **Help Command**: Press **h** to display keyboard controls in-app
- **Better Error Handling**: Comprehensive error messages for common issues
- **Output Directory Creation**: Automatically creates output directories if they don't exist
- **Comprehensive Examples**: Expanded `EXAMPLES.md` with 20+ real-world usage scenarios
- **System Requirements**: Detailed system requirements and performance tips in README

### Improved
- **Brightness/Contrast Adjustment**: Fixed value clipping to prevent overflow (now properly clipped to 0-255 range)
- **Keyboard Feedback**: All filter and adjustment changes now display status messages
- **Documentation**: Significantly expanded README with troubleshooting, command-line arguments, and performance tips
- **Code Quality**: Better type hints with optional parameters clearly marked
- **Error Messages**: More user-friendly and descriptive error messages
- **Frame Handling**: Better frame rate control and timing
- **Video Writer Validation**: Checks if writer is still open before writing frames

### Changed
- **Frame Resizing Logic**: Frames are now properly resized before processing for correct dimensions
- **Status Messages**: More informative feedback for user actions
- **Main Function**: Better argument parsing and validation

### Fixed
- **Value Clipping**: Brightness/contrast adjustments now properly clip to valid range
- **Output Path Validation**: Better handling of output paths without extensions
- **Resource Management**: Improved cleanup of video writer resources

## [2.0] - Previous Release

### Features
- Real-time video processing with 8 professional filters
- Live brightness and contrast adjustments
- Video file recording capabilities
- Snapshot capture functionality
- Professional HUD overlay with FPS monitoring
- Support for webcams and video files

### Known Issues
- Brightness/contrast could overflow in edge cases (fixed in 2.1)
- Limited error handling for some scenarios (improved in 2.1)
- No frame rate limiting option (added in 2.1)
- No performance optimization options (added in 2.1)

## Version History

| Version | Date | Status |
|---------|------|--------|
| 2.1 | 2024-05-29 | Current |
| 2.0 | Previous | Archived |
| 1.x | Early | Legacy |

## Future Roadmap

### Planned for Next Release
- Configuration file support (JSON/YAML)
- Custom filter chain creation
- Preset management system
- Real-time histogram display
- Color grading tools
- Frame interpolation for smooth slow-motion

### Possible Enhancements
- GPU acceleration with CUDA
- Real-time audio processing
- Multi-camera support
- Web interface for remote control
- Cloud recording integration
- Advanced color correction tools
