import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
from ImageProcessor_class import ImageProcessor

class ImageFilterApp:
    """Main application class for image processing GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Tool")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        # Create the processor
        self.processor = ImageProcessor()

        # Initialize variables
        self.original_image = None
        self.current_image = None
        self.processed_image = None
        self.filter_history = []

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Style configuration
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10), padding=5)
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")

        # Left frame for buttons
        self.left_frame = ttk.Frame(main_frame, width=200)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Right frame for images
        self.right_frame = ttk.Frame(main_frame)
        self.right_frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10
        )

        # Top frame for original image
        self.top_frame = ttk.Frame(self.right_frame)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Bottom frame for processed image
        self.bottom_frame = ttk.Frame(self.right_frame)
        self.bottom_frame.pack(
            side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5
        )

        # Original image label
        self.original_label = ttk.Label(
            self.top_frame, text="Original Image", background="#e0e0e0"
        )
        self.original_label.pack(side=tk.TOP, pady=5)

        self.original_canvas = tk.Canvas(
            self.top_frame, bg="#e0e0e0", highlightthickness=0
        )
        self.original_canvas.pack(fill=tk.BOTH, expand=True)

        # Processed image label
        self.processed_label = ttk.Label(
            self.bottom_frame, text="Processed Image", background="#e0e0e0"
        )
        self.processed_label.pack(side=tk.TOP, pady=5)

        self.processed_canvas = tk.Canvas(
            self.bottom_frame, bg="#e0e0e0", highlightthickness=0
        )
        self.processed_canvas.pack(fill=tk.BOTH, expand=True)

        # Browse button
        browse_btn = ttk.Button(
            self.left_frame, text="Browse", command=self.browse_image
        )
        browse_btn.pack(fill=tk.X, pady=5)

        # Save button
        save_btn = ttk.Button(
            self.left_frame, text="Save Image", command=self.save_image
        )
        save_btn.pack(fill=tk.X, pady=5)

        # Reset button
        reset_btn = ttk.Button(self.left_frame, text="Reset", command=self.reset_image)
        reset_btn.pack(fill=tk.X, pady=5)

        # Undo button
        undo_btn = ttk.Button(self.left_frame, text="Undo", command=self.undo_filter)
        undo_btn.pack(fill=tk.X, pady=5)

        # Separator
        ttk.Separator(self.left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Filter buttons
        filters = [
            ("Add Noise", lambda: self.apply_filter(self.processor.add_noise)),
            ("Remove Noise", lambda: self.apply_filter(self.processor.remove_noise)),
            ("Mean Filter", lambda: self.apply_filter(self.processor.mean_filter)),
            ("Median Filter", lambda: self.apply_filter(self.processor.median_filter)),
            (
                "Gaussian Filter",
                lambda: self.apply_filter(self.processor.gaussian_filter),
            ),
            (
                "Gaussian Noise",
                lambda: self.apply_filter(self.processor.gaussian_noise),
            ),
            ("Erosion", lambda: self.apply_filter(self.processor.erosion)),
            ("Dilation", lambda: self.apply_filter(self.processor.dilation)),
            ("Opening", lambda: self.apply_filter(self.processor.opening)),
            ("Closing", lambda: self.apply_filter(self.processor.closing)),
            (
                "Boundary Extraction",
                lambda: self.apply_filter(self.processor.boundary_extraction),
            ),
            (
                "Region Filling",
                lambda: self.apply_filter(self.processor.region_filling),
            ),
        ]

        for text, command in filters:
            btn = ttk.Button(self.left_frame, text=text, command=command)
            btn.pack(fill=tk.X, pady=2)
            # Add styling to make buttons colorful
            btn.configure(style=f"{text.replace(' ', '')}.TButton")
            style.configure(
                f"{text.replace(' ', '')}.TButton",
                background="#4287f5",
                foreground="black",
            )

    def browse_image(self):
        """Open a file dialog to browse for an image"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]
        )

        if file_path:
            try:
                # Read the image with OpenCV
                self.original_image = cv2.imread(file_path)
                if self.original_image is None:
                    messagebox.showerror("Error", "Failed to load the image!")
                    return

                # Convert BGR to RGB for display
                rgb_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
                self.current_image = self.original_image.copy()
                self.processed_image = None
                self.filter_history = []

                # Display the image
                self.display_image(rgb_image, self.original_canvas)
                self.processed_canvas.delete("all")  # Clear processed image canvas

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_image(self, image, canvas):
        """Display an image on a canvas"""
        canvas.delete("all")  # Clear canvas

        # Convert to PIL Image
        pil_image = Image.fromarray(image.astype("uint8"))

        # Resize to fit canvas while maintaining aspect ratio
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        # Default size if canvas size is not yet determined
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 500
            canvas_height = 300

        # Calculate new dimensions
        img_width, img_height = pil_image.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        # Resize image
        resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)

        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(resized_image)

        # Keep a reference to prevent garbage collection
        canvas.image = photo

        # Add image to canvas
        canvas.create_image(
            canvas_width // 2, canvas_height // 2, image=photo, anchor=tk.CENTER
        )

    def apply_filter(self, filter_func):
        """Apply a filter to the current image"""
        if self.current_image is None:
            messagebox.showinfo("Info", "Please load an image first.")
            return

        try:
            # Save current image in history
            self.filter_history.append(self.current_image.copy())

            # Apply filter
            self.current_image = filter_func(self.current_image)

            # Convert BGR to RGB for display
            rgb_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)

            # Display processed image
            self.display_image(rgb_image, self.processed_canvas)

        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred applying the filter: {str(e)}"
            )

    def undo_filter(self):
        """Undo the last applied filter"""
        if not self.filter_history:
            messagebox.showinfo("Info", "No filters to undo.")
            return

        self.current_image = self.filter_history.pop()
        rgb_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        self.display_image(rgb_image, self.processed_canvas)

    def reset_image(self):
        """Reset to the original image"""
        if self.original_image is None:
            messagebox.showinfo("Info", "No image loaded.")
            return

        self.current_image = self.original_image.copy()
        self.filter_history = []

        # Clear processed image
        self.processed_canvas.delete("all")

    def save_image(self):
        """Save the processed image"""
        if self.current_image is None:
            messagebox.showinfo("Info", "No image to save.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[
                ("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            try:
                cv2.imwrite(file_path, self.current_image)
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")