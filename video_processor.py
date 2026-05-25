"""GrayVideo Enhanced: Real-time video processing with professional filters and adjustments."""

import cv2
import argparse
import datetime
import os
import time
import numpy as np
import logging
from typing import Optional, Tuple
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
    def __init__(self, source: int | str = DEFAULT_SOURCE, output_path: Optional[str] = None) -> None:
        """Initialize VideoProcessor with source and optional output path.

        Args:
            source: Camera index (int) or path to video file (str). Defaults to 0 (webcam).
            output_path: Path to save recorded video. If None, no recording.

        Raises:
            RuntimeError: If video source cannot be opened.
        """
        self.source = source
        self.output_path = output_path
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

        # Create snapshots directory if it doesn't exist
        Path(self.snapshot_dir).mkdir(exist_ok=True)

        if not self.cap.isOpened():
            logger.error(f"Could not open video source: {source}")
            raise RuntimeError(f"Could not open video source: {source}")

        # Get video properties
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 20.0

        logger.info(f"Video source initialized: {self.width}x{self.height} @ {self.fps:.1f} FPS")

        if self.output_path:
            self._setup_writer()

    def _setup_writer(self) -> None:
        """Initialize video writer for recording processed frames.

        Saves in color format to allow filter switching during recording.
        """
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(self.output_path, fourcc, self.fps, (self.width, self.height))
        if not self.out.isOpened():
            logger.error(f"Failed to create video writer for: {self.output_path}")
            self.out = None
            return
        self.is_recording = True
        logger.info(f"Recording started: {self.output_path}")

    def apply_adjustments(self, frame: np.ndarray) -> np.ndarray:
        """Apply brightness and contrast adjustments to frame.

        Args:
            frame: Input frame array.

        Returns:
            Adjusted frame with brightness and contrast applied.
        """
        return cv2.convertScaleAbs(frame, alpha=self.contrast, beta=self.brightness)

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

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    if isinstance(self.source, str):
                        print("End of video file reached.")
                    else:
                        print("Error: Failed to read frame from camera.")
                    break

                frame_count += 1
                # Process frame
                processed_frame = self.apply_filter(frame)

                # Write to output if recording
                if self.out:
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
                elif key == ord('e'):
                    self.filter_mode = 'sepia'
                elif key == ord('k'):
                    self.filter_mode = 'sketch'
                elif key == ord('i'):
                    self.filter_mode = 'invert'
                elif key == ord('b'):
                    self.filter_mode = 'blur'
                elif key == ord('c'):
                    self.filter_mode = 'canny'
                elif key == ord('o'):
                    self.filter_mode = 'cartoon'
                elif key == ord('n'):
                    self.filter_mode = 'none'
                elif key == ord('['):
                    self.brightness = max(BRIGHTNESS_MIN, self.brightness - BRIGHTNESS_STEP)
                elif key == ord(']'):
                    self.brightness = min(BRIGHTNESS_MAX, self.brightness + BRIGHTNESS_STEP)
                elif key == ord('-'):
                    self.contrast = max(CONTRAST_MIN, self.contrast - CONTRAST_STEP)
                elif key == ord('='):
                    self.contrast = min(CONTRAST_MAX, self.contrast + CONTRAST_STEP)
                elif key == ord('r'):
                    self.reset_settings()

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

def main() -> None:\n    \"\"\"Main entry point for GrayVideo application.\"\"\"\n    parser = argparse.ArgumentParser(\n        description=\"GrayVideo Enhanced: Professional real-time video processing with filters\",\n        formatter_class=argparse.RawDescriptionHelpFormatter,\n        epilog=\"Examples:\\n\"\n               \"  python video_processor.py                    # Use webcam (camera 0)\\n\"\n               \"  python video_processor.py --source 1          # Use camera 1\\n\"\n               \"  python video_processor.py --source video.mp4  # Process video file\\n\"\n               \"  python video_processor.py --output output.avi # Record output\"\n    )\n    parser.add_argument(\n        \"--source\", type=str, default=\"0\",\n        help=\"Camera index (0, 1, etc.) or path to video file. Default: 0 (webcam)\"\n    )\n    parser.add_argument(\n        \"--output\", type=str,\n        help=\"Path to save processed video (e.g., output.avi)\"\n    )\n    \n    args = parser.parse_args()\n\n    # Determine if source is camera index or file path\n    source = args.source\n    if source.isdigit():\n        source = int(source)\n    elif not os.path.exists(source):\n        logger.error(f\"Video file '{source}' not found.\")\n        return\n\n    try:\n        processor = VideoProcessor(source=source, output_path=args.output)\n        processor.run()\n    except RuntimeError as e:\n        logger.error(f\"Error: {e}\")\n    except Exception as e:\n        logger.error(f\"Unexpected error: {e}\", exc_info=True)\n\n\nif __name__ == \"__main__\":\n    main()

