import cv2

# Open the default webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default webcam, change if using an external one (1, 2, etc.)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame was successfully captured
    if not ret:
        print("Failed to capture frame")
        break

    # Display the frame
    cv2.imshow('Frame', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close the window
cap.release()
cv2.destroyAllWindows()
