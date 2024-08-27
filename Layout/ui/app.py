import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Client.client import upload_file, send_request

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

        self.file_list = tk.Listbox(self, height=10, width=50, bg='black', fg='white')
        self.file_list.pack(pady=20)

        self.update_file_list()  # Inicializar la lista de archivos al iniciar

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as f:
                content = f.read()
            filename = os.path.basename(file_path)
            response = upload_file(filename, content)
            messagebox.showinfo("Resultado", response)
            self.update_file_list()  # Actualizar la lista de archivos después de subir uno nuevo

    def update_file_list(self):
        self.file_list.delete(0, tk.END)  # Limpiar la lista de archivos
        request = "LIST_FILES"
        files = send_request(request)
        for file in files.split('\n'):
            self.file_list.insert(tk.END, file)  # Insertar cada archivo en la lista

if __name__ == "__main__":
    app = FileServerApp()
    app.mainloop()
