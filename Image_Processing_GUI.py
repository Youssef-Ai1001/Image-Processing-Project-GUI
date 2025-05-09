import tkinter as tk
from ImageFilterApp_class import ImageFilterApp

def center_window(window, width=1200, height=700):
    """Center the window on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageFilterApp(root)
    center_window(root)
    root.mainloop()
