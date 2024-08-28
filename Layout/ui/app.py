import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Client.client import upload_file, send_request
import subprocess
from PIL import Image, ImageTk, ImageOps
import ttkbootstrap as ttk  # Import ttkbootstrap for modern UI

class FileServerApp(ttk.Window):  # Inherit from ttk.Window for modern styling
    def __init__(self):
        super().__init__(themename="vapor")  # Apply the vapor theme
        self.title("File Server Client")
        self.geometry("1280x800")  # Expanded size for better layout
        self.create_widgets()

    def create_widgets(self):
        # Use the 'outline' style provided by the vapor theme
        # for outline buttons
        style = ttk.Style()
        style.configure(
            "Outline.TButton",
            font=("Poppins", 10, "bold"),  # Custom font
            padding=(10, 5),  # Increased padding for taller buttons
            relief="flat",  # Flat relief for outline effect
            borderwidth=2,
            bordercolor="#CCCCCC",  # Light color for the outline
            background="#333333",  # Dark background for button
            foreground="#94A3B8",  # Text color
        )
        style.map(
            "Outline.TButton",
            background=[
                ("active", "#6D28D9"),  # Purple background on hover (adjust as needed)
                ("pressed", "#5B21B6"),  # Darker purple on press (adjust as needed)
            ],
            bordercolor=[
                ("active", "#6D28D9"),  # Purple border on hover
                ("pressed", "#5B21B6"),  # Darker purple border on press
            ],
        )

        # Frame for main buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        upload_button = ttk.Button(
            button_frame,
            text="Subir Archivo",
            command=self.upload_file,
            style="Outline.TButton",
        )
        upload_button.pack(side=tk.LEFT, padx=20)

        delete_button = ttk.Button(
            button_frame,
            text="Borrar Todos los Archivos",
            command=self.delete_all_files,
            style="Outline.TButton",
        )
        delete_button.pack(side=tk.LEFT, padx=20)

        # Updated file display frame with padding and expandable layout
        self.file_frame = ttk.Frame(self)
        self.file_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.update_file_list()

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "rb") as f:
                content = f.read()
            filename = os.path.basename(file_path)
            response = upload_file(filename, content)
            messagebox.showinfo("Resultado", response)
            self.update_file_list()

    def update_file_list(self):
        for widget in self.file_frame.winfo_children():
            widget.destroy()

        request = "LIST_FILES"
        files = send_request(request)
        for file in files.split("\n"):
            if file:
                file_icon = self.get_file_icon(file)
                self.create_file_display(file, file_icon)

    def get_file_icon(self, filename):
        extension = filename.split(".")[-1].lower()
        icon_base_path = os.path.join(os.path.dirname(__file__), "..", "icons")

        match extension:
            case "jpg" | "jpeg" | "png" | "svg":
                icon_path = os.path.join(icon_base_path, "edit.png")
            case "txt" | "doc" | "pdf":
                icon_path = os.path.join(icon_base_path, "doc.png")
            case "py" | "c" | "js" | "ts" | "java":
                icon_path = os.path.join(icon_base_path, "code-file.png")
            case _:
                icon_path = os.path.join(icon_base_path, "attach.png")

        if not os.path.exists(icon_path):
            raise FileNotFoundError(f"El icono no se encuentra: {icon_path}")

        icon = Image.open(icon_path)
        # Darker border
        icon = icon.resize((100, 100), Image.Resampling.LANCZOS)  # Larger icons
        return ImageTk.PhotoImage(icon)

    def create_file_display(self, filename, file_icon):
        # File display with Google Drive style (rounded corners)
        file_frame = ttk.Frame(
            self.file_frame
        )
        file_frame.pack(side=tk.LEFT, padx=20, pady=20)

        icon_label = ttk.Label(file_frame, image=file_icon)
        icon_label.image = file_icon
        icon_label.pack(pady=15)

        # File label without underline and with dark theme consistent style
        file_label = ttk.Label(
            file_frame,
            text=filename,  # Keeps consistent with dark mode
            wraplength=180,
            font=("Poppins", 11, "normal"),  # No underline in this font style
            foreground="#94A3B8",  # White color text to prevent blue background
            # Matching the dark theme background
        )
        file_label.pack(pady=10)

        open_button = ttk.Button(
            file_frame,
            text="Abrir",
            command=lambda: self.open_file(filename),
            style="Outline.TButton",
            padding=(8, 4),  # Taller buttons for better interaction
            width=20,  # Increased width for uniformity
        )
        open_button.pack(pady=15, fill=tk.X)

        download_button = ttk.Button(
            file_frame,
            text="Descargar",
            command=lambda: self.download_file(filename),
            style="Outline.TButton",
            padding=(8, 4),  # Taller buttons for better interaction
            width=20,  # Increased width for uniformity
        )
        download_button.pack(pady=15, fill=tk.X)

    def open_file(self, filename):
        filepath = os.path.join("Data", "upload", filename)
        if os.path.exists(filepath):
            if os.name == "nt":
                os.startfile(filepath)
            elif os.name == "posix":
                subprocess.call(
                    ("open", filepath)
                    if sys.platform == "darwin"
                    else ("xdg-open", filepath)
                )
        else:
            messagebox.showerror("Error", "El archivo no se encuentra.")

    def download_file(self, filename):
        filepath = os.path.join("Data", "upload", filename)
        if os.path.exists(filepath):
            save_path = filedialog.asksaveasfilename(defaultextension="*.*", initialfile=filename)
            if save_path:
                with open(filepath, 'rb') as f_src:
                    with open(save_path, 'wb') as f_dest:
                        f_dest.write(f_src.read())
                messagebox.showinfo("Resultado", f"Archivo {filename} descargado con éxito.")
        else:
            messagebox.showerror("Error", "El archivo no se encuentra.")

    def delete_all_files(self):
        folder = os.path.join("Data", "upload")
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            messagebox.showinfo("Resultado", "Todos los archivos han sido eliminados.")
            self.update_file_list()
        else:
            messagebox.showerror("Error", "La carpeta no existe.")

if __name__ == "__main__":
    app = FileServerApp()
    app.mainloop()
