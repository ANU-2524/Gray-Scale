import cv2
import argparse
import datetime

def main():
    """
    Main function to capture video from webcam, convert it to grayscale,
    and provide options to save frames or record the stream.
    """
    parser = argparse.ArgumentParser(description="GrayVedio: Real-time Grayscale Video Capture and Processing")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--output", type=str, help="Path to save the output video (e.g., output.avi)")
    
    args = parser.parse_args()

    # Initialize video capture
    cap = cv2.VideoCapture(args.camera)

    if not cap.isOpened():
        print(f"Error: Camera index {args.camera} is not accessible!")
        return

    # Video writer setup if output path is provided
    out = None
    if args.output:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # Get frame dimensions
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(args.output, fourcc, 20.0, (width, height), isColor=False)
        print(f"Recording video to: {args.output}")

    print("\n--- GrayVedio Controls ---")
    print("  's' : Save current frame as image")
    print("  'q' : Quit application")
    print("---------------------------\n")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame from camera!")
                break

            # Convert to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Write frame to video if recording
            if out:
                out.write(gray_frame)

            # Add instruction overlay (optional, but nice)
            display_frame = gray_frame.copy()
            cv2.putText(display_frame, "Press 's' to Save, 'q' to Quit", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255), 2)

            # Display the resulting frame
            cv2.imshow("GrayVedio - Grayscale Stream", display_frame)

            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            
            if key == ord('s'):
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"capture_{timestamp}.png"
                cv2.imwrite(filename, gray_frame)
                print(f"[*] Frame saved: {filename}")

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        # Release everything when done
        cap.release()
        if out:
            out.release()
        cv2.destroyAllWindows()
        print("Done. Resources released.")

if __name__ == "__main__":
    main()
