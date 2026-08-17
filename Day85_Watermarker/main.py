from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageTk


APP_DIR = Path(__file__).parent
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 755


root = tk.Tk()
root.title("Watermarker")

base_image = None
base_image_path = None
watermark_type = None
watermark_image = None
watermark_text = ""
preview_image = None


def load_font(size):
    font_path = APP_DIR / "Roboto.ttf"
    print(font_path)
    try:
        return ImageFont.truetype(font_path, size)
    except OSError:
        return ImageFont.load_default()


def make_text_watermark(text, base_size, opacity):
    font_size = max(12, int(min(base_size) * (size_var.get() / 100)))
    font = load_font(font_size)

    measuring_image = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
    draw = ImageDraw.Draw(measuring_image)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding = max(10, font_size // 4)
    mark = Image.new(
        "RGBA",
        (text_width + padding * 2, text_height + padding * 2),
        (255, 255, 255, 0),
    )
    draw = ImageDraw.Draw(mark)
    draw.text(
        (padding - bbox[0], padding - bbox[1]),
        text,
        font=font,
        fill=(255, 255, 255, opacity),
    )

    return mark


def make_image_watermark(base_size, opacity):
    image_width, image_height = watermark_image.size
    target_width = max(1, int(base_size[0] * (size_var.get() / 100)))
    target_height = max(1, int(target_width * image_height / image_width))

    mark = watermark_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    alpha = mark.getchannel("A")
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity / 255)
    mark.putalpha(alpha)

    return mark


def render_composite(target_image):
    if target_image is None:
        return None

    result = target_image.copy().convert("RGBA")

    if watermark_type is None:
        return result

    opacity = int(opacity_var.get())

    if watermark_type == "text":
        text = watermark_text.strip()
        if not text:
            return result
        mark = make_text_watermark(text, result.size, opacity)
    elif watermark_type == "image" and watermark_image is not None:
        mark = make_image_watermark(result.size, opacity)
    else:
        return result

    angle = int(rotation_var.get())
    mark = mark.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)

    center_x = int(result.width * (x_var.get() / 100))
    center_y = int(result.height * (y_var.get() / 100))
    paste_x = center_x - mark.width // 2
    paste_y = center_y - mark.height // 2

    result.alpha_composite(mark, (paste_x, paste_y))
    return result


def update_preview(*_):
    global preview_image

    image_canvas.delete("all")

    if base_image is None:
        image_canvas.create_text(
            DISPLAY_WIDTH // 2,
            DISPLAY_HEIGHT // 2,
            text="Import an image to begin",
            fill="white",
            font=("Arial", 20),
        )
        return

    composited = render_composite(base_image)
    fitted_image = ImageOps.contain(composited, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    preview_image = ImageTk.PhotoImage(fitted_image)

    image_canvas.create_image(
        DISPLAY_WIDTH // 2,
        DISPLAY_HEIGHT // 2,
        image=preview_image,
        anchor="center",
    )


def import_file():
    global base_image, base_image_path

    file_path = filedialog.askopenfilename(
        title="Select a base image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif"), ("All files", "*.*")],
    )

    if not file_path:
        return

    base_image_path = Path(file_path)
    base_image = Image.open(file_path).convert("RGBA")
    update_preview()


def add_text():
    global watermark_text, watermark_type

    text = text_var.get().strip()
    if not text:
        messagebox.showinfo("Add text", "Type the text you want to use first.")
        return

    watermark_text = text
    watermark_type = "text"
    update_preview()


def import_watermark():
    global watermark_image, watermark_type

    file_path = filedialog.askopenfilename(
        title="Select a watermark image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif"), ("All files", "*.*")],
    )

    if not file_path:
        return

    watermark_image = Image.open(file_path).convert("RGBA")
    watermark_type = "image"
    update_preview()


def save_image():
    if base_image is None:
        messagebox.showinfo("Save image", "Import a base image before saving.")
        return

    output_path = filedialog.asksaveasfilename(
        title="Save watermarked image",
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All files", "*.*")],
    )

    if not output_path:
        return

    final_image = render_composite(base_image)
    suffix = Path(output_path).suffix.lower()

    if suffix in {".jpg", ".jpeg"}:
        final_image = final_image.convert("RGB")

    final_image.save(output_path)
    messagebox.showinfo("Save image", f"Saved to:\n{output_path}")


def add_labeled_scale(parent, label, variable, from_, to, row):
    ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=(8, 0))

    scale = ttk.Scale(
        parent,
        from_=from_,
        to=to,
        variable=variable,
        command=update_preview,
    )
    scale.grid(row=row + 1, column=0, sticky="ew", padx=5)

    value_label = ttk.Label(parent, width=5)
    value_label.grid(row=row + 1, column=1, sticky="e", padx=5)

    def refresh_value(*_):
        value_label.config(text=str(int(variable.get())))

    variable.trace_add("write", refresh_value)
    refresh_value()

    return scale


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

image_canvas = tk.Canvas(
    root,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    bg="gray20",
    highlightthickness=0,
)
image_canvas.grid(row=0, column=0, sticky="nsew", padx=(8, 4), pady=(8, 4))

right_panel = ttk.Frame(root, padding=8)
right_panel.grid(row=0, column=1, sticky="new", padx=(4, 8), pady=(8, 4))
right_panel.columnconfigure(0, weight=1)

button_panel = ttk.Frame(root, padding=(8, 4, 8, 8))
button_panel.grid(row=1, column=0, sticky="n")

text_var = tk.StringVar()
x_var = tk.DoubleVar(value=50)
y_var = tk.DoubleVar(value=50)
size_var = tk.DoubleVar(value=15)
rotation_var = tk.DoubleVar(value=0)
opacity_var = tk.DoubleVar(value=160)

ttk.Label(right_panel, text="Watermark text").grid(row=0, column=0, columnspan=2, sticky="w", padx=5)
text_entry = ttk.Entry(right_panel, width=34, textvariable=text_var)
text_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(2, 8))

add_text_btn = ttk.Button(right_panel, text="Add text", command=add_text)
add_text_btn.grid(row=2, column=0, sticky="ew", padx=5, pady=4)

import_mark_btn = ttk.Button(right_panel, text="Import watermark", command=import_watermark)
import_mark_btn.grid(row=2, column=1, sticky="ew", padx=5, pady=4)

add_labeled_scale(right_panel, "Horizontal position", x_var, 0, 100, 3)
add_labeled_scale(right_panel, "Vertical position", y_var, 0, 100, 5)
add_labeled_scale(right_panel, "Size", size_var, 1, 60, 7)
add_labeled_scale(right_panel, "Rotation", rotation_var, 0, 360, 9)
add_labeled_scale(right_panel, "Opacity", opacity_var, 0, 255, 11)

save_button = ttk.Button(right_panel, text="Save image", command=save_image)
save_button.grid(row=13, column=0, columnspan=2, sticky="ew", padx=5, pady=(18, 4))

import_button = ttk.Button(button_panel, text="Import base image", command=import_file)
import_button.grid(row=0, column=0, padx=5, pady=5)

update_preview()
root.mainloop()
