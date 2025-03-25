import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Tkinter setup
root = tk.Tk()
root.title("Rendering Images with OpenCV")
root.geometry("800x700")

# Variable to store the image file path
file_path = None
original_img = None  # Store the original image
processed_img = None  # Store the processed image


# Image loading function
def load_image():
    global file_path, original_img, processed_img
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])

    if file_path:
        original_img = cv.imread(file_path)
        original_img = cv.cvtColor(original_img, cv.COLOR_BGR2RGB)  # Convert from BGR (OpenCV) to RGB
        processed_img = None  # Reset the processed image
        display_image(Image.fromarray(original_img))


# Function to display the image
def display_image(img):
    img = img.resize((400, 300))  # Resize to fit the window
    imgtk = ImageTk.PhotoImage(img)
    panel.config(image=imgtk)
    panel.image = imgtk


# Image saving function
def save_image():
    global processed_img
    if processed_img is not None:
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg"), ("JPEG files", "*.jpeg")],
            title="이미지 저장"
        )
        if save_path:
            Image.fromarray(processed_img).save(save_path)
            print(f"이미지가 저장되었습니다: {save_path}")


# Perfect cartoon style conversion
def apply_perfect_cartoon():
    global processed_img
    if file_path:
        img = cv.imread(file_path)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        # Highlight edges
        gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        edges = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 10)

        # Smooth colors
        blurred = cv.medianBlur(img, 7)
        smooth = cv.bilateralFilter(blurred, d=9, sigmaColor=150, sigmaSpace=150)  # Apply stronger filter

        # Color simplification (stronger effect)
        def stronger_color_quantization(image, k=5):  # Simplify colors more
            Z = image.reshape((-1, 3))
            Z = np.float32(Z)

            criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            _, labels, centers = cv.kmeans(Z, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

            centers = np.uint8(centers)
            res = centers[labels.flatten()]
            return res.reshape(image.shape)

        cartoonized = stronger_color_quantization(smooth, k=5)

        # Combine with edges
        cartoon = cv.bitwise_and(cartoonized, cartoonized, mask=edges)

        processed_img = cartoon  # Save the processed image
        display_image(Image.fromarray(cartoon))


# Show original image
def show_original():
    if original_img is not None:
        display_image(Image.fromarray(original_img))


# ESC key to quit the program
def exit_program(event=None):
    root.quit()

# UI buttons
btn_load = tk.Button(root, text="Load a image from Directory", command=load_image, width=30)
btn_original = tk.Button(root, text="Origine Image", command=show_original, width=30)
btn_perfect = tk.Button(root, text="Cartoon Style", command=apply_perfect_cartoon, width=30)
btn_save = tk.Button(root, text="Save a image", command=save_image, width=30)  # Save image button added
btn_exit = tk.Button(root, text="Exit", command=exit_program, width=30)

btn_load.pack(pady=5)
btn_original.pack(pady=5)
btn_perfect.pack(pady=5)
btn_save.pack(pady=5)  # Add the save button
btn_exit.pack(pady=5)

# Label to display the image
panel = tk.Label(root)
panel.pack()

# ESC key event binding
root.bind("<Escape>", exit_program)

# Start Tkinter
root.mainloop()