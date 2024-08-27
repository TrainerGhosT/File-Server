import os
from Server.handlers.file import list_files, upload_file

def handle_request(request):
    if request == "LIST_FILES":
        return list_files()
    elif request.startswith("UPLOAD_FILE"):
        filename, content = parse_upload_request(request)
        return upload_file(filename, content)
    else:
        return "Comando no reconocido"

def parse_upload_request(request):
    parts = request.split('|')
    filename = parts[1]
    content = parts[2].encode()
    return filename, content
