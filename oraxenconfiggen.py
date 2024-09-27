import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

item_template = """
{item_name}:
  itemname: <white>{display_name}
  material: PAPER
  Mechanics:
    furniture:
      limited_placing:
        roof: false
        floor: true
        wall: false
      barrier: false
      type: ITEM_FRAME
      drop:
        silktouch: false
        loots:
        - oraxen_item: {item_name}
          probability: 1
  Pack:
    generate_model: false
    model: {model_path}/{item_name}
    custom_model_data: {custom_model_data}
"""

sittable_template = """
{item_name}:
  itemname: <white>{display_name}
  material: PAPER
  Mechanics:
    furniture:
      limited_placing:
        roof: false
        floor: true
        wall: false
      barrier: false
      seat:
        height: -0.1
        yaw: 0
      type: ITEM_FRAME
      drop:
        silktouch: false
        loots:
        - oraxen_item: {item_name}
          probability: 1
  Pack:
    generate_model: false
    model: {model_path}/{item_name}
    custom_model_data: {custom_model_data}
"""

class OraxenConfigGen:
    def __init__(self, root):
        self.root = root
        self.root.title("Oraxen Configuration Generator")
        self.select_folder_button = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack(pady=10)
        self.file_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50, height=15)
        self.file_listbox.pack(pady=10)
        self.chairs_button = tk.Button(root, text="Mark as Sittable", command=self.mark_as_chairs)
        self.chairs_button.pack(side=tk.LEFT, padx=10)
        self.non_chairs_button = tk.Button(root, text="Mark as Item", command=self.mark_as_non_chairs)
        self.non_chairs_button.pack(side=tk.RIGHT, padx=10)
        self.items = {}
        self.custom_model_data = 0 #CHANGE: Default starting number
        self.selected_folder = ""
        self.generate_yaml_button = tk.Button(root, text="Generate Configuration File", command=self.generate_config_file)
        self.generate_yaml_button.pack(pady=20)

    def select_folder(self):
        self.selected_folder = filedialog.askdirectory()
        if self.selected_folder:
            self.populate_file_list(self.selected_folder)

    def populate_file_list(self, folder_path):
        self.file_listbox.delete(0, tk.END)
        self.items.clear()

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                item_name = os.path.splitext(filename)[0]
                self.file_listbox.insert(tk.END, item_name)

    def mark_as_chairs(self):
        selected_files = self.file_listbox.curselection()
        for index in selected_files:
            item_name = self.file_listbox.get(index)
            self.items[item_name] = "chair"
            self.file_listbox.itemconfig(index, {'bg': 'lightgreen'})

        self.file_listbox.selection_clear(0, tk.END)
        messagebox.showinfo("Marked as Sittable", f"Marked {len(selected_files)} items as sittable.")

    def mark_as_non_chairs(self):
        selected_files = self.file_listbox.curselection()
        for index in selected_files:
            item_name = self.file_listbox.get(index)
            self.items[item_name] = "non-chair"
            self.file_listbox.itemconfig(index, {'bg': 'lightcoral'})

        self.file_listbox.selection_clear(0, tk.END)
        messagebox.showinfo("Marked as Items", f"Marked {len(selected_files)} items as non-sittable items.")

    def generate_config_file(self):
        file_name = simpledialog.askstring("Input", "Enter name for config file (do not include \".yml\"):")
        if not file_name:
            messagebox.showerror("Error", "No file name provided!")
            return

        self.custom_model_data = simpledialog.askinteger("Input", "Enter starting custom model data number:", initialvalue=0)
        if self.custom_model_data is None:
            messagebox.showerror("Error", "No custom model data number provided!")
            return

        folder_path = filedialog.askdirectory(title="Select Folder to Save Config File")
        if folder_path:
            full_file_path = os.path.join(folder_path, f"{file_name}.yml")

            with open(full_file_path, 'w') as yaml_file:
                for item_name, item_type in self.items.items():
                    yaml_data = self.generate_yaml(item_name, item_type)
                    yaml_file.write(yaml_data)

            messagebox.showinfo("Config Generation", "Config file has been successfully generated!")

    def generate_yaml(self, item_name, item_type):
        display_name = item_name.replace("_", " ").title()
        custom_model_data = self.custom_model_data
        self.custom_model_data += 1

        folder_name = os.path.basename(self.selected_folder)
        model_path = f"civicraft/{folder_name}" # CHANGE: Change this to whatever folder in the pack folder you are putting it in.

        if item_type == "chair":
            return sittable_template.format(item_name=item_name, display_name=display_name, custom_model_data=custom_model_data, model_path=model_path)
        else:
            return item_template.format(item_name=item_name, display_name=display_name, custom_model_data=custom_model_data, model_path=model_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = OraxenConfigGen(root)

    root.mainloop()
