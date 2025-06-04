from cvzone.FaceDetectionModule import FaceDetector
import cv2
import cvzone
from time import time

################################################################
output_folder_path = 'dataset/data collect'  # Directory to save collected data
offset_percentage_w = 10  # Width offset percentage
offset_percentage_h = 20  # Height offset percentage
confidence = 0.8  # Confidence threshold for face detection
cam_width, cam_height = 640, 480  # Camera resolution
float_point = 6  # Decimal points for normalization
save = True  # Save detected faces
blur_threshould = 35  # Blurriness threshold
debug = False  # Debug mode flag
class_id = 0 # Class ID for labeling (0: fake, 1: real)
################################################################

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, cam_width)  # Width
cap.set(4, cam_height)  # Height

# Initialize the FaceDetector
detector = FaceDetector()

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image from webcam.")
        break

    img_out = img.copy()
    list_blur = []  # List to check if faces are blurry
    list_info = []  # List to store normalized values and class name

    # Detect faces in the image
    img, bboxs = detector.findFaces(img, draw=False)

    # Process detected faces
    if bboxs:
        for bbox in bboxs:
            x, y, w, h = bbox["bbox"]
            score = bbox["score"][0]
            print(x, y, w, h)

            if score > confidence:
                # Calculate the offsets
                offset_w = int((offset_percentage_w / 100.0) * w)
                offset_h = int((offset_percentage_h / 100.0) * h)

                # Adjust the bounding box
                x_adjusted = max(0, x - offset_w)
                y_adjusted = max(0, y - (offset_h * 3))
                w_adjusted = w + (2 * offset_w)
                h_adjusted = h + (3.5 * offset_h)

                # Ensure the adjusted width and height do not exceed the image boundaries
                w_adjusted = min(w_adjusted, img.shape[1] - x_adjusted)
                h_adjusted = min(h_adjusted, img.shape[0] - y_adjusted)

                # Find blurriness of the face
                img_face = img[y_adjusted:y_adjusted + int(h_adjusted), x_adjusted:x_adjusted + int(w_adjusted)]
                cv2.imshow("Face", img_face)
                blur_value = int(cv2.Laplacian(img_face, cv2.CV_64F).var())
                if blur_value > blur_threshould:
                    list_blur.append(True)
                else:
                    list_blur.append(False)

                # Normalize values for label file
                ih, iw, _ = img.shape
                xc, yc = (x + (w / 2)), (y + (h / 2))
                xcn, ycn = round((xc / iw), float_point), round((yc / ih), float_point)
                wn, hn = round(w / iw, float_point), round(h / ih, float_point)
                print(xcn, ycn, wn, hn)

                list_info.append(f"{class_id} {xcn} {ycn} {wn} {hn}\n")

                # Draw bounding box and text
                cv2.rectangle(img_out, (x_adjusted, y_adjusted), (x_adjusted + int(w_adjusted), y_adjusted + int(h_adjusted)), (255, 0, 0), 3)
                cvzone.putTextRect(img_out, f'Score: {int(score * 100)}% Blur: {blur_value}', (x_adjusted, y_adjusted - 20), scale=2, thickness=4)

                if debug:
                    cv2.rectangle(img, (x_adjusted, y_adjusted), (x_adjusted + int(w_adjusted), y_adjusted + int(h_adjusted)), (255, 0, 0), 3)
                    cvzone.putTextRect(img, f'Score: {int(score * 100)}% Blur: {blur_value}', (x_adjusted, y_adjusted - 20), scale=2, thickness=4)

        # Save image if all faces are not blurry
        if save:
            if all(list_blur) and list_blur != []:
                time_now = time()
                time_now = str(time_now).split('.')
                time_now = time_now[0] + time_now[1]
                cv2.imwrite(f"{output_folder_path}/{time_now}.jpg", img)

                # Save label file
                for info in list_info:
                    f = open(f"{output_folder_path}/{time_now}.txt", 'a')
                    f.write(info)
                    f.close()

    # Display the resulting image
    cv2.imshow("Image", img_out)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
