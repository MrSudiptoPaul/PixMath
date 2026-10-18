# Image Processing & Steganography App

This project is a Streamlit-based web application that allows users to perform various arithmetic and bitwise operations on images, as well as securely hide secret text within an image. 

## ✨ Features

* **Interactive Interface**: Built using Streamlit, featuring a side navigation bar for easy operation selection.
* **Flexible Input Methods**: Upload existing images (`.png`, `.jpg`, `.jpeg`) or capture new photos directly using your device's camera.
* **Automatic Resizing**: When an operation requires two images (like AND, OR, XOR), the app automatically resizes the second image to perfectly match the dimensions of the first.
* **Session State Management**: Safely stores your uploaded images, operation values, and final processed results across interactions.

## 🛠️ Supported Operations

### Arithmetic & Logical Edits
* **Add / Subtract**: Brighten or darken your image by adding or subtracting a specific numeric value from the image's pixels.
* **NOT**: Inverts the image colors.
* **AND, OR, XOR**: Perform bitwise logical operations between two separate images.

### Steganography (Hide Password)
* **Text Hiding**: Enter a secret text or password to invisibly embed it inside an uploaded image.
* **LSB Technique**: The app converts your text to binary and stores it within the Least Significant Bits (LSB) of the image's pixels.
* **Secure Delimiter**: Automatically appends a `###` marker to the end of your secret text to ensure accurate reading later.
* **Decoding**: Easily extract and reveal the hidden text directly from the processed image using the "Decode Text from Image" button.

## 📂 Project Structure

* **`app.py`**: The main execution script that manages the two-column layout, displays the original and processed images, and handles the logic for executing operations and decoding text.
* **`ui.py`**: Manages the sidebar interface, handles the selection between file uploads and camera captures, and maintains the application's session state variables.
* **`operations.py`**: The core backend logic containing NumPy and Pillow (PIL) functions to manipulate pixel arrays, apply math/bitwise transformations, and handle the steganography encoding/decoding processes.
