import subprocess
import socket
from flask import Flask, render_template
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

PI_LIST = [
    {"name": "angatu", "ip": "10.36.15.28"},
    {"name": "teriva", "ip": "10.36.15.27"},
    {"name": "Angá", "ip": "10.36.15.26"},
    {"name": "guarani", "ip": "10.36.15.25"},
    {"name": "tupi", "ip": "10.36.15.24"},
    {"name": "saojorge", "ip": "10.36.15.23"},
    {"name": "saomiguel", "ip": "10.36.15.22"},
    {"name": "ilhaterceira", "ip": "10.36.15.21"},
    {"name": "pico", "ip": "10.36.15.20"},
    {"name": "graciosa1", "ip": "10.36.15.19"},
    {"name": "graciosa2", "ip": "10.36.15.18"},
    {"name": "flores1", "ip": "10.36.15.17"},
    {"name": "flores2", "ip": "10.36.15.16"},
    {"name": "faial1", "ip": "10.36.15.15"},
    {"name": "corvo1", "ip": "10.36.15.14"},
    {"name": "corvo2", "ip": "10.36.15.13"},
    {"name": "santamaria1", "ip": "10.36.15.12"},
    {"name": "santamaria2", "ip": "10.36.15.11"},
    {"name": "RSP-COM-01", "ip": "10.36.15.7"},
    {"name": "RSP-MKT-01", "ip": "10.36.15.5"},
    {"name": "RSP-RES-01", "ip": "10.36.15.3"},
    {"name": "RSP-REV-01", "ip": "10.36.15.4"},
    {"name": "RSP-REC-01", "ip": "10.36.15.2"},
    {"name": "RSP-SGE-01", "ip": "10.36.15.6"},
    {"name": "RSP-TIC-01", "ip": "10.36.15.1"},
    {"name": "RSP-TIC-03", "ip": "10.36.15.33"},
    {"name": "RSP-TIC-04", "ip": "10.36.15.34"},
    {"name": "RP-THI-01", "ip": "10.36.15.29"},
    {"name": "RP-TAS-01", "ip": "10.36.15.30"},
    {"name": "RP-CEH-01", "ip": "10.36.15.31"}
]

def check_port(ip, port=22, timeout=2):
    """Verifica se uma porta específica está respondendo"""
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except:
        return False

def check_pi_status(pi):
    """Verifica o status usando múltiplos métodos"""
    ip = pi["ip"]
    
    # Tentativa 1: Ping básico
    try:
        ping_result = subprocess.run(['ping', '-c', '1', '-W', '1', ip],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL).returncode == 0
        if ping_result:
            return True
    except:
        pass
    
    # Tentativa 2: Verificação de porta SSH (22)
    if check_port(ip, 22):
        return True
        
    # Tentativa 3: Verificação de porta alternativa (opcional)
    # if check_port(ip, 80):  # Verifica porta HTTP
    #     return True
        
    return False

@app.route('/')
def dashboard():
    pi_status = []
    
    # Usando ThreadPool para verificar em paralelo
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(check_pi_status, PI_LIST))
    
    for pi, status in zip(PI_LIST, results):
        if pi["ip"]:  # Só mostra se tiver IP definido
            pi_status.append({
                "name": pi["name"],
                "ip": pi["ip"],
                "status": "Online" if status else "Offline"
            })
    
    return render_template('dashboard.html', pi_status=pi_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)