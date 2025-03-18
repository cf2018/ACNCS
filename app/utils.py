import cv2
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


def process_image(image_path):
    """
    Detects and labels the curved yellow lines in the sail image.
    """
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Error: Unable to load image at {image_path}")

    # Convert to HSV for better yellow color detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the range for yellow color in HSV space
    lower_yellow = np.array([20, 100, 100])  # Lower range of yellow
    upper_yellow = np.array([40, 255, 255])  # Upper range of yellow
    # Create a mask to extract yellow parts
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Apply morphological closing to fill gaps and connect small segments
    kernel = np.ones((5, 5), np.uint8)
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel)

    # Find contours from the yellow mask
    contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



    # Iterate through each contour
    for contour in contours:
        # Check if the contour has enough points to fit a polynomial
        if len(contour) >= 5:  # A minimum of 5 points for fitting
            # Get the x and y coordinates of the contour points
            contour_points = contour.reshape(-1, 2)  # Reshape to a 2D array for fitting
            x = contour_points[:, 0]
            y = contour_points[:, 1]

            # Fit a 3rd-degree polynomial (cubic) to the contour points
            # You can adjust this degree based on the complexity of the curve
            # Fit a cubic polynomial (degree 3)
            poly_coeff = np.polyfit(x, y, 3)
            poly_func = np.poly1d(poly_coeff)

            # Generate smooth fitted curve
            x_fit = np.linspace(min(x), max(x), 1000)
            y_fit = poly_func(x_fit)

            # Ensure values are within image bounds
            y_fit = np.clip(y_fit, 0, img.shape[0] - 1)
            x_fit = np.clip(x_fit, 0, img.shape[1] - 1)

            # Draw the fitted curve (red)
            for i in range(len(x_fit) - 1):
                cv2.line(img, (int(x_fit[i]), int(y_fit[i])),
                        (int(x_fit[i + 1]), int(y_fit[i + 1])), (0, 0, 255), 2)

            # Draw the green line (start to end)
            x1, y1 = x_fit[0], y_fit[0]
            x2, y2 = x_fit[-1], y_fit[-1]
            cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            # Compute the equation of the green line
            m = (y2 - y1) / (x2 - x1) if x2 != x1 else float('inf')  # Slope
            b = y1 - m * x1  # Intercept

            # Find the point on the red curve with max perpendicular distance from the green line
            max_dist = -1
            perpendicular_point = (0, 0)

            for i in range(len(x_fit)):
                x0, y0 = x_fit[i], y_fit[i]
                distance = abs(m * x0 - y0 + b) / np.sqrt(m**2 + 1)

                if distance > max_dist:
                    max_dist = distance
                    perpendicular_point = (x0, y0)

            # Find intersection point on the green line
            x_p, y_p = perpendicular_point
            if m == 0:  # If the green line is horizontal, intersection is just (x_p, y1)
                intersection_x, intersection_y = x_p, y1
            elif m == float('inf'):  # If the green line is vertical, intersection is (x1, y_p)
                intersection_x, intersection_y = x1, y_p
            else:
                # Slope of the perpendicular line is -1/m
                perp_m = -1 / m
                perp_b = y_p - perp_m * x_p  # y = mx + b, solving for b

                # Solve for intersection with y = mx + b of the green line
                intersection_x = (perp_b - b) / (m - perp_m)
                intersection_y = m * intersection_x + b

            # Draw the perpendicular blue line
            cv2.line(img, (int(x_p), int(y_p)), (int(intersection_x), int(intersection_y)), (255, 0, 0), 2)

            # === Calculate Percentages ===
            # Green line total length
            green_line_length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            # Distance along green line where the blue line intersects
            intersection_distance = np.sqrt((intersection_x - x1) ** 2 + (intersection_y - y1) ** 2)
            green_percentage = (intersection_distance / green_line_length) * 100

            # Length of blue perpendicular line
            blue_line_length = np.sqrt((x_p - intersection_x) ** 2 + (y_p - intersection_y) ** 2)

            # Compute total red curve length
            red_curve_length = sum(
                np.sqrt((x_fit[i + 1] - x_fit[i]) ** 2 + (y_fit[i + 1] - y_fit[i]) ** 2)
                for i in range(len(x_fit) - 1)
            )
            green_red_ratio = (blue_line_length / green_line_length) * 100

            # === Draw Text on the Right of the Blue Line ===
            text_x = int(max(intersection_x, x_p) + 20)  # Place text slightly to the right
            text_y = int((intersection_y + y_p) / 2)  # Centered along the blue line

            text1 = f"{green_percentage:.1f}% along green line"
            text2 = f"Blue/Green Length: {green_red_ratio:.1f}%"

            cv2.putText(img, text1, (text_x, text_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(img, text2, (text_x, text_y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

             

    # Save the processed image
    processed_image_path = image_path.replace('uploads', 'uploads/processed')
    cv2.imwrite(processed_image_path, img)

    # Return the path to the processed image
    return processed_image_path




