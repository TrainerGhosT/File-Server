import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Client.client import send_request, upload_file

class FileServerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Server Client")
        self.geometry("500x400")
        self.configure(bg='black')
        self.create_widgets()

    def create_widgets(self):
        upload_button = tk.Button(self, text="Subir Archivo", command=self.upload_file, bg='gray', fg='white')
        upload_button.pack(pady=20)

        view_button = tk.Button(self, text="Ver Archivos", command=self.view_files, bg='gray', fg='white')
        view_button.pack(pady=20)

        self.file_list = tk.Text(self, height=10, width=50, bg='black', fg='white')
        self.file_list.pack(pady=20)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as f:
                content = f.read()
            filename = os.path.basename(file_path)
            response = upload_file(filename, content)
            messagebox.showinfo("Resultado", response)

    def view_files(self):
        request = "LIST_FILES"
        files = send_request(request)
        self.file_list.delete(1.0, tk.END)
        self.file_list.insert(tk.END, files)

if __name__ == "__main__":
    app = FileServerApp()
    app.mainloop()
