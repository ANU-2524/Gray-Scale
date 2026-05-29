# Contributing to GrayVideo Enhanced

Thank you for your interest in contributing to GrayVideo Enhanced! This document provides guidelines and instructions for contributing to the project.

## Code Style

We follow PEP 8 guidelines with the following standards:

- **Type Hints**: All functions and methods must have type hints
- **Docstrings**: Use Google-style docstrings for all classes and methods
- **Constants**: Use UPPERCASE_NAMES for configuration constants
- **Logging**: Use the logging module instead of print statements (except in `_print_controls()`)
- **Line Length**: Keep lines to 100 characters or less
- **Naming**: Use descriptive variable names (e.g., `frame_count` not `fc`)

## Adding New Filters

To add a new filter:

1. **Add Configuration Constants** (if needed)
   ```python
   YOUR_FILTER_PARAM1 = value
   YOUR_FILTER_PARAM2 = value
   ```

2. **Implement the Filter** in `apply_filter()` method
   ```python
   elif self.filter_mode == 'your_filter_name':
       # Your filter implementation
       result = cv2.some_function(frame, YOUR_FILTER_PARAM1, YOUR_FILTER_PARAM2)
       return result
   ```

3. **Add Keyboard Shortcut** in `run()` method
   ```python
   elif key == ord('x'):  # Choose your key (avoid conflicts)
       self.filter_mode = 'your_filter_name'
       self.status_msg = "Your Filter Name"
       self.status_timer = STATUS_MSG_DURATION
   ```

4. **Update Documentation**
   - Add to README.md Filters section
   - Add to keyboard controls table with description
   - Add example in EXAMPLES.md

## Adding New Features

### For Performance Features (FPS Limiting, Resizing, etc.)
1. Add parameter to `__init__()` with type hints
2. Add validation in `__init__()`
3. Use the parameter in appropriate methods
4. Add command-line argument in `main()`
5. Update README.md with usage examples
6. Add entry to CHANGELOG.md under "Added"

### For UI Features
1. Add to HUD rendering in `run()` method
2. Add keyboard shortcut if applicable
3. Use existing HUD constants for styling
4. Update keyboard controls documentation

## Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate it:
   ```bash
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Testing Your Changes

### Basic Testing
1. Run the application with your changes: `python video_processor.py`
2. Test each keyboard shortcut related to your change
3. Test with both webcam and video file sources
4. Verify all filters work correctly

### Performance Testing
1. Test on different hardware if possible
2. Monitor CPU/memory usage with task manager
3. Test with `--fps` and `--scale` options if applicable

### Edge Cases to Test
- Very low/high brightness and contrast values
- Invalid file paths
- Multiple rapid filter changes
- Long recording sessions
- Different resolution cameras

## Commit Guidelines

When committing changes:

1. **Descriptive Messages**: Use clear, present-tense commit messages
   ```
   Good: "Add frame resizing feature with --scale option"
   Bad: "Fixed stuff" or "Update"
   ```

2. **Logical Commits**: Keep changes logically grouped
   - Don't mix unrelated features in one commit
   - Each commit should be independently reviewable

3. **Update Documentation**: Always update docs with your changes
   - README.md for user-facing features
   - CHANGELOG.md for significant changes
   - Code docstrings for implementation details

## Bug Reports

When reporting issues:

1. **Title**: Be specific about the problem
   ```
   Good: "Camera fails to initialize on index > 2"
   Bad: "Doesn't work"
   ```

2. **Description**: Include
   - What you were doing
   - What happened
   - What you expected to happen
   - Python version and OS

3. **Reproduction Steps**: Provide exact commands to reproduce
   ```bash
   python video_processor.py --source 1
   ```

## Feature Requests

1. **Explain the Use Case**: Why would this be useful?
2. **Provide Examples**: Show how it would work
3. **Consider Performance**: How would it impact existing features?

## Code Review Process

1. Ensure all tests pass
2. Code follows PEP 8 and project style
3. Documentation is updated
4. Commit messages are clear
5. Changes are logically organized

## Project Structure

```
GrayVedio/
├── video_processor.py      # Main application
├── requirements.txt         # Dependencies
├── README.md               # User documentation
├── QUICKSTART.md           # Quick start guide
├── EXAMPLES.md             # Usage examples
├── CONTRIBUTING.md         # This file
├── CHANGELOG.md            # Version history
├── config.example.json     # Configuration template
├── setup.bat              # Windows setup script
├── setup.sh               # Unix setup script
└── snapshots/             # Saved frames (auto-created)
```

## Performance Considerations

When adding features:

1. **Avoid Heavy Operations in Main Loop**: Can cause frame drops
2. **Use Efficient Algorithms**: Prefer OpenCV built-ins over custom loops
3. **Memory Management**: Don't accumulate data over time
4. **Test on Low-End Hardware**: Ensure it works on Raspberry Pi/old laptops

## Documentation Standards

### Docstrings
```python
def process_frame(self, frame: np.ndarray) -> np.ndarray:
    """Brief description of what the method does.

    More detailed explanation if needed. Describe parameters
    and behavior.

    Args:
        frame: Input video frame as numpy array.

    Returns:
        Processed frame as numpy array.

    Raises:
        ValueError: If frame is invalid.
    """
```

### Comments
- Explain WHY, not WHAT (code shows what)
- Keep comments up-to-date with code changes
- Remove commented-out code before committing

## Version Numbering

We use semantic versioning: MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

## Questions?

- Check existing issues and discussions
- Read through EXAMPLES.md for inspiration
- Look at similar implementations in video_processor.py

Thank you for contributing to make GrayVideo Enhanced better! 🎬

1. Test with webcam: `python video_processor.py`
2. Test with video file: `python video_processor.py --source test.mp4`
3. Test recording: `python video_processor.py --output test_output.avi`
4. Verify all keyboard shortcuts work correctly

## Submitting Changes

1. Create a descriptive commit message
2. Ensure your code follows PEP 8 and project conventions
3. Test thoroughly before submitting
4. Include documentation updates if applicable

## Reporting Issues

When reporting bugs, please include:
- Python version
- OpenCV version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Relevant error messages or logs

## Questions?

Feel free to open an issue for questions or suggestions about the project.

Happy coding!
