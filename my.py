import os
import time
from flask import Flask, render_template
from io import BytesIO
import base64
from vncdotool import api
import threading
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

app = Flask(__name__)

PI_LIST = [
    # Exemplo:
    # {"name": "Pi1", "ip": "192.168.1.100", "vnc_port": 5900, "vnc_password": "senha"}
]

class VNCScreenshot:
    def __init__(self, host, port, password, timeout=10):
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout
        self.image = None

    def capture(self):
        def _capture():
            try:
                client = api.connect(f"{self.host}:{self.port}", password=self.password)
                self.image = client.captureScreen()
                client.disconnect()
            except Exception as e:
                print(f"Erro VNC: {str(e)}")
                self.image = None

        thread = threading.Thread(target=_capture)
        thread.start()
        thread.join(timeout=self.timeout)
        
        if thread.is_alive():
            return None
        
        return self.image

def capture_vnc_screenshot(pi):
    """Captura screenshot via VNC"""
    try:
        vnc = VNCScreenshot(pi["ip"], pi["vnc_port"], pi["vnc_password"])
        img = vnc.capture()
        
        if img:
            buffered = BytesIO()
            if isinstance(img, Image.Image):  # Se já for PIL Image
                img.save(buffered, format="JPEG", quality=70)
            else:  # Se for outro formato (vncdotool retorna PIL.Image)
                img.save(buffered, format="JPEG", quality=70)
            return f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode()}"
        return None
    except Exception as e:
        print(f"Erro ao capturar {pi['name']}: {str(e)}")
        return None

def check_vnc_connection(pi):
    """Verifica se o VNC está respondendo"""
    try:
        vnc = VNCScreenshot(pi["ip"], pi["vnc_port"], pi["vnc_password"], timeout=5)
        return vnc.capture() is not None
    except:
        return False

@app.route('/')
def dashboard():
    pi_status = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Verifica status via VNC
        online_status = list(executor.map(check_vnc_connection, PI_LIST))
        
        # Captura screenshots paralelamente
        screenshots = {}
        for pi, is_online in zip(PI_LIST, online_status):
            if is_online:
                screenshots[pi["ip"]] = executor.submit(capture_vnc_screenshot, pi)
    
    for pi, is_online in zip(PI_LIST, online_status):
        screenshot = screenshots.get(pi["ip"], None) if is_online else None
        pi_status.append({
            "name": pi["name"],
            "ip": pi["ip"],
            "status": "Online" if is_online else "Offline",
            "screenshot": screenshot.result() if screenshot else None,
            "port": pi["vnc_port"]
        })
    
    return render_template('dashboard_vnc.html', pi_status=pi_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)