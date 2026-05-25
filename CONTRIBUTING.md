# Contributing to GrayVideo Enhanced

Thank you for your interest in contributing to GrayVideo Enhanced! This document provides guidelines and instructions for contributing to the project.

## Code Style

We follow PEP 8 guidelines with the following standards:

- **Type Hints**: All functions and methods must have type hints
- **Docstrings**: Use Google-style docstrings for all classes and methods
- **Constants**: Use UPPERCASE_NAMES for configuration constants
- **Logging**: Use the logging module instead of print statements
- **Line Length**: Keep lines to 100 characters or less

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
       return processed_frame
   ```

3. **Add Keyboard Shortcut** in `run()` method
   ```python
   elif key == ord('x'):  # Choose your key
       self.filter_mode = 'your_filter_name'
   ```

4. **Update Documentation**
   - Add to README.md keyboard controls table
   - Update filter list in Features section

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Testing Your Changes

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
