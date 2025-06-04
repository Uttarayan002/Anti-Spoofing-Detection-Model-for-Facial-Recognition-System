from cvzone.FaceDetectionModule import FaceDetector
import cv2

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Initialize the FaceDetector
detector = FaceDetector()

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image from webcam.")
        break

    # Detect faces in the image
    img, bboxs = detector.findFaces(img)

    # Draw a circle at the center of the first detected face
    if bboxs:
        center = bboxs[0]['center']
        cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

    # Display the resulting image
    cv2.imshow("Image", img)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
