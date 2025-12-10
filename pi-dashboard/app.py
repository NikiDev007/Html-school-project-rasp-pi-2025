import subprocess
from flask import Flask, jsonify, render_template
import platform
import time

app = Flask(__name__)


def get_system_info(command):
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True, timeout=5)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""
    except FileNotFoundError:
        return ""
    except subprocess.TimeoutExpired:
        return ""


def get_external_ip():
    if platform.system() != 'Linux':
        # Simulierter Wert für lokale Tests
        return "84.142.XXX.XXX (Simuliert)"
    try:
        # Hier wird ein Dienst verwendet, der nur die IP-Adresse zurückgibt
        result = subprocess.run(['curl', '-s', 'ifconfig.me'],
                                capture_output=True, text=True, check=True, timeout=5)
        return result.stdout.strip()
    except Exception:
        return "Abruf fehlgeschlagen"


def get_network_details():
    if platform.system() != 'Linux':
        # Simulierte Daten für den Windows/Mac-Test
        return {
            "internal_ip": "192.168.1.99 (Simuliert)",
            "gateway": "192.168.1.1 (Simuliert)",
            "dns_servers": ["8.8.8.8 (Simuliert)", "1.1.1.1 (Simuliert)", "192.168.1.1 (Simuliert)"],
            "external_ip": get_external_ip()
        }

    try:
        # 1. Interne IP-Adresse (Wir verwenden 'hostname -I' für alle IPs)
        internal_ip_raw = get_system_info(['hostname', '-I'])
        # Wählt die erste gefundene IP
        internal_ip = internal_ip_raw.split()[0] if internal_ip_raw else "N/A"

        # 2. Gateway-Adresse (Standard-Router)
        # Sucht in der Routing-Tabelle nach dem Standard-Gateway
        gateway_cmd_output = get_system_info(
            ['ip', 'route', 'show', 'default'])
        gateway = gateway_cmd_output.split(
            ' ')[2] if gateway_cmd_output and 'default via' in gateway_cmd_output else "N/A"

        # 3. DNS-Server (aus resolv.conf)
        dns_raw = get_system_info(['grep', 'nameserver', '/etc/resolv.conf'])
        # Extrahiert die IPs der DNS-Einträge
        dns_servers = [line.split()[1] for line in dns_raw.split(
            '\n') if line and not line.startswith('#')] if dns_raw else ["N/A"]

        return {
            "internal_ip": internal_ip,
            "gateway": gateway,
            "dns_servers": dns_servers,
            "external_ip": get_external_ip()
        }

    except Exception:
        return {
            "internal_ip": "Fehler beim Abruf",
            "gateway": "Fehler beim Abruf",
            "dns_servers": ["Fehler beim Abruf"],
            "external_ip": get_external_ip()
        }


def parse_ram_usage(free_output):
    lines = free_output.split('\n')
    if len(lines) < 2:
        return 0
    parts = lines[1].split()
    if len(parts) >= 4:
        total = int(parts[1])
        used = int(parts[2])
        if total > 0:
            return ((used / total) * 100, 1)
    return 0


def parse_disk_usage(df_output):
    lines = df_output.split('\n')
    if len(lines) < 2:
        return 0, 0, 0
    root_line = [line for line in lines if line.endswith('/')]
    if root_line:
        parts = root_line[0].split()
        if len(parts) >= 5:
            usage_percent = int(parts[4].replace('%', ''))
            total = parts[1]
            used = parts[2]
            return usage_percent, total, used
    return 0, "N/A", "N/A"

# --- Routen ---


@app.route('/logs')
def view_logs():
    try:
        command = ['tail', '-n', '100', '/var/log/syslog']
        result = subprocess.run(
            command, capture_output=True, text=True, check=True)
        log_content = result.stdout
    except subprocess.CalledProcessError as e:
        log_content = f"Fehler beim Abrufen der Logs: {e.stderr}"
    except FileNotFoundError:
        log_content = "Der 'tail'-Befehl wurde nicht gefunden oder die Log-Datei existiert nicht."
    return render_template('logs.html', log_content=log_content)


@app.route('/network')
def network_info():
    details = get_network_details()
    return render_template('network_info.html', details=details)


@app.route('/api/status')
def status_api():
    # --- Windows/Mac Simulation ---
    if platform.system() != 'Linux':
        # Erstelle simulierte, leicht variierende Daten
        current_time = int(time.time())
        temp_sim = 45.0 + (current_time % 10) * 0.1
        ram_sim = 30.0 + (current_time % 20) / 2

        return jsonify({
            "temperature": round(temp_sim, 1),
            "uptime": "up 3 hours, 14 minutes",
            "ram_percent": round(ram_sim, 1),
            "disk_percent": 15,
            "disk_total": "250G",
            "disk_used": "37G",
            "message": "Daten simuliert (Lokaler Test)"
        })

    # --- ECHTE PI-DATEN (nur auf Linux/Pi ausführbar) ---
    try:
        temp_raw = get_system_info(
            ['cat', '/sys/class/thermal/thermal_zone0/temp'])
        cpu_temp = round(int(temp_raw) / 1000,
                         1) if temp_raw and temp_raw.isdigit() else "N/A"

        uptime = get_system_info(['uptime', '-p'])

        free_output = get_system_info(['free', '-m'])
        ram_percent = parse_ram_usage(free_output)

        disk_output = get_system_info(['df', '-h'])
        disk_percent, disk_total, disk_used = parse_disk_usage(disk_output)

        return jsonify({
            "temperature": cpu_temp,
            "uptime": uptime,
            "ram_percent": ram_percent,
            "disk_percent": disk_percent,
            "disk_total": disk_total,
            "disk_used": disk_used,
            "message": "Daten erfolgreich abgerufen"
        })
    except Exception as e:
        return jsonify({
            "error": "Fehler beim Abrufen der Systemdaten",
            "details": str(e)
        }), 500


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
