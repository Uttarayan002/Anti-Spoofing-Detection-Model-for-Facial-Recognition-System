from ultralytics import YOLO

# Initialize YOLO model with a pre-trained model
model = YOLO('yolov8n.pt')  # Use the same or similar model architecture

def main():
    # Train the model with the dataset and parameters consistent with previous success
    model.train(
        data='/home/rik/Documents/face_spoof_detection/dataset/splitdata/data.yaml',
        epochs=30,   # Previous successful epoch count
        lr0=0.01,    # Previous successful learning rate
        batch=16,    # Adjust batch size if needed
        imgsz=640,   # Ensure image size is suitable
        device='cpu' # Use CPU if no GPU is available
    )

if __name__ == '__main__':
    main()
