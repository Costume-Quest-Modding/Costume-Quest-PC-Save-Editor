import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# ---------- Constants ----------
IMG_FOLDER = os.path.join(os.path.dirname(__file__), "images/cards") # folder containing your PNGs
IMG_PER_ROW = 11
IMG_SIZE = 64       # grid display size
HOVER_SCALE = 3    # 2x the grid size for hover popup

# Card names
CARD_NAMES = {
    1: "Raz-Ums", 2: "Glop", 3: "Wobblers", 4: "Choconana", 5: "Shimmerfizz", 6: "Chunkwutter",
    7: "Candy Hair", 8: "Moops", 9: "Chocolate Carrot", 10: "Fuds", 11: "Sweet Tooth", 12: "Jammie Jams",
    13: "Lollopops", 14: "Fruity Foam", 15: "Swedish Noses", 16: "Box Cake", 17: "Gooz", 18: "Fee-Fi-Fo-Fudge",
    19: "Slime Beetles", 20: "Sour Feet", 21: "Fish Head", 22: "Gummy Water", 23: "Licorice Cables", 24: "Cinnamon Brain",
    25: "Mossy Log", 26: "Wood Chips", 27: "Pizza Sundae", 28: "Sweet Fat", 29: "Pimples", 30: "Frozen Butter",
    31: "Edible Hat", 32: "Sludge", 33: "Coffee Toffee Taffee", 34: "Banana Beard", 35: "Broccoli Wafers", 36: "Gingerbread Ham",
    37: "Mice Crispy Treat", 38: "Jaw Hurters", 39: "Blobbles", 40: "Barf Roll-Ups", 41: "Chocolate Hamburger", 42: "Clippingz",
    43: "Salmon Rings", 44: "Street Chews", 45: "Fried Popcorn", 46: "Coconuts & Bolts", 47: "Jelly Has-Beens", 48: "Unicorn Pellets",
    49: "Misfortune Cookie", 50: "Sugar Bucket", 51: "Old Lady Fingers", 52: "Boogie Pie", 53: "Human Crackers", 54: "Gloop"
}

# ---------- Hover functions ----------
def show_hover(event, pil_img, card_name):
    top = tk.Toplevel()
    top.overrideredirect(True)
    top.attributes("-topmost", True)

    # Resize to 2x grid size
    resized_img = pil_img.resize((IMG_SIZE * HOVER_SCALE, IMG_SIZE * HOVER_SCALE), Image.Resampling.LANCZOS)
    tk_img = ImageTk.PhotoImage(resized_img)

    # Card name label
    name_lbl = tk.Label(top, text=card_name, font=("Arial", 12, "bold"))
    name_lbl.pack()

    # Image label
    img_lbl = tk.Label(top, image=tk_img)
    img_lbl.image = tk_img  # keep reference
    img_lbl.pack()

    # Position near cursor
    x, y = event.x_root + 10, event.y_root + 10
    top.geometry(f"+{x}+{y}")

    event.widget._popup = top  # store reference

def hide_hover(event):
    if hasattr(event.widget, "_popup"):
        event.widget._popup.destroy()
        del event.widget._popup

# ---------- Main program ----------
def main():
    root = tk.Tk()
    root.title("54 Cards with Hover Preview and Names")
    root.geometry("800x600")

    # Scrollable canvas
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Load images
    images = []  # list of tuples: (card_number, tk_img, pil_img)
    for i in range(1, 55):
        filename = f"trickcard_{i:03}.png"  # image_001.png ... image_054.png
        img_path = os.path.join(IMG_FOLDER, filename)
        if not os.path.exists(img_path):
            print(f"Warning: {filename} not found")
            continue

        pil_img = Image.open(img_path)
        resized_img = pil_img.resize((IMG_SIZE, IMG_SIZE), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(resized_img)
        images.append((i, tk_img, pil_img))

    # Display images with names and hover
    for idx, (num, tk_img, pil_img) in enumerate(images):
        row = idx // IMG_PER_ROW
        col = idx % IMG_PER_ROW

        # Image label
        lbl = tk.Label(scrollable_frame, image=tk_img)
        lbl.image = tk_img
        lbl.grid(row=row*2, column=col, padx=5, pady=5)

        card_name = CARD_NAMES.get(num, f"Card {num}")
        lbl.bind("<Enter>", lambda e, pil_img=pil_img, name=card_name: show_hover(e, pil_img, name))
        lbl.bind("<Leave>", hide_hover)

        # Card name label below grid image
        name_lbl = tk.Label(scrollable_frame, text=card_name, wraplength=IMG_SIZE, justify="center")
        name_lbl.grid(row=row*2 + 1, column=col, padx=5, pady=(0,10))

    root.mainloop()

if __name__ == "__main__":
    main()
