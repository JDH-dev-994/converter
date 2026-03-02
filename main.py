import tkinter as tk
from tkinter import filedialog, ttk
import threading
import os
from converter import convert_pdf_to_json

class ConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF → JSON converter")
        self.root.geometry("600x400")
        
        self.pdf_folder = ""
        self.json_folder = ""

        self.create_widgets()

    def create_widgets(self):
        button_style = {"bg": "#2d2d2d", "fg": "white", "activebackground": "#444"}

        tk.Button(self.root, text="choose folder with PDF",
                  command=self.select_pdf_folder, **button_style).pack(pady=5)
        tk.Button(self.root, text="choose folder for JSON",
                  command=self.select_json_folder, **button_style).pack(pady=5)
        
        self.start_button = tk.Button(self.root, text="start",
                                      command=self.start_thread,
                                      bg="#007acc", fg="white")
        self.start_button.pack(pady=10)
        
        self.status_label = tk.Label(self.root, text="READY",
                                     bg="#1e1e1e", fg="white")
        self.status_label.pack()
        
        self.progress = ttk.Progressbar(self.root, mode="determinate")
        self.progress.pack(fill="x", padx=20, pady=10)
        
        self.log_text = tk.Text(self.root, bg="#121212", fg="#00ff90")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def select_pdf_folder(self):
        self.pdf_folder = filedialog.askdirectory()
        self.log(f"PDF folder: {self.pdf_folder}")

    def select_json_folder(self):
        self.json_folder = filedialog.askdirectory()
        self.log(f"JSON folder: {self.json_folder}")

    def start_thread(self):
        thread = threading.Thread(target=self.start_conversion)
        thread.start()

    def start_conversion(self):
        if not self.pdf_folder or not self.json_folder:
            self.log("error: choose both folders!")
            return
        
        self.start_button.config(state="disabled")
        
        files = [f for f in os.listdir(self.pdf_folder) if f.lower().endswith(".pdf")]
        total = len(files)
        self.progress["maximum"] = total
        self.progress["value"] = 0

        self.log("=== starting of processing ===")

        for idx, file in enumerate(files, start=1):
            pdf_path = os.path.join(self.pdf_folder, file)
            try:
                convert_pdf_to_json(pdf_path, self.json_folder)
                self.log(f"[OK] {file}")
            except Exception as e:
                self.log(f"[ERROR] {file} -> {e}")
            self.progress["value"] = idx
            self.root.update_idletasks()

        self.log("=== processing finished ===")
        self.start_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterGUI(root)
    root.mainloop()
