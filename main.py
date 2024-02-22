import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import ImageTk, Image
import numpy as np


def browse_image():
    global image
    global original
    file_path = filedialog.askopenfilename()
    if file_path:
        original = cv2.imread(file_path)
        image = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        display_image(image)
        status_label.config(text=f"Selected: {file_path}")


def display_image(img):
    img = Image.fromarray(img)
    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo)
    image_label.image = photo


def convert_to_rgb():
    global image
    global original
    image = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    display_image(image)
    status_label.config(text="Converted to RGB")


def convert_to_grayscale():
    global image
    global original
    image = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    display_image(image)
    status_label.config(text="Converted to Grayscale")


def convert_to_binary():
    global image
    global original
    image = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    display_image(image)
    status_label.config(text="Converted to Binary")


def brightness(x):
    matrix = np.ones(image.shape, dtype="uint8") * abs(x)
    if x >= 0:
        image_modified = cv2.add(image, matrix)
        status_label.config(text=f"Increased brightness by {x}")
    else:
        image_modified = cv2.subtract(image, matrix)
        status_label.config(text=f"Decreased brightness by {abs(x)}")
    image_modified = Image.fromarray(image_modified)
    photo = ImageTk.PhotoImage(image_modified)
    image_label.config(image=photo)
    image_label.image = photo


def contrast(x):
    matrix = np.ones(image.shape) * abs(x)
    image_modified = np.uint8(np.clip(cv2.multiply(np.float64(image), matrix), 0, 255))
    image_modified = Image.fromarray(image_modified)
    photo = ImageTk.PhotoImage(image_modified)
    image_label.config(image=photo)
    image_label.image = photo
    status_label.config(text=f"Changed contrast by {x}")


def add_line():
    x1, y1 = int(x_entry.get()), int(y_entry.get())
    x2, y2 = int(x2_entry.get()), int(y2_entry.get())
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    display_image(image)

def add_rectangle():
    x1, y1 = int(x_entry.get()), int(y_entry.get())
    x2, y2 = int(x2_entry.get()), int(y2_entry.get())
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    display_image(image)

def add_circle():
    x, y = int(x_entry.get()), int(y_entry.get())
    radius = int(radius_entry.get())
    cv2.circle(image, (x, y), radius, (255, 0, 0), 2)
    display_image(image)

def add_text():
    x, y = int(x_entry.get()), int(y_entry.get())
    text = text_entry.get()
    cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    display_image(image)


root = tk.Tk()
root.title("Image Processor")

image_label = tk.Label(root)
image_label.pack(padx=10, pady=10)

status_label = tk.Label(root, text="")
status_label.pack(pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_image)
browse_button.pack(pady=5)

rgb_button = tk.Button(root, text="Convert to RGB", command=convert_to_rgb)
rgb_button.pack(pady=5)

grayscale_button = tk.Button(root, text="Convert to Grayscale", command=convert_to_grayscale)
grayscale_button.pack(pady=5)

binary_button = tk.Button(root, text="Convert to Binary", command=convert_to_binary)
binary_button.pack(pady=5)

brightness_scale = tk.Scale(root, label="Brightness", from_=-100, to=100, resolution=1, orient=tk.HORIZONTAL,
                            length=100,
                            command=lambda x: brightness(int(x)))
brightness_scale.set(0)
brightness_scale.pack(pady=5)

contrast_scale = tk.Scale(root, label="Contrast", from_=0.5, to=1.5, resolution=0.1, orient=tk.HORIZONTAL, length=100,
                          command=lambda x: contrast(float(x)))
contrast_scale.set(1)
contrast_scale.pack(pady=5)

x_label = tk.Label(root, text="X Coordinate:")
x_label.pack()

x_entry = tk.Entry(root, width=10)
x_entry.pack(pady=5)

y_label = tk.Label(root, text="Y Coordinate:")
y_label.pack()

y_entry = tk.Entry(root, width=10)
y_entry.pack(pady=5)

x2_label = tk.Label(root, text="X2 Coordinate:")
x2_label.pack()

x2_entry = tk.Entry(root, width=10)
x2_entry.pack(pady=5)

y2_label = tk.Label(root, text="Y2 Coordinate:")
y2_label.pack()

y2_entry = tk.Entry(root, width=10)
y2_entry.pack(pady=5)

radius_label = tk.Label(root, text="Radius:")
radius_label.pack()

radius_entry = tk.Entry(root, width=10)
radius_entry.pack(pady=5)

text_label = tk.Label(root, text="Text:")
text_label.pack()

text_entry = tk.Entry(root, width=30)
text_entry.pack(pady=5)

line_button = tk.Button(root, text="Add Line", command=add_line)
line_button.pack(pady=5)

rect_button = tk.Button(root, text="Add Rectangle", command=add_rectangle)
rect_button.pack(pady=5)

circle_button = tk.Button(root, text="Add Circle", command=add_circle)
circle_button.pack(pady=5)

text_button = tk.Button(root, text="Add Text", command=add_text)
text_button.pack(pady=5)

root.mainloop()
