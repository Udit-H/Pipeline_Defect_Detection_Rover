import cv2
import numpy as np


# crack detection
def detect_cracks(image):
    # to read the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

    # to reduce noise, apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # canny edge detection
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

    # highlight crack
    kernel = np.ones((3, 3), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)
    eroded_edges = cv2.erode(dilated_edges, kernel, iterations=1)

    # finding contours to highlight cracks
    contours, _ = cv2.findContours(
        eroded_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    result = image.copy()
    total_area = image.shape[0] * image.shape[1]

    # getting the boxes for the contours
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:
            x, y, w, h = cv2.boundingRect(contour)

            # calulate the percentage of the crack
            crack_percentage = (area / total_area) * 100

            # draw box
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Put percentage above the box
            cv2.putText(
                result,
                f"{crack_percentage:.2f}%",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
            )
    # cv2.drawContours(result, contours, -1, (0, 0, 255), 2)  # Draw contours in red
    return result, contours  # Return both result and contours


# leak detection
def detect_leaks(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # Convert to HSV color space

    lower_bound = np.array([0, 0, 200])  # Define lower bound for leak detection
    upper_bound = np.array([180, 255, 255])  # Define upper bound for leak detection

    mask = cv2.inRange(hsv, lower_bound, upper_bound)  # Create a mask for leaks
    result = cv2.bitwise_and(
        image, image, mask=mask
    )  # Apply the mask to the original image

    return result, mask  # Return both result and mask


# calculate crack percentage
def calculate_crack_percentage(image, contours):
    total_area = image.shape[0] * image.shape[1]
    crack_area = 0
    for contour in contours:
        crack_area += cv2.contourArea(contour)
    crack_percentage = (crack_area / total_area) * 100
    return crack_percentage


# calculate leak percentage
def calculate_leak_percentage(mask):
    total_pixels = mask.size
    leak_pixels = cv2.countNonZero(mask)
    leak_percentage = (leak_pixels / total_pixels) * 100
    return leak_percentage


def apply_canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)  # Reduce noise
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)  # Apply Canny
    return edges


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)  # or use a video file
    cv2.namedWindow("Crack detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Crack detection", 800, 600)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        edges = apply_canny(frame)
        cracks, contours = detect_cracks(frame)  # Get contours for calculation
        leaks, mask = detect_leaks(frame)  # Get mask for calculation

        # Calculate percentages
        crack_percent = calculate_crack_percentage(frame, contours)
        leak_percent = calculate_leak_percentage(mask)

        # Add text tags on the frames
        cv2.putText(
            cracks,
            f"Crack %: {crack_percent:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )
        cv2.putText(
            leaks,
            f"Leak %: {leak_percent:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )

        overlay = frame.copy()
        # make the whole screen black like before but add red for edges
        overlay[edges == 0] = [0, 0, 0]

        # cv2.imshow("Canny Edges", edges)
        # cv2.imshow("Overlay Edges", overlay)
        # cv2.imshow("Leak detections", leaks)
        cv2.imshow("Crack detection", cracks)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
