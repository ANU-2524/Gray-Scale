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
        self.filter_mode = 'grayscale' # default filter
        self.is_recording = False
        
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

    def apply_filter(self, frame):
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
        
        return frame # 'none' or original

    def run(self):
        print("\n--- GrayVideo Enhanced Controls ---")
        print("  'q' : Quit")
        print("  's' : Save current frame")
        print("  'g' : Grayscale mode (default)")
        print("  'e' : Sepia mode")
        print("  'k' : Sketch mode")
        print("  'i' : Invert mode")
        print("  'n' : Normal mode")
        print("-----------------------------------\n")

        prev_time = 0
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    if isinstance(self.source, str):
                        print("End of video file reached.")
                    else:
                        print("Error: Failed to read frame from camera.")
                    break

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

                cv2.putText(display_frame, f"Filter: {self.filter_mode.capitalize()} | FPS: {int(fps)}", 
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                if self.is_recording:
                    cv2.circle(display_frame, (self.width - 30, 30), 10, (0, 0, 255), -1)

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
                elif key == ord('n'):
                    self.filter_mode = 'none'

        finally:
            self.cleanup()

    def save_frame(self, frame):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.png"
        cv2.imwrite(filename, frame)
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

