import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image, ImageDraw


# ---------------- MAIN WINDOW ----------------

window = tk.Tk()
window.title("ColourNest 🎨")
window.geometry("1000x750")
window.configure(bg="#FFF7FB")


# ---------------- VARIABLES ----------------

brush_color = "#000000"
brush_size = 5
eraser = False

last_x = None
last_y = None

undo_stack = []
redo_stack = []


# ---------------- IMAGE ----------------

image = Image.new("RGB", (900, 520), "white")
draw_image = ImageDraw.Draw(image)


# ---------------- DRAWING ----------------

def start_draw(event):
    global last_x, last_y

    last_x = event.x
    last_y = event.y


def draw(event):
    global last_x, last_y

    if last_x is None or last_y is None:
        last_x = event.x
        last_y = event.y
        return

    if eraser:
        color = "white"
    else:
        color = brush_color

    # Draw on Tkinter canvas
    canvas.create_line(
        last_x,
        last_y,
        event.x,
        event.y,
        fill=color,
        width=brush_size,
        capstyle=tk.ROUND,
        smooth=True
    )

    # Draw on PIL image
    draw_image.line(
        (last_x, last_y, event.x, event.y),
        fill=color,
        width=brush_size
    )

    last_x = event.x
    last_y = event.y


def stop_draw(event):
    global last_x, last_y

    last_x = None
    last_y = None


# ---------------- SAVE STATE ----------------

def save_state():
    undo_stack.append(image.copy())
    redo_stack.clear()


# ---------------- COLORS ----------------

def choose_color():
    global brush_color, eraser

    color = colorchooser.askcolor(title="Choose a color")

    if color[1] is not None:
        brush_color = color[1]
        eraser = False


def set_color(color):
    global brush_color, eraser

    brush_color = color
    eraser = False


# ---------------- TOOLS ----------------

def use_brush():
    global eraser
    eraser = False


def use_eraser():
    global eraser
    eraser = True


def set_size(size):
    global brush_size
    brush_size = size


# ---------------- CLEAR ----------------

def clear_canvas():
    save_state()

    canvas.delete("all")

    draw_image.rectangle(
        (0, 0, 900, 520),
        fill="white"
    )


# ---------------- UNDO ----------------

def undo():
    if undo_stack:

        redo_stack.append(image.copy())

        previous = undo_stack.pop()

        image.paste(previous)

        canvas.delete("all")

        display_image()


# ---------------- REDO ----------------

def redo():
    if redo_stack:

        undo_stack.append(image.copy())

        next_image = redo_stack.pop()

        image.paste(next_image)

        canvas.delete("all")

        display_image()


# ---------------- DISPLAY IMAGE ----------------

def display_image():

    photo = tk.PhotoImage(
        data=image_to_png()
    )

    canvas.image = photo

    canvas.create_image(
        0,
        0,
        image=photo,
        anchor="nw"
    )


def image_to_png():
    import io
    import base64

    buffer = io.BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    return base64.b64encode(
        buffer.getvalue()
    )


# ---------------- SAVE PNG ----------------

def save_drawing():

    filename = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("All Files", "*.*")
        ]
    )

    if filename:
        image.save(filename)


# ---------------- NEW CANVAS ----------------

def new_canvas():

    global image, draw_image

    canvas.delete("all")

    image = Image.new(
        "RGB",
        (900, 520),
        "white"
    )

    draw_image = ImageDraw.Draw(image)


# ---------------- TITLE ----------------

title = tk.Label(
    window,
    text="🎨 ColourNest",
    font=("Arial", 28, "bold"),
    bg="#FFF7FB",
    fg="#6D597A"
)

title.pack(pady=12)


subtitle = tk.Label(
    window,
    text="Draw • Doodle • Create ✨",
    font=("Arial", 12),
    bg="#FFF7FB",
    fg="#8E7D95"
)

subtitle.pack()


# ---------------- TOOLBAR ----------------

toolbar = tk.Frame(
    window,
    bg="#FFF7FB"
)

toolbar.pack(pady=10)


tk.Button(
    toolbar,
    text="🖌 Brush",
    command=use_brush,
    width=10
).pack(side="left", padx=4)


tk.Button(
    toolbar,
    text="🧽 Eraser",
    command=use_eraser,
    width=10
).pack(side="left", padx=4)


tk.Button(
    toolbar,
    text="🌈 Colors",
    command=choose_color,
    width=10
).pack(side="left", padx=4)


tk.Button(
    toolbar,
    text="↩ Undo",
    command=undo,
    width=10
).pack(side="left", padx=4)


tk.Button(
    toolbar,
    text="↪ Redo",
    command=redo,
    width=10
).pack(side="left", padx=4)


tk.Button(
    toolbar,
    text="🗑 Clear",
    command=clear_canvas,
    width=10
).pack(side="left", padx=4)


tk.Button(
    toolbar,
    text="🆕 New",
    command=new_canvas,
    width=10
).pack(side="left", padx=4)


tk.Button(
    toolbar,
    text="💾 Save",
    command=save_drawing,
    width=10
).pack(side="left", padx=4)


# ---------------- BRUSH SIZE ----------------

size_frame = tk.Frame(
    window,
    bg="#FFF7FB"
)

size_frame.pack(pady=5)


tk.Label(
    size_frame,
    text="Brush Size:",
    bg="#FFF7FB",
    font=("Arial", 11)
).pack(side="left", padx=5)


tk.Button(
    size_frame,
    text="Small",
    command=lambda: set_size(3)
).pack(side="left", padx=3)


tk.Button(
    size_frame,
    text="Medium",
    command=lambda: set_size(7)
).pack(side="left", padx=3)


tk.Button(
    size_frame,
    text="Large",
    command=lambda: set_size(15)
).pack(side="left", padx=3)


tk.Button(
    size_frame,
    text="XL",
    command=lambda: set_size(25)
).pack(side="left", padx=3)


# ---------------- PASTEL PALETTE ----------------

palette_frame = tk.Frame(
    window,
    bg="#FFF7FB"
)

palette_frame.pack(pady=8)


pastel_colors = [
    "#FFB7C5",
    "#FFC8DD",
    "#CDB4DB",
    "#BDE0FE",
    "#A2D2FF",
    "#BDE0C8",
    "#B7E4C7",
    "#FFF1A8",
    "#FFD6A5",
    "#FFADAD",
    "#E9C46A",
    "#D8B4FE",
    "#F4A261",
    "#CDEAC0",
    "#FFFFFF",
    "#000000"
]


for color in pastel_colors:

    tk.Button(
        palette_frame,
        bg=color,
        width=3,
        height=1,
        relief="raised",
        command=lambda c=color: set_color(c)
    ).pack(
        side="left",
        padx=2
    )


# ---------------- CANVAS ----------------

canvas = tk.Canvas(
    window,
    bg="white",
    width=900,
    height=520,
    highlightthickness=2,
    highlightbackground="#E8DDEB"
)

canvas.pack(pady=12)


# ---------------- MOUSE EVENTS ----------------

canvas.bind(
    "<Button-1>",
    start_draw
)

canvas.bind(
    "<B1-Motion>",
    draw
)

canvas.bind(
    "<ButtonRelease-1>",
    stop_draw
)


# ---------------- START ----------------

window.mainloop()