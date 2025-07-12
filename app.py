import subprocess
import socket
from flask import Flask, render_template
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

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
    {"name": "RSP-MKT-01", "ip": "10.36.15.7"},
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

PRINTER_LIST = [
    {"name": "IMP-TIC-PB01", "location": "TIC", "ip": "10.35.0.91"},
    {"name": "IMP-PROP-CL01", "location": "TIC", "ip": "10.35.0.90"},
    {"name": "IMP-TELL-PB01", "location": "Vacation", "ip": "10.35.0.40"},
    {"name": "IMP-OND-CL01", "location": "Ondas", "ip": "10.35.0.77"},
    {"name": "IMP-NUT-CL01", "location": "Nutrição", "ip": "192.168.7.104"},
    {"name": "IMP-COZ-CL01", "location": "Cozinha", "ip": "10.35.0.62"},
    {"name": "IMP-CEN-CL01", "location": "Central do Hospede", "ip": "10.35.0.60"},
    {"name": "IMP-MAR-CL01", "location": "ADM", "ip": "192.168.7.107"},
    {"name": "IMP-SPA-PB01", "location": "SPA", "ip": "10.35.0.70"},
    {"name": "IMP-GOV-PB01", "location": "Governança", "ip": "10.35.0.65"},
    {"name": "IMP-OND-CL02", "location": "Vitória", "ip": "192.168.7.110"},
    {"name": "IMP-MAN-PB01", "location": "Manutenção", "ip": "10.35.0.66"},
    {"name": "IMP-CIE-A3", "location": "CIE", "ip": "10.35.0.50"},
    {"name": "IMP-MUL-PB01", "location": "Multipropriedade", "ip": "10.35.0.44"},
    {"name": "IMP-CIE-PB01", "location": "CIE", "ip": "10.35.0.51"},
    {"name": "IMP-RECR-CL01", "location": "Entretenimento", "ip": "192.168.7.115"},
    {"name": "IMP-VACCLUB-BACK", "location": "Vacation", "ip": "192.168.7.116"},
    {"name": "IMP-CPDA-PB01", "location": "CPDA", "ip": "10.35.0.52"},
    {"name": "IMP-ALM-PB01", "location": "Almoxarifado", "ip": "192.168.7.118"},
    {"name": "IMP-OBR-PB01", "location": "Manutenção", "ip": "10.35.0.68"},
    {"name": "IMP-MKT-CL01", "location": "Marketing", "ip": "10.35.0.34"},
    {"name": "IMP-EVE-PB01", "location": "Eventos", "ip": "10.35.0.55"},
    {"name": "IMP-RES-PB01", "location": "Reservas", "ip": "10.35.0.33"},
    {"name": "IMP-FAT-PB01", "location": "Faturamento", "ip": "10.35.0.20"},
    {"name": "IMP-FAT-PB02", "location": "Faturamento", "ip": "10.35.0.21"},
    {"name": "IMP-REC-PB01", "location": "Recepção", "ip": "10.35.0.30"},
    {"name": "IMP-RCP-PB01", "location": "Transporte", "ip": "10.35.0.25"},
    {"name": "IMP-MED-PB01", "location": "Médico", "ip": "192.168.7.127"},
    {"name": "IMP-ADM1-PB01", "location": "ADM", "ip": "10.35.0.10"},
    {"name": "IMP-RH-PB01", "location": "RH", "ip": "10.35.0.23"},
    {"name": "IMP-ENG-CL01", "location": "ADM", "ip": "10.35.0.11"},
    {"name": "IMP-NAZ-PB01", "location": "ADM", "ip": "10.35.0.13"},
    {"name": "IMP-PRE-CL01", "location": "ADM", "ip": "10.35.0.14"},
    {"name": "IMP-FIN-PB01", "location": "Financeiro", "ip": "10.35.0.22"},
    {"name": "IMP-CPDA-PB02", "location": "CPDA", "ip": "10.35.0.53"},
    {"name": "IMP-ROUP-PB01", "location": "Rouparia", "ip": "192.168.7.135"},
    {"name": "IMP-ACA-PB01", "location": "ACADEMIA", "ip": "192.168.7.136"},
    {"name": "IMP-VACCLUB-FRENTE", "location": "Vacation", "ip": "10.35.0.42"},
    {"name": "IMP-BOU-PB01", "location": "Boutique", "ip": "10.35.0.32"},
    {"name": "IMP-COZ-PB02", "location": "Cozinha", "ip": "10.35.0.63"},
    {"name": "IMP-MAN-PB02", "location": "Manutenção", "ip": "10.35.0.67"},
    {"name": "IMP-REC-PB02", "location": "Recepção", "ip": "10.35.0.31"},
    {"name": "IMP-SGE-PB01", "location": "Serviços Gerais", "ip": "10.35.0.69"},
    {"name": "IMP-PAD-PB01", "location": "Padaria", "ip": "10.35.0.64"},
    {"name": "IMP-VACCLUB-FUNDO-PB01", "location": "Vacation", "ip": "10.35.0.41"},
    {"name": "IMP-VEBC-01", "location": "Recepção Estaleirinho", "ip": "192.168.104.65"},
    {"name": "IMP-GEBC-01", "location": "Gerencia Estaleirinho", "ip": "192.168.104.67"},
    {"name": "IMP-ADMBC-PB01", "location": "Sala de Vendas 2 - MP - ADM", "ip": "192.168.122.23"},
    {"name": "IMP-GEMP-PB01", "location": "Sala de vendas 2 - MP - GERENCIA", "ip": "192.168.122.22"},
    {"name": "IMP-RECMP-PB01", "location": "Sala de vendas 2 - RECEPÇÃO", "ip": "192.168.122.21"},
    {"name": "IMP-ADMAVB-PB01", "location": "Sala de vendas Avenida Brasil - ADM", "ip": "192.168.125.23"}
]

def check_port(ip, port=22, timeout=2):
    """Verifica se uma porta específica está respondendo"""
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except:
        return False

def check_device_status(device):
    """Verifica o status de um dispositivo (Raspberry Pi ou impressora)"""
    ip = device["ip"]
    
    # Tentativa 1: Ping básico
    try:
        ping_result = subprocess.run(['ping', '-c', '1', '-W', '1', ip],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL).returncode == 0
        if ping_result:
            return True
    except:
        pass
    
    # Tentativa 2: Verificação de porta (9100 para impressoras, 22 para Raspberry Pi)
    port = 9100 if "IMP-" in device["name"] else 22
    if check_port(ip, port):
        return True
        
    return False

@app.route('/')
def dashboard():
    pi_status = []
    printer_status = []
    update_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Verificar status dos Raspberry Pi em paralelo
    with ThreadPoolExecutor(max_workers=20) as executor:
        pi_results = list(executor.map(check_device_status, PI_LIST))
    
    for pi, status in zip(PI_LIST, pi_results):
        if pi["ip"]:  # Só mostra se tiver IP definido
            pi_status.append({
                "name": pi["name"],
                "ip": pi["ip"],
                "status": "Online" if status else "Offline"
            })
    
    # Verificar status das impressoras em paralelo
    with ThreadPoolExecutor(max_workers=20) as executor:
        printer_results = list(executor.map(check_device_status, PRINTER_LIST))
    
    for printer, status in zip(PRINTER_LIST, printer_results):
        if printer["ip"]:  # Só mostra se tiver IP definido
            printer_status.append({
                "name": printer["name"],
                "location": printer["location"],
                "ip": printer["ip"],
                "status": "Online" if status else "Offline"
            })
    
    return render_template('dashboard.html', 
                         pi_status=pi_status,
                         printer_status=printer_status,
                         update_time=update_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)