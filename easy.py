
from pathlib import Path
import fitz
import math

def data_entry_data():
    return  {
    '0': '1HGCM82633A123456',
    '1': 2023,
    '2': 'Toyota',
    '3': '7ABC123',
    '4': 'N/A',
    '5': 'John Doe',
    '6': 'Jane Smith',
    '7': '10',
    '8': '01',
    '9': '2',
    '10': '0',
    '11': '2',
    '12': '4',
    '13': '15000',
    '14': 'None',
    '15': '0',
    '16': 'John Doe',
    '17': '10/02/2024',
    '18': '34521',
    '19': 'Shloak Rat',
    '20': '10/02/2024',
    '21': '34522',
    '22': '456 Oak Ave',
    '23': 'San Francisco',
    '24': 'CA',
    '25': '94102',
    '26': '123-456-7890',
    '27': 'Janet Singh',
    '28': '',
    '29': '123 Main St',
    '30': 'Los Angeles',
    '31': 'CA',
    '32': '90001',
}

# Helper function to compute the center of a rectangle
def rect_center(rect):
    x_center = (rect.x0 + rect.x1) / 2
    y_center = (rect.y0 + rect.y1) / 2
    return (x_center, y_center)

# Helper function to compute the Euclidean distance between two points
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Main logic to update the PDF with the closest signature images
data_entry_data = data_entry_data()

with fitz.open('easy-pdf.pdf') as doc:
    target_page = doc[0]

    font_rgb = (0, 137, 210)
    font_color = tuple(value / 255 for value in font_rgb)

    # Image paths for John and Jane
    john_image_path = "signature.png"
    shloak_image_path = "john.png"
    
    # Offset for image placement
    offset_x = 20  
    offset_y = 0 
    
    # Loop through and update form fields
    for indx, field in enumerate(target_page.widgets()):
        if field.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
            field.field_value = str(data_entry_data.get(str(indx), ''))
            field.update()

        if indx == 32:
            break
    #Get the locations of the signature, John Doe, and Jane Smith
    signature_locations = target_page.search_for("SIGNATURE")
    john_locations = target_page.search_for("John Doe")
    shloak_locations = target_page.search_for("Jane Smith")

    min_distance_john = float('inf')
    closest_signature_john = None

    for john_rect in john_locations:
        for signature_rect in signature_locations:
            distance = euclidean_distance(rect_center(john_rect), rect_center(signature_rect))
            if distance < min_distance_john:
                min_distance_john = distance
                closest_signature_john = signature_rect

    if closest_signature_john:
        x0, y0, x1, y1 = closest_signature_john
        img_x0 = x1 + offset_x  
        img_y0 = y1 + offset_y  
        width, height = 100, 20  
        rect = fitz.Rect(img_x0, img_y0, img_x0 + width, img_y0 + height)
        target_page.insert_image(rect, filename=john_image_path)

    min_distance_shloak = float('inf')
    closest_signature_shloak = None

    for shloak_rect in shloak_locations:
        for signature_rect in signature_locations:
            distance = euclidean_distance(rect_center(shloak_rect), rect_center(signature_rect))
            if distance < min_distance_shloak:
                min_distance_shloak = distance
                closest_signature_shloak = signature_rect

    if closest_signature_shloak:
        x0, y0, x1, y1 = closest_signature_shloak
        img_x0 = x1 + offset_x  
        img_y0 = y1 + offset_y  
        width, height = 100, 20  
        rect = fitz.Rect(img_x0, img_y0, img_x0 + width, img_y0 + height)
        target_page.insert_image(rect, filename=shloak_image_path)

    doc.save('output_with_john_and_shloak_signaturesssss.pdf')
