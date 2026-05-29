"""GrayVideo Enhanced: Real-time video processing with professional filters and adjustments."""

import cv2
import argparse
import datetime
import os
import time
import numpy as np
import logging
import json
from typing import Optional, Tuple, Dict, Any
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration Constants
DEFAULT_SOURCE = 0
DEFAULT_FILTER = 'none'
SNAPSHOT_DIR = "snapshots"
VIDEO_FORMAT = 'mp4'  # 'avi' or 'mp4'
FPS_DISPLAY_DECIMALS = 0
BRIGHTNESS_STEP = 5
BRIGHTNESS_MIN = -100
BRIGHTNESS_MAX = 100
CONTRAST_STEP = 0.1
CONTRAST_MIN = 0.1
CONTRAST_MAX = 3.0
STATUS_MSG_DURATION = 40  # frames
FLASH_FRAMES = 4
SKETCH_SIGMA_S = 60
SKETCH_SIGMA_R = 0.07
SKETCH_SHADE_FACTOR = 0.05
BLUR_KERNEL = (15, 15)
CARTOON_MEDIAN_BLUR = 5
CARTOON_BILATERAL_D = 9
CARTOON_BILATERAL_SIGMA_COLOR = 300
CARTOON_BILATERAL_SIGMA_SPACE = 300
CANNY_THRESHOLD1 = 100
CANNY_THRESHOLD2 = 200
CARTOON_ADAPTIVE_THRESH_BLOCKSIZE = 9
HUD_HEIGHT = 45
HUD_COLOR = (0, 255, 0)  # Green
RECORDING_COLOR = (0, 0, 255)  # Red
RECORDING_INDICATOR_RADIUS = 8
RECORDING_INDICATOR_X_OFFSET = 30
RECORDING_INDICATOR_Y = 25


class VideoProcessor:
    """Real-time video processor with professional filters and live adjustments."""
    def __init__(self, source: int | str = DEFAULT_SOURCE, output_path: Optional[str] = None,
                 target_fps: Optional[int] = None, resize_scale: float = 1.0) -> None:
        """Initialize VideoProcessor with source and optional output path.

        Args:
            source: Camera index (int) or path to video file (str). Defaults to 0 (webcam).
            output_path: Path to save recorded video. If None, no recording.
            target_fps: Target FPS for limiting frame rate. If None, no limit.
            resize_scale: Scale factor for frame resizing (0.5 = half size, 2.0 = double). Default: 1.0.

        Raises:
            RuntimeError: If video source cannot be opened.
            ValueError: If resize_scale is invalid.
        """
        if resize_scale <= 0 or resize_scale > 3.0:
            raise ValueError("resize_scale must be between 0 (exclusive) and 3.0")

        self.source = source
        self.output_path = output_path
        self.target_fps = target_fps
        self.resize_scale = resize_scale
        self.cap = cv2.VideoCapture(source)
        self.out = None
        self.filter_mode = DEFAULT_FILTER
        self.is_recording = False
        self.brightness = 0
        self.contrast = 1.0
        self.snapshot_dir = SNAPSHOT_DIR
        self.status_msg = ""
        self.status_timer = 0
        self.flash_frames = 0
        self.frame_delay = 1.0 / target_fps if target_fps else 0

        # Create snapshots directory if it doesn't exist
        Path(self.snapshot_dir).mkdir(exist_ok=True)

        if not self.cap.isOpened():
            source_desc = f"camera {source}" if isinstance(source, int) else f"file '{source}'"
            logger.error(f"Could not open video source: {source_desc}")
            raise RuntimeError(f"Could not open video source: {source_desc}. "
                             "Please verify the camera is connected or the file path is correct.")

        # Get video properties
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 20.0

        # Apply resize scale
        if resize_scale != 1.0:
            self.width = int(self.width * resize_scale)
            self.height = int(self.height * resize_scale)
            logger.info(f"Frame resizing enabled: {resize_scale}x -> {self.width}x{self.height}")

        logger.info(f"Video source initialized: {self.width}x{self.height} @ {self.fps:.1f} FPS")
        if target_fps:
            logger.info(f"Frame rate limited to {target_fps} FPS")

        if self.output_path:
            self._setup_writer()

    def _setup_writer(self) -> None:
        """Initialize video writer for recording processed frames.

        Saves in color format to allow filter switching during recording.

        Raises:
            IOError: If output directory doesn't exist or can't be created.
        """
        # Ensure output directory exists
        output_dir = os.path.dirname(os.path.abspath(self.output_path))
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except OSError as e:
                logger.error(f"Could not create output directory: {output_dir}")
                raise IOError(f"Cannot create output directory: {output_dir}") from e

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(self.output_path, fourcc, self.fps, (self.width, self.height))
        if not self.out.isOpened():
            logger.error(f"Failed to create video writer for: {self.output_path}")
            self.out = None
            raise IOError(f"Failed to create video writer. Check if the path is valid and you have write permissions.")
        self.is_recording = True
        logger.info(f"Recording started: {self.output_path}")

    def apply_adjustments(self, frame: np.ndarray) -> np.ndarray:
        """Apply brightness and contrast adjustments to frame.

        Args:
            frame: Input frame array.

        Returns:
            Adjusted frame with brightness and contrast applied, properly clipped to valid range.
        """
        # Apply contrast (alpha) and brightness (beta)
        adjusted = cv2.convertScaleAbs(frame, alpha=self.contrast, beta=self.brightness)
        # Ensure values stay within valid uint8 range
        adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
        return adjusted

    def apply_filter(self, frame: np.ndarray) -> np.ndarray:
        """Apply selected filter to frame.

        Args:
            frame: Input frame array.

        Returns:
            Processed frame with applied filter and adjustments.
        """
        frame = self.apply_adjustments(frame)

        if self.filter_mode == 'grayscale':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        elif self.filter_mode == 'sepia':
            kernel = np.array([[0.272, 0.534, 0.131],
                              [0.349, 0.686, 0.168],
                              [0.393, 0.769, 0.189]])
            sepia = cv2.transform(frame, kernel)
            sepia = np.clip(sepia, 0, 255)
            return sepia.astype(np.uint8)

        elif self.filter_mode == 'sketch':
            gray, _ = cv2.pencilSketch(frame, sigma_s=SKETCH_SIGMA_S, sigma_r=SKETCH_SIGMA_R,
                                       shade_factor=SKETCH_SHADE_FACTOR)
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        elif self.filter_mode == 'invert':
            return cv2.bitwise_not(frame)

        elif self.filter_mode == 'blur':
            return cv2.GaussianBlur(frame, BLUR_KERNEL, 0)

        elif self.filter_mode == 'canny':
            edges = cv2.Canny(frame, CANNY_THRESHOLD1, CANNY_THRESHOLD2)
            return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        elif self.filter_mode == 'cartoon':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, CARTOON_MEDIAN_BLUR)
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY, CARTOON_ADAPTIVE_THRESH_BLOCKSIZE,
                                        CARTOON_ADAPTIVE_THRESH_BLOCKSIZE)
            color = cv2.bilateralFilter(frame, CARTOON_BILATERAL_D, CARTOON_BILATERAL_SIGMA_COLOR,
                                       CARTOON_BILATERAL_SIGMA_SPACE)
            cartoon = cv2.bitwise_and(color, color, mask=edges)
            return cartoon

        return frame

    def _print_controls(self) -> None:
        """Print available keyboard controls to console."""
        print("\n" + "="*40)
        print("GrayVideo Enhanced - Keyboard Controls")
        print("="*40)
        print("Navigation:")
        print("  q: Quit application      | r: Reset all settings")
        print("\nFilters:")
        print("  n: Normal (no filter)    | g: Grayscale")
        print("  e: Sepia                 | k: Sketch")
        print("  i: Invert                | b: Blur")
        print("  c: Canny edge detection  | o: Cartoon")
        print("\nAdjustments:")
        print("  [/]: Brightness -/+      | -/=: Contrast -/+")
        print("\nCapture:")
        print("  s: Save frame snapshot")
        print("="*40 + "\n")

    def run(self) -> None:
        """Main loop for video processing and real-time filter application."""
        self._print_controls()

        prev_time = 0
        frame_count = 0
        last_frame_time = time.time()

        try:
            while True:
                # Frame rate limiting
                if self.target_fps:
                    elapsed = time.time() - last_frame_time
                    if elapsed < self.frame_delay:
                        time.sleep(self.frame_delay - elapsed)

                ret, frame = self.cap.read()
                if not ret:
                    if isinstance(self.source, str):
                        logger.info("End of video file reached.")
                    else:
                        logger.error("Failed to read frame from camera.")
                    break

                last_frame_time = time.time()
                frame_count += 1

                # Apply resize if needed
                if self.resize_scale != 1.0:
                    frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_LINEAR)

                # Process frame
                processed_frame = self.apply_filter(frame)

                # Write to output if recording
                if self.out and self.out.isOpened():
                    self.out.write(processed_frame)

                # UI Overlay
                display_frame = processed_frame.copy()

                # Calculate FPS
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
                prev_time = curr_time

                # HUD background
                cv2.rectangle(display_frame, (0, 0), (self.width, HUD_HEIGHT), (0, 0, 0), -1)
                cv2.line(display_frame, (0, HUD_HEIGHT), (self.width, HUD_HEIGHT), HUD_COLOR, 1)

                info_text = f"Filter: {self.filter_mode.capitalize()} | FPS: {int(fps)} | BR: {self.brightness} | CT: {self.contrast:.1f}"
                cv2.putText(display_frame, info_text,
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, HUD_COLOR, 1, cv2.LINE_AA)

                if self.is_recording:
                    # Blinking recording indicator
                    if (frame_count // 10) % 2 == 0:
                        cv2.circle(display_frame, (self.width - RECORDING_INDICATOR_X_OFFSET,
                                   RECORDING_INDICATOR_Y), RECORDING_INDICATOR_RADIUS, RECORDING_COLOR, -1)
                    cv2.putText(display_frame, "REC", (self.width - 80, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, RECORDING_COLOR, 2)

                # Status Message
                if self.status_timer > 0:
                    cv2.putText(display_frame, self.status_msg, (10, self.height - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
                    self.status_timer -= 1

                # Flash Effect
                if self.flash_frames > 0:
                    display_frame = cv2.addWeighted(display_frame, 0.5,
                                                  np.full(display_frame.shape, 255, dtype=np.uint8), 0.5, 0)
                    self.flash_frames -= 1

                cv2.imshow("GrayVideo - Enhanced Stream", display_frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    self.save_frame(processed_frame)
                elif key == ord('g'):
                    self.filter_mode = 'grayscale'
                    self.status_msg = "Grayscale filter"
                    self.status_timer = STATUS_MSG_DURATION
                elif key == ord('e'):
                    self.filter_mode = 'sepia'
                    self.status_msg = "Sepia filter"
                    self.status_timer = STATUS_MSG_DURATION
                elif key == ord('k'):
                    self.filter_mode = 'sketch'
                    self.status_msg = "Sketch filter"
                    self.status_timer = STATUS_MSG_DURATION
                elif key == ord('i'):
                    self.filter_mode = 'invert'
                    self.status_msg = "Invert filter"
                    self.status_timer = STATUS_MSG_DURATION
                elif key == ord('b'):
                    self.filter_mode = 'blur'
                    self.status_msg = "Blur filter"
                    self.status_timer = STATUS_MSG_DURATION
                elif key == ord('c'):
                    self.filter_mode = 'canny'
                    self.status_msg = "Canny edge detection"
                    self.status_timer = STATUS_MSG_DURATION
                elif key == ord('o'):
                    self.filter_mode = 'cartoon'
                    self.status_msg = "Cartoon filter"
                    self.status_timer = STATUS_MSG_DURATION
                elif key == ord('n'):
                    self.filter_mode = 'none'
                    self.status_msg = "Normal (no filter)"
                    self.status_timer = STATUS_MSG_DURATION
                elif key == ord('['):
                    self.brightness = max(BRIGHTNESS_MIN, self.brightness - BRIGHTNESS_STEP)
                    self.status_msg = f"Brightness: {self.brightness}"
                    self.status_timer = STATUS_MSG_DURATION
                elif key == ord(']'):
                    self.brightness = min(BRIGHTNESS_MAX, self.brightness + BRIGHTNESS_STEP)
                    self.status_msg = f"Brightness: {self.brightness}"
                    self.status_timer = STATUS_MSG_DURATION
                elif key == ord('-'):
                    self.contrast = max(CONTRAST_MIN, self.contrast - CONTRAST_STEP)
                    self.status_msg = f"Contrast: {self.contrast:.1f}"
                    self.status_timer = STATUS_MSG_DURATION
                elif key == ord('='):
                    self.contrast = min(CONTRAST_MAX, self.contrast + CONTRAST_STEP)
                    self.status_msg = f"Contrast: {self.contrast:.1f}"
                    self.status_timer = STATUS_MSG_DURATION
                elif key == ord('r'):
                    self.reset_settings()
                elif key == ord('h'):
                    self._print_controls()

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            self.cleanup()

    def reset_settings(self) -> None:
        """Reset brightness, contrast, and filter to defaults."""
        self.brightness = 0
        self.contrast = 1.0
        self.filter_mode = DEFAULT_FILTER
        self.status_msg = "Settings reset"
        self.status_timer = STATUS_MSG_DURATION

    def save_frame(self, frame: np.ndarray) -> None:
        """Save current frame as PNG snapshot.

        Args:
            frame: Frame to save.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.snapshot_dir, f"capture_{timestamp}.png")
        success = cv2.imwrite(filename, frame)
        if success:
            self.status_msg = f"Saved: {os.path.basename(filename)}"
            self.status_timer = STATUS_MSG_DURATION
            self.flash_frames = FLASH_FRAMES
            logger.info(f"Frame saved: {filename}")
        else:
            logger.error(f"Failed to save frame: {filename}")

    def cleanup(self) -> None:
        """Release all resources and close windows."""
        self.cap.release()
        if self.out:
            self.out.release()
        cv2.destroyAllWindows()
        logger.info("Resources released. Goodbye!")

def main() -> None:
    """Main entry point for GrayVideo application."""
    parser = argparse.ArgumentParser(
        description="GrayVideo Enhanced: Professional real-time video processing with filters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python video_processor.py                                    # Use webcam (camera 0)\n"
               "  python video_processor.py --source 1                         # Use camera 1\n"
               "  python video_processor.py --source video.mp4                 # Process video file\n"
               "  python video_processor.py --output output.avi                # Record output\n"
               "  python video_processor.py --fps 30 --scale 0.75              # Limit FPS and resize"
    )
    parser.add_argument(
        "--source", type=str, default="0",
        help="Camera index (0, 1, etc.) or path to video file. Default: 0 (webcam)"
    )
    parser.add_argument(
        "--output", type=str,
        help="Path to save processed video (e.g., output.avi)"
    )
    parser.add_argument(
        "--fps", type=int, default=None,
        help="Target FPS for frame rate limiting (e.g., 30). Default: unlimited"
    )
    parser.add_argument(
        "--scale", type=float, default=1.0,
        help="Frame resize scale factor (0.25-3.0). Default: 1.0 (no resize). "
             "Use 0.5 for half-size, 2.0 for double-size, etc."
    )

    args = parser.parse_args()

    # Determine if source is camera index or file path
    source = args.source
    if source.isdigit():
        source = int(source)
    elif not os.path.exists(source):
        logger.error(f"Video file '{source}' not found.")
        return

    # Validate FPS
    if args.fps is not None and args.fps <= 0:
        logger.error("FPS must be a positive number.")
        return

    # Validate and prepare output path
    output_path = args.output
    if output_path:
        # Ensure output has proper extension
        if not output_path.lower().endswith(('.avi', '.mp4')):
            output_path += '.avi'
            logger.warning(f"No file extension provided. Using: {output_path}")

    try:
        processor = VideoProcessor(
            source=source,
            output_path=output_path,
            target_fps=args.fps,
            resize_scale=args.scale
        )
        processor.run()
    except (RuntimeError, ValueError, IOError) as e:
        logger.error(f"Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)\n\n\nif __name__ == \"__main__\":\n    main()

