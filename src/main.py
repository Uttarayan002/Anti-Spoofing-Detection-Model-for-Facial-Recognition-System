import tkinter as tk
from tkinter import simpledialog, messagebox, Canvas
from PIL import Image, ImageTk
import subprocess
import sys
import os
import cv2
import face_recognition

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Initialize video source and capture
        self.video_source = 0
        self.vid = VideoCapture(self.video_source)

        # Create a canvas for video display
        self.canvas = Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Create control buttons
        self.btn_login = tk.Button(window, text="Login", width=10, command=self.login)
        self.btn_login.pack(side=tk.LEFT)
        self.btn_exit = tk.Button(window, text="Exit", width=10, command=self.exit)
        self.btn_exit.pack(side=tk.LEFT)

        # Register User button
        self.btn_register = tk.Button(window, text="Register User", width=15, command=self.register_user)
        self.btn_register.pack(side=tk.TOP, pady=10)

        # Set update delay
        self.delay = 15
        self.update()

        self.window.mainloop()

    def login(self):
        """Start login process."""
        # Delete tmp folder if exists
        self.delete_tmp_folder()

        # Take snapshot when Login button is clicked
        self.take_snapshot()

        # Compare the snapshot with stored user image
        if self.compare_images():
            # Show user ID and name in the YOLO detection GUI (spoof.py)
            subprocess.Popen([sys.executable, "spoof.py", self.current_id, self.current_user])

            # Save user ID and name in present_student.txt
            self.save_present_student()

            # Close the main.py interface
            self.window.quit()
            self.window.destroy()

            # Recreate tmp folder
            self.create_tmp_folder()

    def delete_tmp_folder(self):
        """Delete the tmp folder and its contents if it exists."""
        folder_path = 'tmp'
        if os.path.exists(folder_path):
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Reason: {e}")
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    try:
                        os.rmdir(dir_path)
                    except Exception as e:
                        print(f"Failed to delete {dir_path}. Reason: {e}")
            try:
                os.rmdir(folder_path)
            except Exception as e:
                print(f"Failed to delete {folder_path}. Reason: {e}")

    def create_tmp_folder(self):
        """Create tmp folder if it doesn't exist."""
        folder_path = 'tmp'
        os.makedirs(folder_path, exist_ok=True)

    def register_user(self):
        """Handle user registration."""
        user_id = simpledialog.askstring("Register User", "Enter User ID:")
        if user_id:
            user_name = simpledialog.askstring("Register User", "Enter User Name:")
            if user_name:
                # Take snapshot and check if the user already exists
                self.take_snapshot()
                if self.user_exists(user_id, user_name) or self.face_exists():
                    messagebox.showwarning("User Exists", "User with this ID, Name, or Face already exists.")
                else:
                    messagebox.showinfo("Snapshot", "Click OK to take a snapshot and save user details.")
                    self.take_snapshot(user_id, user_name)

    def user_exists(self, user_id, user_name):
        """Check if user ID or name already exists in the user_details folder."""
        folder_path = 'user_details'
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.startswith(f"{user_id}_") or file.split("_")[1].split(".")[0] == user_name:
                    return True
        return False

    def face_exists(self):
        """Check if face in the current snapshot already exists in the user_details folder."""
        tmp_image_path = 'tmp/tmp.jpg'
        tmp_image = face_recognition.load_image_file(tmp_image_path)
        tmp_encoding = face_recognition.face_encodings(tmp_image)

        if not tmp_encoding:
            print("No face found in tmp.jpg.")
            return False

        user_details_folder = 'user_details'
        if not os.path.exists(user_details_folder):
            print(f"No user images found in {user_details_folder}.")
            return False

        for file in os.listdir(user_details_folder):
            if file.endswith(".jpg") or file.endswith(".png"):
                user_image_path = os.path.join(user_details_folder, file)
                user_image = face_recognition.load_image_file(user_image_path)
                user_encoding = face_recognition.face_encodings(user_image)

                if not user_encoding:
                    print(f"No face found in {file}. Skipping.")
                    continue

                # Compare face encodings
                result = face_recognition.compare_faces([tmp_encoding[0]], user_encoding[0])

                if result[0]:
                    print(f"Face match found: {file}")
                    return True

        return False

    def take_snapshot(self, user_id=None, user_name=None):
        """Capture a snapshot of the current video feed and save details."""
        ret, frame = self.vid.get_frame()

        if ret:
            # Create folder if it doesn't exist
            folder_path = 'tmp'
            os.makedirs(folder_path, exist_ok=True)

            # Save snapshot image as tmp.jpg
            snapshot_file = os.path.join(folder_path, 'tmp.jpg')
            cv2.imwrite(snapshot_file, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

            # Save user details to a text file if provided
            if user_id and user_name:
                details_folder = 'user_details'
                os.makedirs(details_folder, exist_ok=True)
                
                # Save image with user_id_user_name.jpg format
                user_image_file = os.path.join(details_folder, f"{user_id}_{user_name}.jpg")
                cv2.imwrite(user_image_file, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def compare_images(self):
        """Compare tmp.jpg with the stored user images."""
        tmp_image_path = 'tmp/tmp.jpg'
        tmp_image = face_recognition.load_image_file(tmp_image_path)
        tmp_encoding = face_recognition.face_encodings(tmp_image)

        if not tmp_encoding:
            print("No face found in tmp.jpg.")
            return False

        user_details_folder = 'user_details'
        if not os.path.exists(user_details_folder):
            print(f"No user images found in {user_details_folder}.")
            return False

        match_found = False
        for file in os.listdir(user_details_folder):
            if file.endswith(".jpg") or file.endswith(".png"):
                user_image_path = os.path.join(user_details_folder, file)
                user_image = face_recognition.load_image_file(user_image_path)
                user_encoding = face_recognition.face_encodings(user_image)

                if not user_encoding:
                    print(f"No face found in {file}. Skipping.")
                    continue

                # Compare face encodings
                result = face_recognition.compare_faces([tmp_encoding[0]], user_encoding[0])

                if result[0]:
                    print(f"Match found: {file}")
                    match_found = True

                    # Extract ID and username from the matched filename
                    self.current_id, self.current_user = self.extract_id_and_user(file)
                    print(f"ID: {self.current_id}, User: {self.current_user}")
                    break

        if not match_found:
            print("No match found.")
            messagebox.showerror("Error", "No match found.")
            return False

        return True

    def extract_id_and_user(self, filename):
        """Extract ID and username from the filename."""
        parts = filename.split("_")
        if len(parts) == 2:
            id, user = parts[0], parts[1].split(".")[0]
            return id, user
        else:
            return None, None

    def save_present_student(self):
        """Save current student's ID and name in present_student.txt."""
        if self.current_id and self.current_user:
            filename = 'present_student.txt'
            with open(filename, 'w') as f:
                f.write(f"ID: {self.current_id}\n")
                f.write(f"Name: {self.current_user}\n")

    def update(self):
        """Update the video frame and detection."""
        ret, frame = self.vid.get_frame()
        if ret:
            # Display the frame in the canvas
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Schedule the next update
        self.window.after(self.delay, self.update)

    def exit(self):
        """Exit the application."""
        self.window.quit()
        self.vid.__del__()

class VideoCapture:
    def __init__(self, video_source=0):
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

# Run the application
if __name__ == "__main__":
    App(tk.Tk(), "Tkinter YOLO Detection")

