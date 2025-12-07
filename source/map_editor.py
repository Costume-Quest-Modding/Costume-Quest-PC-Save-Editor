import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from constants import MAP_HOUSES, MAP_IMAGES


class MapEditor(ttk.Frame):
    def __init__(self, parent, initial_world="Suburbs", max_size=(800, 575)):
        super().__init__(parent)
        self.max_width, self.max_height = max_size

        # --- Top controls frame ---
        top_frame = ttk.Frame(self)
        top_frame.pack(side="top", fill="x", padx=5, pady=5)

        # World selection
        self.world_var = tk.StringVar(value=initial_world)
        self.world_menu = ttk.OptionMenu(
            top_frame, self.world_var, initial_world, *MAP_IMAGES.keys(), command=self._change_world
        )
        self.world_menu.pack(side="left")

        # Zoom controls frame
        zoom_frame = ttk.Frame(top_frame)
        zoom_frame.pack(side="left", padx=10)

        self.zoom_levels = [0.5, 0.75, 1, 1.25, 1.5, 2]
        self.current_zoom = 0.75

        self.zoom_label = ttk.Label(
            zoom_frame, text=f"{self.current_zoom}x", width=6, anchor="center")
        self.zoom_label.pack(side="left")

        self.zoom_minus = ttk.Button(
            zoom_frame, text="-", width=3, command=lambda: self._change_zoom(-1))
        self.zoom_minus.pack(side="left", padx=(0, 2))
        self.zoom_plus = ttk.Button(
            zoom_frame, text="+", width=3, command=lambda: self._change_zoom(1))
        self.zoom_plus.pack(side="left")

        # --- Canvas ---
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Coord label
        self.coord_var = tk.StringVar(value="X: 0, Y: 0")
        self.coord_label = tk.Label(self.canvas, textvariable=self.coord_var,
                                    bg="black", fg="white")
        self.coord_window = self.canvas.create_window(
            0, 0, anchor="ne", window=self.coord_label)

        # Drag / pan
        self.offset_x = 0
        self.offset_y = 0
        self.drag_start = None
        self._user_moved = False

        # Houses
        self.houses = {}
        self.house_rects = {}

        # Bindings
        self.canvas.bind("<Motion>", self._update_coords)
        self.canvas.bind("<MouseWheel>", self._zoom)
        self.canvas.bind("<Button-4>", self._zoom)
        self.canvas.bind("<Button-5>", self._zoom)
        self.canvas.bind("<ButtonPress-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._drag)
        self.canvas.bind("<ButtonRelease-1>", self._end_drag)
        self.canvas.bind(
            "<Configure>", lambda e: self._update_coord_position())

        # Load initial map
        self._load_world(initial_world)

    # -----------------------------
    # Core Methods
    # -----------------------------
    def _load_world(self, world_name):
        self.world_name = world_name
        map_path = MAP_IMAGES.get(world_name)
        if not map_path or not os.path.isfile(map_path):
            self.canvas.delete("all")
            self.canvas.create_text(
                200, 200, text=f"Map '{world_name}' not found", fill="red")
            return

        self.orig_img = Image.open(map_path)
        self.orig_w, self.orig_h = self.orig_img.size

        # Reset zoom
        self.current_zoom = 0.75
        self._user_moved = False

        # Clear old canvas items
        self.canvas.delete("all")
        self.house_rects.clear()

        # Load houses from constants once
        self.houses = MAP_HOUSES.get(world_name, {})

        # Create the canvas image placeholder
        self.canvas_image = self.canvas.create_image(0, 0, anchor="nw")

        # Create windows for coord label
        self.coord_window = self.canvas.create_window(
            0, 0, anchor="ne", window=self.coord_label)

        # Apply zoom (draws image and houses)
        self._set_zoom(self.current_zoom)

    def _change_world(self, value):
        self._load_world(value)

    def _change_zoom(self, direction):
        """direction: +1 to zoom in, -1 to zoom out"""
        try:
            idx = self.zoom_levels.index(self.current_zoom)
        except ValueError:
            idx = 1

        if direction > 0 and idx < len(self.zoom_levels) - 1:
            next_zoom = self.zoom_levels[idx + 1]
        elif direction < 0 and idx > 0:
            next_zoom = self.zoom_levels[idx - 1]
        else:
            return

        self._set_zoom(next_zoom)

    # --- zoom with scroll wheel ---
    def _zoom(self, event):
        if hasattr(event, "delta") and event.delta != 0:
            direction = 1 if event.delta > 0 else -1
        elif hasattr(event, "num"):
            direction = 1 if event.num == 4 else -1
        else:
            direction = 0
        self._change_zoom(direction)

    # --- the missing _set_zoom method ---
    def _set_zoom(self, zoom):
        prev_zoom = self.current_zoom
        self.current_zoom = zoom
        new_size = (int(self.orig_w * zoom), int(self.orig_h * zoom))
        self.map_img = self.orig_img.resize(new_size, Image.NEAREST)
        self.tk_map = ImageTk.PhotoImage(self.map_img)

        # Update canvas image
        self.canvas.itemconfig(self.canvas_image, image=self.tk_map)

        # Center map if user hasn't moved
        if not self._user_moved:
            self.offset_x = (self.max_width - new_size[0]) // 2
            self.offset_y = (self.max_height - new_size[1]) // 2

        self.canvas.coords(self.canvas_image, self.offset_x, self.offset_y)

        # Clear old house rectangles
        for rect in self.house_rects.values():
            self.canvas.delete(rect)
        self.house_rects.clear()

        # Draw new house rectangles using existing self.houses
        for hid, (x1, y1, x2, y2) in self.houses.items():
            rect = self.canvas.create_rectangle(
                x1 * zoom + self.offset_x,
                y1 * zoom + self.offset_y,
                x2 * zoom + self.offset_x,
                y2 * zoom + self.offset_y,
                outline="red", width=2, tags=hid
            )
            self.canvas.tag_bind(hid, "<Button-1>", lambda e,
                                 h=hid: self.toggle_house(h))
            self.house_rects[hid] = rect

        # Update zoom label
        self.zoom_label.config(text=f"{self.current_zoom}x")

    # --- image resizing ---

    def _resize_image_to_max(self, img):
        w, h = img.size
        max_w, max_h = self.max_width, self.max_height
        if w > max_w or h > max_h:
            ratio = min(max_w / w, max_h / h)
            return img.resize((int(w * ratio), int(h * ratio)), Image.NEAREST)
        return img

    # --- house click ---
    def toggle_house(self, hid):
        print(f"Clicked: {hid}")

    # --- coords ---
    def _update_coords(self, event):
        rel_x = (self.canvas.canvasx(event.x) -
                 self.offset_x) / self.current_zoom
        rel_y = (self.canvas.canvasy(event.y) -
                 self.offset_y) / self.current_zoom
        rel_x = max(0, min(rel_x, self.orig_w))
        rel_y = max(0, min(rel_y, self.orig_h))
        self.coord_var.set(f"X: {int(rel_x)}, Y: {int(rel_y)}")

    def _update_coord_position(self):
        canvas_width = self.canvas.winfo_width()
        self.canvas.coords(self.coord_window, canvas_width - 10, 10)

    # --- drag & pan ---
    def _start_drag(self, event):
        self.drag_start = (event.x, event.y)

    def _drag(self, event):
        if not self.drag_start:
            return
        dx = event.x - self.drag_start[0]
        dy = event.y - self.drag_start[1]
        self.offset_x += dx
        self.offset_y += dy
        self.drag_start = (event.x, event.y)
        self._user_moved = True

        self.canvas.coords(self.canvas_image, self.offset_x, self.offset_y)
        scale_x = self.map_img.width / self.orig_w
        scale_y = self.map_img.height / self.orig_h
        for hid, rect in self.house_rects.items():
            x1, y1, x2, y2 = self.houses[hid]
            self.canvas.coords(rect,
                               x1 * scale_x + self.offset_x,
                               y1 * scale_y + self.offset_y,
                               x2 * scale_x + self.offset_x,
                               y2 * scale_y + self.offset_y)
        self._update_coord_position()

    def _end_drag(self, event):
        self.drag_start = None
