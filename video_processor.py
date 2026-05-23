import cv2
import argparse
import datetime
import os
import time
import numpy as np

class VideoProcessor:
    def __init__(self, source=0, output_path=None):
        self.source = source
        self.output_path = output_path
        self.cap = cv2.VideoCapture(source)
        self.out = None
        self.filter_mode = 'none' # default filter changed to none for better start
        self.is_recording = False
        self.brightness = 0
        self.contrast = 1.0
        self.snapshot_dir = "snapshots"
        self.status_msg = ""
        self.status_timer = 0
        self.flash_frames = 0
        
        if not os.path.exists(self.snapshot_dir):
            os.makedirs(self.snapshot_dir)
        
        if not self.cap.isOpened():
            raise Exception(f"Error: Could not open video source {source}")

        # Get video properties
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 20.0

        if self.output_path:
            self._setup_writer()

    def _setup_writer(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # We save as color even if grayscale to allow switching filters during recording
        self.out = cv2.VideoWriter(self.output_path, fourcc, self.fps, (self.width, self.height))
        self.is_recording = True
        print(f"[*] Recording video to: {self.output_path}")

    def apply_adjustments(self, frame):
        return cv2.convertScaleAbs(frame, alpha=self.contrast, beta=self.brightness)

    def apply_filter(self, frame):
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
            gray, _ = cv2.pencilSketch(frame, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
        elif self.filter_mode == 'invert':
            return cv2.bitwise_not(frame)

        elif self.filter_mode == 'blur':
            return cv2.GaussianBlur(frame, (15, 15), 0)

        elif self.filter_mode == 'canny':
            edges = cv2.Canny(frame, 100, 200)
            return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        elif self.filter_mode == 'cartoon':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                        cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(frame, 9, 300, 300)
            cartoon = cv2.bitwise_and(color, color, mask=edges)
            return cartoon
        
        return frame # 'none' or original

    def run(self):
        print("\n--- GrayVideo Enhanced Controls ---")
        print("  'q' : Quit          | 's' : Save Frame")
        print("  'g' : Grayscale     | 'e' : Sepia")
        print("  'k' : Sketch        | 'i' : Invert")
        print("  'b' : Blur          | 'c' : Canny")
        print("  'o' : Cartoon       | 'n' : Normal (Reset Filter)")
        print("  '[' : Brightness -  | ']' : Brightness +")
        print("  '-' : Contrast -    | '=' : Contrast +")
        print("  'r' : Reset All Settings")
        print("-----------------------------------\n")

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
                cv2.rectangle(display_frame, (0, 0), (self.width, 45), (0, 0, 0), -1)
                cv2.line(display_frame, (0, 45), (self.width, 45), (0, 255, 0), 1)

                info_text = f"Filter: {self.filter_mode.capitalize()} | FPS: {int(fps)} | BR: {self.brightness} | CT: {self.contrast:.1f}"
                cv2.putText(display_frame, info_text, 
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
                
                if self.is_recording:
                    # Blinking recording indicator
                    if (frame_count // 10) % 2 == 0:
                        cv2.circle(display_frame, (self.width - 30, 25), 8, (0, 0, 255), -1)
                    cv2.putText(display_frame, "REC", (self.width - 80, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

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
                    self.brightness = max(-100, self.brightness - 5)
                elif key == ord(']'):
                    self.brightness = min(100, self.brightness + 5)
                elif key == ord('-'):
                    self.contrast = max(0.1, self.contrast - 0.1)
                elif key == ord('='):
                    self.contrast = min(3.0, self.contrast + 0.1)
                elif key == ord('r'):
                    self.brightness = 0
                    self.contrast = 1.0
                    self.filter_mode = 'none'

        finally:
            self.cleanup()

    def save_frame(self, frame):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.snapshot_dir, f"capture_{timestamp}.png")
        cv2.imwrite(filename, frame)
        self.status_msg = f"Saved: {os.path.basename(filename)}"
        self.status_timer = 40 # Show for 40 frames
        self.flash_frames = 4  # Flash for 4 frames
        print(f"[*] Frame saved: {filename}")

    def cleanup(self):
        self.cap.release()
        if self.out:
            self.out.release()
        cv2.destroyAllWindows()
        print("[*] Resources released. Goodbye!")

def main():
    parser = argparse.ArgumentParser(description="GrayVideo: Enhanced Real-time Video Processing")
    parser.add_argument("--source", type=str, default="0", 
                        help="Camera index (int) or path to video file (string). Default: 0")
    parser.add_argument("--output", type=str, 
                        help="Path to save the output video (e.g., output.avi)")
    
    args = parser.parse_args()

    # Determine if source is camera index or file path
    source = args.source
    if source.isdigit():
        source = int(source)
    elif not os.path.exists(source):
        print(f"Error: Video file '{source}' not found.")
        return

    try:
        processor = VideoProcessor(source=source, output_path=args.output)
        processor.run()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

