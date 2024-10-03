# import cv2
# import numpy as np

# # Load the image
# image_path = "Screenshot 2024-10-02 at 10.54.20 PM.png"
# image = cv2.imread(image_path)

# # Convert to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Apply edge detection (Canny)
# edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# # Use HoughLinesP to detect lines
# lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

# # Create a copy of the original image to draw lines on
# image_with_horizontal_lines = image.copy()

# # Iterate through the detected lines and draw horizontal lines
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     # Check if the line is approximately horizontal
#     if abs(y2 - y1) < 10:  # Adjust the threshold for horizontality
#         cv2.line(image_with_horizontal_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)

# # Save the result
# output_path = "horizontal_lines_output.png"
# cv2.imwrite(output_path, image_with_horizontal_lines)

# # Display the result (optional, only for local environments)
# # cv2.imshow('Image with Horizontal Lines', image_with_horizontal_lines)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()

import cv2
import numpy as np

# Load the image
image_path = "Screenshot 2024-10-02 at 10.54.20 PM.png"
image = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply edge detection (Canny)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Use HoughLinesP to detect lines
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

# Create a copy of the original image to draw rectangles
image_with_rectangles = image.copy()

# Iterate through the detected lines and process horizontal lines
for line in lines:
    x1, y1, x2, y2 = line[0]
    # Check if the line is approximately horizontal
    if abs(y2 - y1) < 10:  # Horizontal line condition
        # Define the region 20 pixels above the line
        top_y = max(y1 - 20, 0)
        bottom_y = y1
        left_x = min(x1, x2)
        right_x = max(x1, x2)
        
        # Extract the region above the line
        region_above = gray[top_y:bottom_y, left_x:right_x]

        # Calculate the percentage of white pixels in the region
        white_pixel_count = np.sum(region_above >= 240)  # Pixels close to white
        total_pixel_count = region_above.size
        white_pixel_percentage = (white_pixel_count / total_pixel_count) * 100

        # If 90% or more of the pixels are white, draw a rectangle above the line
        if white_pixel_percentage >= 90:
            cv2.rectangle(image_with_rectangles, (left_x, top_y), (right_x, bottom_y), (0, 255, 0), 2)

# Save the result
output_path = "rectangles_output.png"
cv2.imwrite(output_path, image_with_rectangles)

# Display the result (optional, only for local environments)
# cv2.imshow('Image with Rectangles', image_with_rectangles)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
