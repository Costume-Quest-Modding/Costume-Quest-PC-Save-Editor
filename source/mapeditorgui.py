import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import os

# -------------------------------
# MapObject class
# -------------------------------


class MapObject:
    def __init__(self, **kwargs):
        self.fields = kwargs

    def __getitem__(self, key):
        return self.fields.get(key, "")

    def __setitem__(self, key, value):
        self.fields[key] = value

    def to_text(self):
        text = ""
        for key, value in self.fields.items():
            text += f"{key}: {value}\n"
        return text.strip()

    @classmethod
    def from_text(cls, text_block):
        fields = {}
        for line in text_block.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip()
        return cls(**fields)


# -------------------------------
# MapManager class
# -------------------------------
class MapManager:
    def __init__(self):
        self.objects = []

    def add_object(self, map_object):
        self.objects.append(map_object)

    def remove_object(self, internal_name):
        self.objects = [
            obj for obj in self.objects if obj['InternalName'] != internal_name]

    def get_object(self, internal_name):
        for obj in self.objects:
            if obj['InternalName'] == internal_name:
                return obj
        return None

    def load_from_file(self, file_path):
        if not os.path.exists(file_path):
            return
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        blocks = content.split("-\n")
        self.objects = [MapObject.from_text(block)
                        for block in blocks if block.strip()]

    def save_to_file(self, file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            for obj in self.objects:
                f.write(obj.to_text() + "\n-\n")

    def sort_objects(self, by="InternalName"):
        self.objects.sort(key=lambda obj: obj[by].lower() if obj[by] else "")


# -------------------------------
# GUI
# -------------------------------
class MapEditorGUI(tk.Tk):
    def __init__(self, manager, file_path):
        super().__init__()
        self.title("Costume Quest Map Editor")
        self.manager = manager
        self.file_path = file_path

        self.create_widgets()
        self.populate_list()

    def create_widgets(self):
        # Treeview with InternalName | Name | Category | Subtype | Position | Reward | Description
        self.tree = ttk.Treeview(
            self,
            columns=("InternalName", "Name", "Category", "Subtype",
                     "Position", "Reward", "Description"),
            show="headings"
        )
        for col in ("InternalName", "Name", "Category", "Subtype", "Position", "Reward", "Description"):
            self.tree.heading(col, text=col)
        self.tree.bind("<Double-1>", self.edit_selected_object)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Buttons
        frame = tk.Frame(self)
        frame.pack(pady=5)
        tk.Button(frame, text="Load File", command=self.load_file).pack(
            side=tk.LEFT, padx=5)
        tk.Button(frame, text="Add Object", command=self.add_object).pack(
            side=tk.LEFT, padx=5)
        tk.Button(frame, text="Edit Object", command=self.edit_selected_object).pack(
            side=tk.LEFT, padx=5)
        tk.Button(frame, text="Remove Object",
                  command=self.remove_selected_object).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Duplicate Object",
                  command=self.duplicate_selected_object).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Sort by InternalName", command=lambda: self.sort_objects(
            "InternalName")).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Sort by Category", command=lambda: self.sort_objects(
            "Category")).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Save", command=self.save_file).pack(
            side=tk.LEFT, padx=5)
        tk.Button(frame, text="Exit", command=self.destroy).pack(
            side=tk.LEFT, padx=5)

    def populate_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for obj in self.manager.objects:
            # Ensure unique iid
            base_iid = obj['InternalName'] if obj['InternalName'] else str(
                id(obj))
            iid = base_iid
            counter = 1
            while iid in self.tree.get_children():
                iid = f"{base_iid}_{counter}"
                counter += 1

            self.tree.insert("", tk.END, iid=iid, values=(
                obj['InternalName'],
                obj['Name'],
                obj['Category'],
                obj['Subtype'],
                obj['Position'],
                obj['Reward'],
                obj['Description']
            ))

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select map object text file",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if not file_path:
            return
        self.file_path = file_path
        self.manager.load_from_file(file_path)
        self.populate_list()
        messagebox.showinfo("Load File", f"Loaded '{file_path}'.")

    def add_object(self):
        obj_data = self.get_object_fields()
        if obj_data:
            obj = MapObject(**obj_data)
            self.manager.add_object(obj)
            self.populate_list()

    def edit_selected_object(self, event=None):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Edit Object", "Select an object first.")
            return
        iid_values = self.tree.item(selected, "values")
        internal_name = iid_values[0] if iid_values else selected
        obj = self.manager.get_object(internal_name)
        if not obj:
            return
        new_data = self.get_object_fields(existing=obj.fields)
        if new_data:
            for k, v in new_data.items():
                obj[k] = v
            self.populate_list()

    def remove_selected_object(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Remove Object", "Select an object first.")
            return
        iid_values = self.tree.item(selected, "values")
        internal_name = iid_values[0] if iid_values else selected
        self.manager.remove_object(internal_name)
        self.populate_list()

    def duplicate_selected_object(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning(
                "Duplicate Object", "Select an object first.")
            return
        iid_values = self.tree.item(selected, "values")
        internal_name = iid_values[0] if iid_values else selected
        original = self.manager.get_object(internal_name)
        if not original:
            return

        # Create a copy
        new_fields = original.fields.copy()
        # Generate a unique InternalName
        base_name = new_fields.get("InternalName", "Copy")
        count = 1
        new_name = f"{base_name}_Copy"
        while self.manager.get_object(new_name):
            count += 1
            new_name = f"{base_name}_Copy{count}"
        new_fields["InternalName"] = new_name

        duplicate_obj = MapObject(**new_fields)
        self.manager.add_object(duplicate_obj)
        self.populate_list()
        messagebox.showinfo("Duplicate Object",
                            f"Duplicated '{base_name}' as '{new_name}'.")

    def sort_objects(self, field):
        self.manager.sort_objects(field)
        self.populate_list()

    def save_file(self):
        self.manager.save_to_file(self.file_path)
        messagebox.showinfo("Save", f"Saved to '{self.file_path}'.")

    def get_object_fields(self, existing=None):
        fields = {}
        # Input order: InternalName, Name, Category, Subtype, Position, Reward, Description
        prompts = ["InternalName", "Name", "Category",
                   "Subtype", "Position", "Reward", "Description"]
        for key in prompts:
            default = existing.get(key, "") if existing else ""
            value = simpledialog.askstring(
                "Input", f"{key}:", initialvalue=default, parent=self)
            if value is None:
                return None
            fields[key] = value

        # Optional fields for Card Trade
        if fields["Subtype"] == "Quest_CardTrade":
            for key in ["CardOffered", "CardRequested"]:
                default = existing.get(key, "") if existing else ""
                value = simpledialog.askstring(
                    "Input", f"{key}:", initialvalue=default, parent=self)
                if value is None:
                    return None
                fields[key] = value
        return fields


# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    file_path = "map_objects.txt"
    manager = MapManager()
    manager.load_from_file(file_path)

    app = MapEditorGUI(manager, file_path)
    app.geometry("1400x500")
    app.mainloop()

    # Save on exit
    manager.save_to_file(file_path)
