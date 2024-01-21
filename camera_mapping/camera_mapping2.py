import cv2
import numpy as np

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for the first green range in HSV
    lower_green = np.array([30, 50, 60])
    upper_green = np.array([80, 255, 255])

    # Create a mask for the first green color using color-based segmentation
    mask_color1 = cv2.inRange(hsv, lower_green, upper_green)

    # Define lower and upper bounds for the second green-blue range in HSV
    lower_green_blue = np.array([80, 80, 100])
    upper_green_blue = np.array([150, 255, 255])

    # Create a mask for the second green-blue color using color-based segmentation
    mask_color2 = cv2.inRange(hsv, lower_green_blue, upper_green_blue)

    # Combine both masks for green and green-blue colors
    combined_mask = cv2.bitwise_or(mask_color1, mask_color2)

    # Convert frame to grayscale for adaptive thresholding
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to the grayscale image
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Combine adaptive thresholding and color-based segmentation masks
    combined_mask = cv2.bitwise_and(adaptive_thresh, combined_mask)

    # Apply the combined mask to the original frame to extract the green and green-blue objects
    extracted_object = cv2.bitwise_and(frame, frame, mask=combined_mask)

    # Display the extracted object
    cv2.imshow('Extracted Green and Green-Blue Objects', extracted_object)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
