# AutoFill PDFs with an Agentic Approach

## Easy PDF 
Approach: iterate through the text boxes and fill info 
Signature: Calculate the Euclidian distance between "Signature" and the closest name to append the correct signature. 

## Hard PDF 
Approach:
- Detect contours using Canny Edge Detection
- Annotate boxes on vertical contour if 90% of the space in the box is white


## Scope for improvement: 
The current solution is not seamless and not PDF agnostic

