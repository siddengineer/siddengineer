import cv2
import numpy as np

# Load the image
image = cv2.imread('WhatsApp Image 2024-10-01 at 22.25.19_ce99807e.jpg')

# Resize the image for faster processing (optional)
image = cv2.resize(image, (800, 800))

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply edge detection (Canny)
edges = cv2.Canny(blurred, 50, 150)

# Find contours based on the edges detected
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Loop through contours and filter by area to detect empty ground spaces
for contour in contours:
    # Get the bounding box for each contour
    x, y, w, h = cv2.boundingRect(contour)
    
    # Define a size threshold to filter out small irrelevant contours
    if 100 < w < 300 and 100 < h < 300:  # Adjust these values to suit the empty ground spaces size
        # Draw rectangles around detected empty spaces
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Show the result with detected boxes (empty spaces)
cv2.imshow('Empty Space Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

