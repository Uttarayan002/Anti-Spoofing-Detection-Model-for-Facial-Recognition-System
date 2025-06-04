import tkinter as tk
from tkinter import Canvas, messagebox
from PIL import Image, ImageTk
import cv2
import time
from ultralytics import YOLO
import cvzone
import sys

# Confidence threshold for detection
confidence = 0.8
# Class names for detection
class_names = ["fake", "real"]

class App:
    def __init__(self, window, window_title, user_id, user_name):
        self.window = window
        self.window.title(window_title)

        self.user_id = user_id
        self.user_name = user_name

        # Initialize video source and capture
        self.video_source = 0
        self.vid = VideoCapture(self.video_source)

        # Create a canvas for video display
        self.canvas = Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Display user ID and name
        self.lbl_user_info = tk.Label(window, text=f"User ID: {self.user_id}, User Name: {self.user_name}", font=("Helvetica", 12))
        self.lbl_user_info.pack()

        # Load YOLO model
        self.model = YOLO("/home/rik/Documents/face_spoof_detection/runs/detect/train28/weights/best.pt")
        self.prev_frame_time = 0
        self.is_running = True  # Automatically start the video feed

        # Timer for tracking "fake" presence
        self.fake_start_time = None
        self.warning_displayed = False

        # Set update delay
        self.delay = 15
        self.update()

    def update(self):
        """Update the video frame and detection."""
        ret, frame = self.vid.get_frame()

        if ret:
            new_frame_time = time.time()
            results = self.model(frame, stream=True, verbose=False)
            fake_detected = False

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    w, h = x2 - x1, y2 - y1
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])

                    if conf > confidence:
                        if class_names[cls] == "fake":
                            color = (0, 0, 255)  # Red color for "fake"
                            fake_detected = True
                        else:
                            color = (0, 255, 0)  # Green color for "real"

                        # Draw bounding box and text
                        cvzone.cornerRect(frame, (x1, y1, w, h), l=9, rt=2, colorC=color, colorR=color)
                        cvzone.putTextRect(frame, f'{class_names[cls]}',
                                           (max(0, x1), max(35, y1)),
                                           scale=1, thickness=1,
                                           colorR=color, colorB=(0, 0, 0))

            if fake_detected:
                self.check_fake_duration(new_frame_time)
            else:
                self.fake_start_time = None
                self.warning_displayed = False

            fps = 1 / (new_frame_time - self.prev_frame_time)
            self.prev_frame_time = new_frame_time
            fps_text = f'FPS: {fps:.2f}'

            # Display the FPS on the frame
            cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Display the frame in the canvas
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Schedule the next update
        self.window.after(self.delay, self.update)

    def check_fake_duration(self, current_time):
        """Check if 'fake' object has been present for more than 30 seconds."""
        if self.fake_start_time is None:
            self.fake_start_time = current_time
        elif current_time - self.fake_start_time >= 5 and not self.warning_displayed:
            messagebox.showwarning("Warning", "WARNING: You are fake!!!")
            self.warning_displayed = True

    def exit(self):
        """Exit the application."""
        self.window.quit()
        self.vid.__del__()

class VideoCapture:
    def __init__(self, video_source=1):
        # Initialize video capture
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Set video frame width and height
        self.vid.set(3, 640)
        self.vid.set(4, 480)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        """Capture frame from the video source."""
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (False, None)

    def __del__(self):
        """Release the video source."""
        if self.vid.isOpened():
            self.vid.release()

# Run the application with user ID and name from main.py
if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Expected two arguments: user_id and user_name")

    user_id = sys.argv[1]
    user_name = sys.argv[2]
    
    root = tk.Tk()
    app = App(root, "Spoof Detection", user_id, user_name)
    root.mainloop()
