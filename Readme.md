# Image Processing GUI Tool

A graphical user interface (GUI) for applying various image processing techniques using Python. This application uses OpenCV, NumPy, and Pillow to perform operations such as noise addition, noise removal, filtering, morphological transformations, and region-based operations on images.

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [Project Structure](#project-structure)
* [How It Works](#how-it-works)
* [Contributing](#contributing)
* [License](#license)

## Overview

The Image Processing GUI Tool is designed for users who want a quick and interactive way to apply a variety of image processing filters and operations without needing to write code. Built with Tkinter, the tool provides a responsive, user-friendly interface that allows users to load an image, apply different processing techniques, view the original and processed images side by side, and save the processed result.

## Features

* **Image Loading:** Browse and load images in common formats (JPG, JPEG, PNG, BMP, TIFF).
* **Noise Operations:**

  * **Add Noise:** Introduce random noise to an image.
  * **Gaussian Noise:** Add Gaussian (normal distribution) noise.
  * **Remove Noise:** Clean an image using Non-Local Means Denoising.
* **Filtering Techniques:**

  * **Mean Filter:** Reduce noise with a simple averaging filter.
  * **Median Filter:** Preserve edges while smoothing the image.
  * **Gaussian Filter:** Smooth images using Gaussian convolution.
* **Morphological Operations:**

  * **Erosion:** Remove small-scale details by eroding the image boundaries.
  * **Dilation:** Expand image boundaries, emphasizing features.
  * **Opening:** Erosion followed by dilation to remove noise.
  * **Closing:** Dilation followed by erosion to close small holes.
* **Advanced Operations:**

  * **Boundary Extraction:** Highlight object edges by extracting boundaries.
  * **Region Filling:** Fill holes within regions based on connectivity.
* **User Interface:**

  * Side-by-side display of the original and processed images.
  * Buttons for each processing function.
  * Options to undo changes, reset to the original image, and save the processed result.

## Prerequisites

To run the project, ensure you have Python installed (Python 3.6 or later recommended). The following Python libraries are required:

* **Tkinter** (usually comes built-in with Python)
* **OpenCV** (`opencv-python`)
* **NumPy**
* **Pillow**

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/image-processing-gui.git
   cd image-processing-gui
   ```

2. **Set Up a Virtual Environment (Optional):**

   ```bash
   python -m venv env
   source env/bin/activate  # For Linux/Mac
   env\Scripts\activate     # For Windows
   ```

3. **Install Dependencies:**

   ```bash
   pip install opencv-python numpy Pillow
   ```

   *Note: Tkinter is included with most Python installations. If it is not available, consult your OS documentation.*

## Usage

1. **Run the Application:**

   ```bash
   python <filename>.py
   ```

   Replace `<filename>.py` with the name of your script file (e.g., `main.py`).

2. **Interface Overview:**

   * **Left Panel:** Contains buttons for loading images, saving, resetting, undoing actions, and applying various filters.
   * **Right Panel:** Split into two sections:

     * **Top Section:** Displays the original loaded image.
     * **Bottom Section:** Shows the processed image after any filter or operation is applied.

3. **Applying Filters:**

   * Click the **Browse** button to open an image.
   * Select a filter by clicking its corresponding button (e.g., "Add Noise", "Gaussian Filter", etc.).
   * To revert to the previous state, click **Undo**. Use **Reset** to return to the original image.
   * Once satisfied with the result, click **Save Image** to store the processed image.

## Project Structure

```
image-processing-gui/
│
├── README.md                # Project overview and instructions
├── Image_Processing_GUI.py  # Main application script (contains the GUI and processing code)
└── requirements.txt         # List of dependencies (optional)
```

## How It Works

* **ImageProcessor Class:**
  Contains static methods for each image processing operation using OpenCV and NumPy. This includes adding noise, various filtering techniques, and morphological operations (erosion, dilation, opening, closing, boundary extraction, and region filling).

* **ImageFilterApp Class:**
  Manages the GUI built with Tkinter. It sets up the UI layout, handles user events (such as button clicks to apply filters), displays images on canvases, and maintains a history of applied filters for undo functionality.

* **Centering the Window:**
  The `center_window` function ensures the application window is centered on the screen when launched.

* **Event Handling:**
  The project leverages Tkinter’s built-in dialogs for image selection and error handling. Each processing button triggers the respective method from the `ImageProcessor` class and updates the display accordingly.

## Contributing

Contributions are welcome! If you have any ideas, bug fixes, or new features, please submit a pull request or open an issue on the GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
