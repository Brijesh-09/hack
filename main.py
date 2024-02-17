from flask import Flask, render_template, jsonify
import cv2

app = Flask(__name__)

# Function to capture image from webcam
def capture_image():
    # Open the first webcam
    cap = cv2.VideoCapture(0)
    
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Couldn't open the webcam")
        return None
    
    # Capture a frame
    ret, frame = cap.read()
    
    # Release the webcam
    cap.release()
    
    if not ret:
        print("Error: Couldn't capture a frame")
        return None
    
    return frame

# Function to check if a user is present in the image
def is_user_present(image):
    # Check if the image is None
    if image is None:
        return False
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Compute the absolute difference between the current frame and the next frame
    next_frame = capture_image()
    if next_frame is None:
        return False
    next_gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
    next_blurred = cv2.GaussianBlur(next_gray, (5, 5), 0)
    frame_diff = cv2.absdiff(blurred, next_blurred)
    
    # Apply a threshold to the difference image
    _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
    
    # Count the number of non-zero pixels in the thresholded image
    non_zero_pixels = cv2.countNonZero(thresh)
    
    # If the number of non-zero pixels exceeds a certain threshold, consider a user present
    if non_zero_pixels > 1000:
        return True
    else:
        return False

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to get user status
@app.route('/user_status')
def get_user_status():
    # Check if the user is present and return the status
    status = "User is online" if is_user_present(capture_image()) else "User is offline"
    return jsonify({'status': status})

if __name__ == "__main__":
    app.run(debug=True)
