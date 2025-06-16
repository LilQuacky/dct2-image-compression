import os
import tkinter as tk

from tkinter import filedialog, messagebox
from tkinter import ttk
from main import dct2_compress


class DCT2App:
    def __init__(self, root):
        self.root = root
        self.root.title("DCT2 Image Compression Tool")
        self.root.geometry("500x500")
        self.root.configure(bg="#2e2e2e")

        self.file_path = tk.StringVar()
        self.output_folder = tk.StringVar(value=os.getcwd() + "\\output\\")
        self.F = tk.IntVar(value=8)
        self.d = tk.IntVar(value=10)
        self.show_img = tk.BooleanVar(value=True)

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "TLabel",
            background="#2e2e2e",
            foreground="white",
            font=('Helvetica', 10)
        )
        style.configure(
            "TEntry",
            fieldbackground="#424242",
            foreground="white",
            bordercolor="#4caf50",
            lightcolor="#4caf50",
            darkcolor="#2e2e2e",
            padding=5
        )
        style.configure(
            "TButton",
            padding=6,
            relief="flat",
            background="#4caf50",
            foreground="white"
        )
        style.map(
            "TButton",
            background=[("active", "#45a049")]
        )
        style.configure(
            "TCheckbutton",
            background="#2e2e2e",
            foreground="white")
        style.map(
            "TCheckbutton",
            background=[("active", "#3e3e3e")],
            foreground=[("active", "#ffffff")]
        )

        ttk.Label(self.root, text="Select a BMP image using the Browse button:").pack(pady=(10, 0))

        self.file_label = tk.Label(
            self.root,
            text="No file selected",
            bg="#424242",
            fg="white",
            relief="groove",
            width=50,
            height=2
        )
        self.file_label.pack(pady=10)

        ttk.Button(self.root, text="Browse", command=self.browse_file).pack(pady=5)

        ttk.Label(self.root, text="Output folder:").pack(pady=(15, 0))
        self.output_entry = ttk.Entry(self.root, textvariable=self.output_folder, width=50, style="TEntry")
        self.output_entry.pack(pady=10)
        ttk.Button(self.root, text="Select Folder", command=self.browse_output_folder).pack(pady=5)

        ttk.Label(self.root, text="Block size (F):").pack(pady=(15, 0))
        self.f_slider = tk.Scale(self.root, from_=1, to=64, orient=tk.HORIZONTAL, variable=self.F,
                                 command=self.update_d_slider, bg="#2e2e2e", fg="white", troughcolor="#4caf50",
                                 highlightthickness=0)
        self.f_slider.pack(padx=20, fill="x")

        ttk.Label(self.root, text="Frequency cut-off (d):").pack(pady=(15, 0))
        self.d_slider = tk.Scale(self.root, from_=0, to=14, orient=tk.HORIZONTAL, variable=self.d, bg="#2e2e2e",
                                 fg="white", troughcolor="#4caf50", highlightthickness=0)
        self.d_slider.pack(padx=20, fill="x")

        confirm_frame = tk.Frame(self.root, bg="#2e2e2e")
        confirm_frame.pack(pady=20)
        ttk.Button(confirm_frame, text="Confirm", command=self.submit).pack(side="left", padx=10)
        ttk.Checkbutton(confirm_frame, text="Show image at end", variable=self.show_img, style="TCheckbutton").pack(
            side="left")

    def update_d_slider(self, val):
        f_val = int(val)
        max_d = 2 * f_val - 2
        self.d_slider.config(to=max_d)
        if self.d.get() > max_d:
            self.d.set(max_d)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
        if filename:
            self.file_path.set(filename)
            self.file_label.config(text=os.path.basename(filename))

    def browse_output_folder(self):
        foldername = filedialog.askdirectory()
        if foldername:
            self.output_folder.set(foldername)

    def submit(self):
        try:
            f_value = self.F.get()
            d_value = self.d.get()
            file_path = self.file_path.get()
            output_folder = self.output_folder.get()
            show_img = self.show_img.get()

            if not os.path.isfile(file_path):
                raise ValueError("Invalid or no file selected.")
            if not os.path.isdir(output_folder):
                raise ValueError("Invalid or no output folder selected.")
            if f_value <= 0:
                raise ValueError("F must be a positive integer.")
            if not (0 <= d_value <= 2 * f_value - 2):
                raise ValueError(f"d must be between 0 and {2 * f_value - 2}.")

            dct2_compress(file_path, f_value, d_value, output_folder, show_img)

        except ValueError as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = DCT2App(root)
    root.mainloop()
