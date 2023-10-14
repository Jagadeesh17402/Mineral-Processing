import cv2
import numpy as np
import os
import streamlit as st

# Function 1: Smallest Circle that Encapsulates the Particle
def find_encapsulating_circle(input_image):
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(largest_contour)
        center = (int(x), int(y))
        radius = int(radius)
        result_image = input_image.copy()
        cv2.circle(result_image, center, radius, (0, 255, 0), 2)
        return result_image
    else:
        return input_image

# Function 2: Total Surface Area of the Particle
def calculate_surface_area(input_image):
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        particle_area = cv2.contourArea(largest_contour)
        result_image = input_image.copy()
        cv2.putText(result_image, f'Area: {int(particle_area)} pixels^2', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return result_image
    else:
        return input_image

# Function 3: Major Axis Inside the Particle
def find_major_axis(input_image):
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        ellipse = cv2.fitEllipse(largest_contour)
        major_axis_length = max(ellipse[1])
        minor_axis_length = min(ellipse[1])
        angle = ellipse[2]
        result_image = input_image.copy()
        center = (int(ellipse[0][0]), int(ellipse[0][1]))
        major_axis_endpoint1 = (
            int(center[0] + major_axis_length / 2 * np.cos(np.radians(angle))),
            int(center[1] + major_axis_length / 2 * np.sin(np.radians(angle)))
        )
        major_axis_endpoint2 = (
            int(center[0] - major_axis_length / 2 * np.cos(np.radians(angle))),
            int(center[1] - major_axis_length / 2 * np.sin(np.radians(angle)))
        )
        cv2.ellipse(result_image, center, (int(major_axis_length / 2), int(minor_axis_length / 2)), angle, 0, 360, (0, 255, 0), 2)
        cv2.line(result_image, major_axis_endpoint1, major_axis_endpoint2, (0, 255, 0), 2)
        return result_image
    else:
        return input_image

# Function 4: Total Perimeter of the Particle
def calculate_perimeter(input_image):
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        perimeter = cv2.arcLength(largest_contour, True)
        result_image = input_image.copy()
        cv2.drawContours(result_image, [largest_contour], -1, (0, 255, 0), 2)
        cv2.putText(result_image, f'Perimeter: {int(perimeter)} pixels', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return result_image
    else:
        return input_image

# Function 5: Centroid of the Particle
def find_centroid(input_image):
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        centroid_x = int(M['m10'] / M['m00'])
        centroid_y = int(M['m01'] / M['m00'])
        result_image = input_image.copy()
        cv2.circle(result_image, (centroid_x, centroid_y), 5, (0, 255, 0), -1)
        return result_image
    else:
        return input_image
    

# display_output.py 

# Function to process and display the image with all operations
def process_image(input_image):
    st.image(input_image, caption="Original Image", use_column_width=True)

    # Apply the five operations to the input image
    encapsulating_circle = find_encapsulating_circle(input_image)
    surface_area = calculate_surface_area(input_image)
    major_axis = find_major_axis(input_image)
    perimeter = calculate_perimeter(input_image)
    centroid = find_centroid(input_image)

    # Display the results
    st.image(encapsulating_circle, caption="Smallest Circle", use_column_width=True)
    st.image(surface_area, caption="Total Surface Area", use_column_width=True)
    st.image(major_axis, caption="Major Axis", use_column_width=True)
    st.image(perimeter, caption="Total Perimeter", use_column_width=True)
    st.image(centroid, caption="Centroid", use_column_width=True)

st.title("Mineral Processing Technology – Image Analytics")

# Add CSS styling for the project description
st.markdown(
    """
    <style>
        .project-description {
            background-color: #F0F0F0; /* Light gray background color */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            color: #333333; /* Dark gray text color */
        }
        .app-footer {
            text-align: right;
            margin-top: 10px;
            color: #555555; /* Gray text color in the footer */
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("<div class='project-description'>In the field of Mineral Processing Technology, size analysis of the various particles of an extracted sample is of importance in determining the quality of minerals, entropy values, and in establishing the degree of liberation of the values from the gangue at various particle sizes.</div>", unsafe_allow_html=True)

# Upload an image
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    input_image = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), cv2.IMREAD_COLOR)

    # Process the uploaded image
    process_image(input_image)

    # "Project by ROOP Shankar Voruganti" in the right bottom corner
    st.markdown(
        "<div style='position: fixed; bottom: 20px; right: 20px;'>Project by ROOP Shankar Voruganti</div>",
        unsafe_allow_html=True
    )

    if st.button("Process Another Image"):
        st.experimental_rerun()

# Clear previous output images
if "encapsulating_circle" in st.session_state:
    del st.session_state["encapsulating_circle"]
if "surface_area" in st.session_state:
    del st.session_state["surface_area"]
if "major_axis" in st.session_state:
    del st.session_state["major_axis"]
if "perimeter" in st.session_state:
    del st.session_state["perimeter"]
if "centroid" in st.session_state:
    del st.session_state["centroid"]