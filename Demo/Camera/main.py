import cv2
import os
import time

cap = cv2.VideoCapture(0)  # Change index if needed
image_path = "captured_image.jpg"  # Image file name

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Iriun Webcam", frame)

    # Capture and replace the image every 5 seconds
    time.sleep(5)  # Wait for 5 seconds

    # Delete the previous image if it exists
    if os.path.exists(image_path):
        os.remove(image_path)

    # Save the new image
    cv2.imwrite(image_path, frame)
    print(f"New image captured and saved as {image_path}")

    # Check for exit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
