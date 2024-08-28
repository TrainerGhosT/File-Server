from Server.core.server import start_server
from Layout.ui.app import FileServerApp
import threading

def run_server():
    start_server()

def run_ui():
    app = FileServerApp()
    app.mainloop()

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    run_ui()
    
    #para cerrar sever cuando se cierra el ui
    print("Cerrando la aplicación...")
