import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../Data')
UPLOAD_DIR = os.path.join(DATA_DIR, 'upload')
DOWNLOAD_DIR = os.path.join(DATA_DIR, 'download')

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def list_files():
    files = os.listdir(UPLOAD_DIR)
    return '\n'.join(files)

def upload_file(filename, content):
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, 'wb') as f:
        f.write(content)
    return f"Archivo {filename} subido con éxito"
