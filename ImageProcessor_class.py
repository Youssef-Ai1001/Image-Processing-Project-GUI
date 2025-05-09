import cv2
import numpy as np

class ImageProcessor:
    """Class for handling image processing operations"""

    @staticmethod
    def add_noise(image, intensity=0.05):
        """Add random noise to image"""
        row, col, ch = image.shape
        mean = 0
        sigma = intensity * 255
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = image + gauss
        return np.clip(noisy, 0, 255).astype(np.uint8)

    @staticmethod
    def remove_noise(image, ksize=5):
        """Remove noise using Non-Local Means Denoising"""
        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

    @staticmethod
    def mean_filter(image, ksize=5):
        """Apply mean filter"""
        return cv2.blur(image, (ksize, ksize))

    @staticmethod
    def median_filter(image, ksize=5):
        """Apply median filter"""
        return cv2.medianBlur(image, ksize)

    @staticmethod
    def gaussian_filter(image, ksize=5):
        """Apply Gaussian filter"""
        return cv2.GaussianBlur(image, (ksize, ksize), 0)

    @staticmethod
    def gaussian_noise(image, mean=0, sigma=25):
        """Add Gaussian noise to image"""
        row, col, ch = image.shape
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = image + gauss
        return np.clip(noisy, 0, 255).astype(np.uint8)

    @staticmethod
    def erosion(image, ksize=5):
        """Apply erosion operation"""
        # Convert to grayscale if it's not already
        if len(image.shape) > 2:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Threshold to get binary image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Create kernel and apply erosion
        kernel = np.ones((ksize, ksize), np.uint8)
        eroded = cv2.erode(binary, kernel, iterations=1)

        # Convert back to BGR if original was color
        if len(image.shape) > 2:
            return cv2.cvtColor(eroded, cv2.COLOR_GRAY2BGR)
        return eroded

    @staticmethod
    def dilation(image, ksize=5):
        """Apply dilation operation"""
        # Convert to grayscale if it's not already
        if len(image.shape) > 2:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Threshold to get binary image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Create kernel and apply dilation
        kernel = np.ones((ksize, ksize), np.uint8)
        dilated = cv2.dilate(binary, kernel, iterations=1)

        # Convert back to BGR if original was color
        if len(image.shape) > 2:
            return cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
        return dilated

    @staticmethod
    def opening(image, ksize=5):
        """Apply opening operation (erosion followed by dilation)"""
        if len(image.shape) > 2:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Threshold to get binary image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        kernel = np.ones((ksize, ksize), np.uint8)
        opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        if len(image.shape) > 2:
            return cv2.cvtColor(opened, cv2.COLOR_GRAY2BGR)
        return opened

    @staticmethod
    def closing(image, ksize=5):
        """Apply closing operation (dilation followed by erosion)"""
        if len(image.shape) > 2:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Threshold to get binary image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        kernel = np.ones((ksize, ksize), np.uint8)
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        if len(image.shape) > 2:
            return cv2.cvtColor(closed, cv2.COLOR_GRAY2BGR)
        return closed

    @staticmethod
    def boundary_extraction(image, ksize=5):
        """Extract boundaries from the image"""
        if len(image.shape) > 2:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Threshold to get binary image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        kernel = np.ones((ksize, ksize), np.uint8)
        # Boundary is original - eroded
        eroded = cv2.erode(binary, kernel, iterations=1)
        boundary = binary - eroded

        if len(image.shape) > 2:
            return cv2.cvtColor(boundary, cv2.COLOR_GRAY2BGR)
        return boundary

    @staticmethod
    def region_filling(image, ksize=5):
        """Fill holes in the regions"""
        if len(image.shape) > 2:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Threshold to get binary image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Invert image for flood fill
        inverted = cv2.bitwise_not(binary)

        # Create a mask slightly larger than the image
        h, w = binary.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)

        # Flood fill from the borders
        floodfill = inverted.copy()
        cv2.floodFill(floodfill, mask, (0, 0), 255)

        # Invert floodfilled image
        floodfill_inv = cv2.bitwise_not(floodfill)

        # Combine the original and floodfilled image
        filled = binary | floodfill_inv

        if len(image.shape) > 2:
            return cv2.cvtColor(filled, cv2.COLOR_GRAY2BGR)
        return filled