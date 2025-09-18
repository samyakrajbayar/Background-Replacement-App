import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import os

class BackgroundReplacerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Replacer - Green Screen Tool")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.original_image = None
        self.background_image = None
        self.result_image = None
        self.preview_image = None
        
        # Color range variables (HSV)
        self.hue_min = tk.IntVar(value=35)
        self.hue_max = tk.IntVar(value=85)
        self.sat_min = tk.IntVar(value=40)
        self.sat_max = tk.IntVar(value=255)
        self.val_min = tk.IntVar(value=40)
        self.val_max = tk.IntVar(value=255)
        
        # Smoothing variables
        self.blur_kernel = tk.IntVar(value=5)
        self.erode_iterations = tk.IntVar(value=2)
        self.dilate_iterations = tk.IntVar(value=2)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main title
        title_label = tk.Label(self.root, text="🎬 Background Replacer", 
                             font=('Arial', 24, 'bold'), 
                             fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=20)
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel for controls
        self.create_control_panel(main_frame)
        
        # Right panel for images
        self.create_image_panel(main_frame)
        
    def create_control_panel(self, parent):
        control_frame = tk.Frame(parent, bg='#34495e', relief=tk.RAISED, bd=2)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # File operations section
        file_frame = tk.LabelFrame(control_frame, text="📁 File Operations", 
                                 font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e')
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Load original image button
        load_btn = tk.Button(file_frame, text="Load Original Image", 
                           command=self.load_original_image,
                           bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                           relief=tk.FLAT, padx=20, pady=8)
        load_btn.pack(pady=5, fill=tk.X, padx=10)
        
        # Load background image button
        bg_btn = tk.Button(file_frame, text="Load Background Image", 
                         command=self.load_background_image,
                         bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'),
                         relief=tk.FLAT, padx=20, pady=8)
        bg_btn.pack(pady=5, fill=tk.X, padx=10)
        
        # Color adjustment section
        color_frame = tk.LabelFrame(control_frame, text="🎨 Color Range (HSV)", 
                                  font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e')
        color_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Hue sliders
        self.create_slider_pair(color_frame, "Hue", self.hue_min, self.hue_max, 0, 179)
        
        # Saturation sliders
        self.create_slider_pair(color_frame, "Saturation", self.sat_min, self.sat_max, 0, 255)
        
        # Value sliders
        self.create_slider_pair(color_frame, "Value", self.val_min, self.val_max, 0, 255)
        
        # Processing section
        process_frame = tk.LabelFrame(control_frame, text="⚙️ Processing Options", 
                                    font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e')
        process_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Blur kernel size
        self.create_slider(process_frame, "Blur Kernel", self.blur_kernel, 1, 15, 2)
        
        # Erosion iterations
        self.create_slider(process_frame, "Erosion", self.erode_iterations, 0, 10)
        
        # Dilation iterations
        self.create_slider(process_frame, "Dilation", self.dilate_iterations, 0, 10)
        
        # Action buttons
        action_frame = tk.Frame(control_frame, bg='#34495e')
        action_frame.pack(fill=tk.X, padx=10, pady=20)
        
        # Process button
        process_btn = tk.Button(action_frame, text="🔄 Process Image", 
                              command=self.process_image,
                              bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                              relief=tk.FLAT, padx=20, pady=10)
        process_btn.pack(pady=5, fill=tk.X)
        
        # Save button
        save_btn = tk.Button(action_frame, text="💾 Save Result", 
                           command=self.save_result,
                           bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                           relief=tk.FLAT, padx=20, pady=10)
        save_btn.pack(pady=5, fill=tk.X)
        
        # Presets section
        preset_frame = tk.LabelFrame(control_frame, text="🎯 Quick Presets", 
                                   font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e')
        preset_frame.pack(fill=tk.X, padx=10, pady=10)
        
        green_preset_btn = tk.Button(preset_frame, text="Green Screen", 
                                   command=self.green_screen_preset,
                                   bg='#2ecc71', fg='white', font=('Arial', 10),
                                   relief=tk.FLAT, pady=5)
        green_preset_btn.pack(pady=2, fill=tk.X, padx=10)
        
        blue_preset_btn = tk.Button(preset_frame, text="Blue Screen", 
                                  command=self.blue_screen_preset,
                                  bg='#3498db', fg='white', font=('Arial', 10),
                                  relief=tk.FLAT, pady=5)
        blue_preset_btn.pack(pady=2, fill=tk.X, padx=10)
        
    def create_image_panel(self, parent):
        image_frame = tk.Frame(parent, bg='#2c3e50')
        image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(image_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Original image tab
        self.original_tab = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(self.original_tab, text="Original")
        
        self.original_canvas = tk.Canvas(self.original_tab, bg='white', 
                                       relief=tk.SUNKEN, bd=2)
        self.original_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Background image tab
        self.background_tab = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(self.background_tab, text="Background")
        
        self.background_canvas = tk.Canvas(self.background_tab, bg='white', 
                                         relief=tk.SUNKEN, bd=2)
        self.background_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Result image tab
        self.result_tab = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(self.result_tab, text="Result")
        
        self.result_canvas = tk.Canvas(self.result_tab, bg='white', 
                                     relief=tk.SUNKEN, bd=2)
        self.result_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Mask preview tab
        self.mask_tab = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(self.mask_tab, text="Mask Preview")
        
        self.mask_canvas = tk.Canvas(self.mask_tab, bg='white', 
                                   relief=tk.SUNKEN, bd=2)
        self.mask_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_slider_pair(self, parent, label, var_min, var_max, min_val, max_val):
        frame = tk.Frame(parent, bg='#34495e')
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame, text=f"{label}:", fg='#ecf0f1', bg='#34495e', 
                font=('Arial', 10)).pack(anchor=tk.W)
        
        min_frame = tk.Frame(frame, bg='#34495e')
        min_frame.pack(fill=tk.X, pady=2)
        tk.Label(min_frame, text="Min:", fg='#bdc3c7', bg='#34495e', 
                font=('Arial', 9)).pack(side=tk.LEFT)
        min_scale = tk.Scale(min_frame, from_=min_val, to=max_val, orient=tk.HORIZONTAL,
                           variable=var_min, bg='#34495e', fg='#ecf0f1',
                           highlightthickness=0, command=self.on_slider_change)
        min_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        max_frame = tk.Frame(frame, bg='#34495e')
        max_frame.pack(fill=tk.X, pady=2)
        tk.Label(max_frame, text="Max:", fg='#bdc3c7', bg='#34495e', 
                font=('Arial', 9)).pack(side=tk.LEFT)
        max_scale = tk.Scale(max_frame, from_=min_val, to=max_val, orient=tk.HORIZONTAL,
                           variable=var_max, bg='#34495e', fg='#ecf0f1',
                           highlightthickness=0, command=self.on_slider_change)
        max_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
    def create_slider(self, parent, label, variable, min_val, max_val, step=1):
        frame = tk.Frame(parent, bg='#34495e')
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame, text=f"{label}:", fg='#ecf0f1', bg='#34495e', 
                font=('Arial', 10)).pack(anchor=tk.W)
        
        scale = tk.Scale(frame, from_=min_val, to=max_val, orient=tk.HORIZONTAL,
                        variable=variable, bg='#34495e', fg='#ecf0f1',
                        highlightthickness=0, resolution=step,
                        command=self.on_slider_change)
        scale.pack(fill=tk.X, pady=2)
        
    def on_slider_change(self, value):
        # Real-time preview update when sliders change
        if self.original_image is not None:
            self.update_mask_preview()
    
    def load_original_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Original Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.original_image = cv2.imread(file_path)
            if self.original_image is not None:
                self.display_image(self.original_image, self.original_canvas)
                self.update_mask_preview()
            else:
                messagebox.showerror("Error", "Could not load the image!")
    
    def load_background_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Background Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.background_image = cv2.imread(file_path)
            if self.background_image is not None:
                self.display_image(self.background_image, self.background_canvas)
            else:
                messagebox.showerror("Error", "Could not load the background image!")
    
    def display_image(self, cv_image, canvas):
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        
        # Get canvas dimensions
        canvas.update()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width, canvas_height = 400, 300
        
        # Resize image to fit canvas while maintaining aspect ratio
        h, w = rgb_image.shape[:2]
        aspect_ratio = w / h
        
        if canvas_width / canvas_height > aspect_ratio:
            new_height = canvas_height - 20
            new_width = int(new_height * aspect_ratio)
        else:
            new_width = canvas_width - 20
            new_height = int(new_width / aspect_ratio)
        
        resized_image = cv2.resize(rgb_image, (new_width, new_height))
        
        # Convert to PIL Image and then to PhotoImage
        pil_image = Image.fromarray(resized_image)
        photo = ImageTk.PhotoImage(pil_image)
        
        # Clear canvas and display image
        canvas.delete("all")
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        canvas.create_image(x, y, anchor=tk.NW, image=photo)
        
        # Keep a reference to prevent garbage collection
        canvas.image = photo
    
    def update_mask_preview(self):
        if self.original_image is None:
            return
            
        # Create mask using current settings
        mask = self.create_mask(self.original_image)
        
        # Convert mask to 3-channel for display
        mask_display = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        
        # Display the mask
        self.display_image(mask_display, self.mask_canvas)
    
    def create_mask(self, image):
        # Convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Create mask based on HSV range
        lower = np.array([self.hue_min.get(), self.sat_min.get(), self.val_min.get()])
        upper = np.array([self.hue_max.get(), self.sat_max.get(), self.val_max.get()])
        
        mask = cv2.inRange(hsv, lower, upper)
        
        # Apply blur if kernel size > 1
        kernel_size = self.blur_kernel.get()
        if kernel_size > 1:
            # Ensure kernel size is odd
            if kernel_size % 2 == 0:
                kernel_size += 1
            mask = cv2.medianBlur(mask, kernel_size)
        
        # Apply morphological operations
        kernel = np.ones((3, 3), np.uint8)
        
        if self.erode_iterations.get() > 0:
            mask = cv2.erode(mask, kernel, iterations=self.erode_iterations.get())
        
        if self.dilate_iterations.get() > 0:
            mask = cv2.dilate(mask, kernel, iterations=self.dilate_iterations.get())
        
        return mask
    
    def process_image(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an original image first!")
            return
        
        if self.background_image is None:
            messagebox.showwarning("Warning", "Please load a background image first!")
            return
        
        # Resize background to match original image
        h, w = self.original_image.shape[:2]
        background_resized = cv2.resize(self.background_image, (w, h))
        
        # Create mask
        mask = self.create_mask(self.original_image)
        
        # Invert mask (we want to keep the subject, not the background)
        mask_inv = cv2.bitwise_not(mask)
        
        # Apply Gaussian blur to the mask edges for smoother blending
        mask_blurred = cv2.GaussianBlur(mask_inv, (5, 5), 0)
        mask_normalized = mask_blurred.astype(np.float64) / 255.0
        
        # Create the result image with smooth blending
        self.result_image = self.original_image.copy().astype(np.float64)
        
        for c in range(3):
            self.result_image[:, :, c] = (
                mask_normalized * self.original_image[:, :, c] + 
                (1 - mask_normalized) * background_resized[:, :, c]
            )
        
        self.result_image = self.result_image.astype(np.uint8)
        
        # Display result
        self.display_image(self.result_image, self.result_canvas)
        
        messagebox.showinfo("Success", "Image processed successfully!")
    
    def save_result(self):
        if self.result_image is None:
            messagebox.showwarning("Warning", "No processed image to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Result Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            cv2.imwrite(file_path, self.result_image)
            messagebox.showinfo("Success", f"Image saved successfully to {file_path}")
    
    def green_screen_preset(self):
        # Typical green screen values
        self.hue_min.set(35)
        self.hue_max.set(85)
        self.sat_min.set(40)
        self.sat_max.set(255)
        self.val_min.set(40)
        self.val_max.set(255)
        self.blur_kernel.set(5)
        self.erode_iterations.set(2)
        self.dilate_iterations.set(2)
        self.update_mask_preview()
    
    def blue_screen_preset(self):
        # Typical blue screen values
        self.hue_min.set(100)
        self.hue_max.set(130)
        self.sat_min.set(50)
        self.sat_max.set(255)
        self.val_min.set(50)
        self.val_max.set(255)
        self.blur_kernel.set(5)
        self.erode_iterations.set(2)
        self.dilate_iterations.set(2)
        self.update_mask_preview()

def main():
    root = tk.Tk()
    app = BackgroundReplacerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()