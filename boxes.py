# import cv2
# import numpy as np
# import pytesseract

# # Path to the Tesseract executable (only necessary on Windows)
# # Example: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # Load the image
# image_path = "Screenshot 2024-10-02 at 10.54.20 PM.png"
# image = cv2.imread(image_path)

# # Convert the image to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Apply thresholding to detect the text areas
# _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# # Find contours in the image
# contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Create a copy of the original image to draw on
# output_image = image.copy()

# # Sort contours top to bottom (to detect white spaces between text blocks)
# contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])

# # Loop through each contour and analyze whitespace
# for i, contour in enumerate(contours):
#     # Get the bounding box for each contour (text)
#     x, y, w, h = cv2.boundingRect(contour)
    
#     # Determine where to draw the box: above or below
#     # If it's not the last contour, check the space between the current and next text block
#     if i < len(contours) - 1:
#         next_x, next_y, next_w, next_h = cv2.boundingRect(contours[i + 1])
        
#         # Calculate the vertical space between this text block and the next one
#         space_between = next_y - (y + h)
        
#         if space_between > 10:  # We define "enough" white space as more than 10 pixels
#             # Draw a box in the white space below the text
#             cv2.rectangle(output_image, (x, y + h), (x + w, next_y), (255, 0, 0), 2)
#         else:
#             # If no space, draw a small box just under the text
#             cv2.rectangle(output_image, (x, y + h), (x + w, y + h + 20), (0, 0, 255), 2)
#     else:
#         # If it's the last contour, draw a box just below the last text block
#         cv2.rectangle(output_image, (x, y + h), (x + w, y + h + 20), (0, 0, 255), 2)

# # Save the output image
# output_image_path = "output_image_with_whitespace_boxes.png"
# cv2.imwrite(output_image_path, output_image)

# print(f"Processed image with whitespace boxes saved at {output_image_path}")


import cv2
import numpy as np
import pytesseract

# Use the correct path to the image
image_path = r"Screenshot 2024-10-02 at 10.54.20 PM.png"

# Load the image
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    print("Error: Could not open or find the image. Please check the file path.")
    exit()

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to detect the text areas
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Find contours in the image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a list of bounding boxes
boxes = [cv2.boundingRect(contour) for contour in contours]

# Function to merge overlapping boxes
def merge_boxes(boxes, min_width=20):
    merged_boxes = []
    while boxes:
        # Start with the first box
        current_box = boxes.pop(0)
        x, y, w, h = current_box

        # Ensure the box width is at least 20px
        if w < min_width:
            padding = (min_width - w) // 2
            x = max(0, x - padding)
            w = min_width

        merged = False
        for i, other_box in enumerate(boxes):
            ox, oy, ow, oh = other_box
            # Check if the boxes overlap or are close to each other (e.g., within 10px)
            if (x < ox + ow + 10 and x + w + 10 > ox and
                y < oy + oh + 10 and y + h + 10 > oy):
                # Merge the boxes by taking the minimum/maximum coordinates
                new_x = min(x, ox)
                new_y = min(y, oy)
                new_w = max(x + w, ox + ow) - new_x
                new_h = max(y + h, oy + oh) - new_y
                boxes[i] = (new_x, new_y, new_w, new_h)  # Update with the merged box
                merged = True
                break
        
        if not merged:
            merged_boxes.append((x, y, w, h))

    return merged_boxes

# Merge overlapping boxes
merged_boxes = merge_boxes(boxes)

# Draw the merged boxes on the original image
output_image = image.copy()
for (x, y, w, h) in merged_boxes:
    cv2.rectangle(output_image, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Save the output image with merged boxes
output_image_path = "/Users/shloakrathod/Desktop/Interaction Co/hard/output_image_with_merged_boxes.png"
cv2.imwrite(output_image_path, output_image)

print(f"Processed image with merged boxes saved at {output_image_path}")
