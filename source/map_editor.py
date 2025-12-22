import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from constants import MAP_HOUSES, MAP_IMAGES


class MapEditor(ttk.Frame):
    def __init__(self, parent, initial_world="Suburbs", max_size=(800, 575)):
        super().__init__(parent)
        self.root = self.winfo_toplevel()
        self.max_width, self.max_height = max_size

        # --- Top controls ---
        top_frame = ttk.Frame(self)
        top_frame.pack(side="top", fill="x", padx=5, pady=5)

        # World selection
        self.world_var = tk.StringVar(value=initial_world)
        self.world_menu = ttk.OptionMenu(
            top_frame, self.world_var, initial_world, *MAP_IMAGES.keys(), command=self._change_world
        )
        self.world_menu.pack(side="left")

        # Zoom controls
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

        # --- Content frame ---
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            self.content_frame, bg="black", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # --- Side info panel ---
        self.side_panel = ttk.Frame(
            self.content_frame, width=260, relief="ridge")
        self.side_panel.pack_propagate(False)
        self.side_panel_visible = False

        header = ttk.Frame(self.side_panel)
        header.pack(fill="x", padx=6, pady=6)

        self.side_title = ttk.Label(
            header, text="Details", font=("Segoe UI", 11, "bold"))
        self.side_title.pack(side="left")

        close_btn = ttk.Button(header, text="X", width=3,
                               command=self._close_side_panel)
        close_btn.pack(side="right")

        self.side_body = ttk.Frame(self.side_panel)
        self.side_body.pack(fill="both", expand=True, padx=10, pady=10)

        self.info_var = tk.StringVar(value="Click a house")
        self.info_label = ttk.Label(
            self.side_body, textvariable=self.info_var, justify="left")
        self.info_label.pack(anchor="nw")

        self.coord_var = tk.StringVar(value="X: 0, Y: 0")
        self.coord_label = tk.Label(
            self.canvas, textvariable=self.coord_var, bg="black", fg="white")
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

        # Per-world view state (zoom, offsets, cursor)
        self._world_views = {}
        self._last_rel = (0, 0)

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

        self.current_zoom = 0.75
        self._user_moved = False
        self._close_side_panel()

        # Clear canvas
        self.canvas.delete("all")
        self.house_rects.clear()

        # Re-create the coord label window
        self.coord_label = tk.Label(
            self.canvas, textvariable=self.coord_var, bg="black", fg="white")
        self.coord_window = self.canvas.create_window(
            0, 0, anchor="ne", window=self.coord_label)

        # Load houses for this world
        self.houses = MAP_HOUSES.get(world_name, {})

        # Create the map image placeholder
        self.canvas_image = self.canvas.create_image(0, 0, anchor="nw")

        # Apply zoom (draws image and houses)
        self._set_zoom(self.current_zoom)

        # Restore saved view for this world (if available)
        state = self._world_views.get(world_name)
        if state:
            # restore zoom if different
            if state.get("zoom") is not None and state.get("zoom") != self.current_zoom:
                self._set_zoom(state["zoom"])
            # restore offsets
            self.offset_x = state.get("offset_x", self.offset_x)
            self.offset_y = state.get("offset_y", self.offset_y)
            self.canvas.coords(self.canvas_image, self.offset_x, self.offset_y)
            # reposition house rects using current scale
            scale_x = self.map_img.width / self.orig_w
            scale_y = self.map_img.height / self.orig_h
            for hid, rect in self.house_rects.items():
                x1, y1, x2, y2 = self.houses[hid]["coords"]
                self.canvas.coords(rect,
                                   x1 * scale_x + self.offset_x,
                                   y1 * scale_y + self.offset_y,
                                   x2 * scale_x + self.offset_x,
                                   y2 * scale_y + self.offset_y)
            # restore cursor display
            cur = state.get("cursor")
            if cur:
                self._last_rel = cur
                self.coord_var.set(f"X: {int(cur[0])}, Y: {int(cur[1])}")
        else:
            # nothing saved; ensure coord window position is updated
            self._update_coord_position()

    def _change_world(self, value):
        # persist current world's view before switching
        self._save_view_state()
        self._load_world(value)

    def _change_zoom(self, direction):
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

    def _zoom(self, event):
        if hasattr(event, "delta") and event.delta != 0:
            direction = 1 if event.delta > 0 else -1
        elif hasattr(event, "num"):
            direction = 1 if event.num == 4 else -1
        else:
            direction = 0
        self._change_zoom(direction)

    def _set_zoom(self, zoom):
        self.current_zoom = zoom
        new_size = (int(self.orig_w * zoom), int(self.orig_h * zoom))
        self.map_img = self.orig_img.resize(new_size, Image.NEAREST)
        self.tk_map = ImageTk.PhotoImage(self.map_img)
        self.canvas.itemconfig(self.canvas_image, image=self.tk_map)

        if not self._user_moved:
            self.offset_x = (self.max_width - new_size[0]) // 2
            self.offset_y = (self.max_height - new_size[1]) // 2

        self.canvas.coords(self.canvas_image, self.offset_x, self.offset_y)

        # Clear old rectangles
        for rect in self.house_rects.values():
            self.canvas.delete(rect)
        self.house_rects.clear()

        # Draw houses
        for hid, house in self.houses.items():
            x1, y1, x2, y2 = house["coords"]
            rect = self.canvas.create_rectangle(
                x1 * zoom + self.offset_x,
                y1 * zoom + self.offset_y,
                x2 * zoom + self.offset_x,
                y2 * zoom + self.offset_y,
                outline="red",
                width=2,
                fill="black",
                tags=hid
            )
            self.canvas.tag_bind(rect, "<ButtonRelease-1>",
                                 lambda e, h=hid: self.show_house_info(h))
            self.house_rects[hid] = rect

        self.zoom_label.config(text=f"{self.current_zoom}x")
        # ensure coord window remains on top
        self._raise_coord_window()

    # --- coords ---
    def _update_coords(self, event):
        rel_x = (self.canvas.canvasx(event.x) -
                 self.offset_x) / self.current_zoom
        rel_y = (self.canvas.canvasy(event.y) -
                 self.offset_y) / self.current_zoom
        rel_x = max(0, min(rel_x, self.orig_w))
        rel_y = max(0, min(rel_y, self.orig_h))
        # store last relative map coords for persistence
        self._last_rel = (rel_x, rel_y)
        self.coord_var.set(f"X: {int(rel_x)}, Y: {int(rel_y)}")

    def _update_coord_position(self):
        if not self.coord_window:
            return
        canvas_width = self.canvas.winfo_width()
        self.canvas.coords(self.coord_window, canvas_width - 10, 10)

    # --- drag & pan ---
    def _start_drag(self, event):
        item = self.canvas.find_withtag("current")
        if item and item[0] in self.house_rects.values():
            return
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
            x1, y1, x2, y2 = self.houses[hid]["coords"]
            self.canvas.coords(rect,
                               x1 * scale_x + self.offset_x,
                               y1 * scale_y + self.offset_y,
                               x2 * scale_x + self.offset_x,
                               y2 * scale_y + self.offset_y)
        self._update_coord_position()

    def _end_drag(self, event):
        self.drag_start = None

    # --- side panel ---
    def _open_side_panel(self):
        if not self.side_panel_visible:
            self.side_panel.pack(side="right", fill="y")
            self.root.update_idletasks()
            self.root.geometry(
                f"{self.root.winfo_width() + 260}x{self.root.winfo_height()}")
            self.side_panel_visible = True

    def _close_side_panel(self):
        if self.side_panel_visible:
            self.side_panel.pack_forget()
            self.root.update_idletasks()
            self.root.geometry(
                f"{self.root.winfo_width() - 260}x{self.root.winfo_height()}")
            self.side_panel_visible = False

    # --- house info ---
    def show_house_info(self, hid):
        house = self.houses[hid]
        x1, y1, x2, y2 = house["coords"]
        self.info_var.set(
            f"Name: {hid}\n"
            f"Description: {house['description']}\n"
            f"Category: {house['category']}\n"
            f"Subtype: {house['subtype']}\n"
            f"Reward: {house.get('reward', '')}\n\n"
            f"World: {self.world_name}\n"
            f"Internal Name: {house.get('internal_name', '')}\n"
            f"Bounds:\n  X1: {x1}\n  Y1: {y1}\n  X2: {x2}\n  Y2: {y2}"
        )
        if not self.side_panel_visible:
            self._open_side_panel()

    def _save_view_state(self):
        """Persist the current view state (zoom, offsets, cursor) for the active world."""
        if not hasattr(self, "world_name"):
            return
        self._world_views[self.world_name] = {
            "zoom": self.current_zoom,
            "offset_x": self.offset_x,
            "offset_y": self.offset_y,
            "cursor": getattr(self, "_last_rel", None),
        }

    def _raise_coord_window(self):
        """Ensure the coord window is on top of the canvas stacking order."""
        try:
            if self.coord_window:
                self.canvas.tag_raise(self.coord_window)
        except tk.TclError:
            pass
