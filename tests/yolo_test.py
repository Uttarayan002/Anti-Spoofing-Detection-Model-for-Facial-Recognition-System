from ultralytics import YOLO
import cv2
import cvzone
import time

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Load the YOLO model
model = YOLO("../models/yolov8n.pt")

# Define class names
class_names = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
               "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
               "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
               "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball",
               "baseball glove", "skateboard", "surfboard", "tennis board", "bottle", "wine glass", "cup",
               "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
               "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "potted plant", "bed",
               "dining table", "toilet", "tv monitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
               "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
               "teddy bear", "hair dryer", "toothbrush"]

# Initialize frame timing
prev_frame_time = 0

while True:
    new_frame_time = time.time()  # Get current time
    success, img = cap.read()  # Read frame from webcam
    if not success:
        print("Failed to capture image from webcam.")
        break

    results = model(img,stream=True,verbose=False)  # Perform YOLO detection

    for result in results:
        # Iterate over detections
        for box in result.boxes:
            # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1

            # Draw rectangle on the image
            cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2)

            # Convert confidence score to float and round
            conf = float(box.conf[0])
            conf = round(conf, 2)
            
            # Get class id
            cls = int(box.cls[0])

            # Put class name and confidence on the image
            cvzone.putTextRect(img, f'{class_names[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

    # Calculate and display FPS
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    print(f'FPS: {fps:.2f}')

    # Display the resulting frame
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on pressing 'q'
        break

# Release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()

