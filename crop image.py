from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

class ImageResizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Resizer")

        # Initialize paths and resolution variables
        self.input_image_path = ""
        self.output_image_path = ""
        self.new_resolution = (0, 0)

        # Create Tkinter window box with function create_widgets
        self.create_widgets()

    def create_widgets(self):
        # Input image selection
        self.input_label = tk.Label(self.master, text="Select Image:")
        self.input_label.grid(row=0, column=0, padx=10, pady=10)

        self.input_entry = tk.Entry(self.master, width=40, state='disabled')
        self.input_entry.grid(row=0, column=1, padx=10, pady=10)

        self.browse_button = tk.Button(self.master, text="Browse", command=self.browse_input_image)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)

        # New resolution input boxes
        self.resolution_label = tk.Label(self.master, text="New Resolution (Width x Height):")
        self.resolution_label.grid(row=1, column=0, padx=10, pady=10)

        self.width_entry = tk.Entry(self.master, width=10)
        self.width_entry.grid(row=1, column=1, padx=5, pady=10)

        self.height_entry = tk.Entry(self.master, width=10)
        self.height_entry.grid(row=1, column=2, padx=5, pady=10)

        # Resize button - Complets operation and triggers resize_image function
        self.resize_button = tk.Button(self.master, text="Resize Image", command=self.resize_image)
        self.resize_button.grid(row=2, column=1, pady=20)

    def browse_input_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            self.input_image_path = file_path
            self.input_entry.config(state='normal')
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)
            self.input_entry.config(state='disabled')

            # Load the selected image
            image = Image.open(file_path)
            image.thumbnail((200, 200))
            # Display the selected image
            tk_image = ImageTk.PhotoImage(image)
            self.image_label = tk.Label(self.master, image=tk_image)
            self.image_label.image = tk_image
            self.image_label.grid(row=3, column=1, pady=10)

    def resize_image(self):
        try:
            # Get the new resolution from the "input_entry" above
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            self.new_resolution = (width, height)

            # Check if an input image is selected (dev note - just use an if true next time)
            if not self.input_image_path:
                messagebox.showerror("Error", "Please select an input image.")
                return

            # Specify output file path
            self.output_image_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")])

            # Check if an output path is provided
            if not self.output_image_path:
                return

            # Open the image file
            with Image.open(self.input_image_path) as img:
                # Convert RGBA to RGB just in case
                if img.mode == 'RGBA':
                    img = img.convert('RGB')

                # Resize the image using "BICUBIC resampling" - No idea what BICUBIC means but it works
                resized_img = img.resize(self.new_resolution, Image.BICUBIC)

                # Save the resized image to the output path defined before
                resized_img.save(self.output_image_path)

                messagebox.showinfo("Success", f"Image resolution changed and saved to {self.output_image_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")



if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()
