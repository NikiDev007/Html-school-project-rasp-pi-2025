import psutil
from flask import Flask, jsonify, render_template
import platform
import time
import sqlite3
import threading
import random

app = Flask(__name__)

DATABASE = 'system_metrics.db'


def get_external_ip():
    if platform.system() != 'Linux':
        # Simulierter Wert für lokale Tests
        return "84.142.XXX.XXX (Simuliert)"
    try:
        import subprocess
        result = subprocess.run(['curl', '-s', 'ifconfig.me'],
                                capture_output=True, text=True, check=True, timeout=5)
        return result.stdout.strip()
    except Exception:
        return "Abruf fehlgeschlagen"


def get_network_details():
    # psutil ist plattformunabhängig, aber die Abfrage nach Gateway und DNS ist komplexer.
    # Wir nutzen psutil für IPs, aber behalten die Simulation für Nicht-Linux.
    if platform.system() != 'Linux':
        return {
            "internal_ip": "192.168.1.99 (Simuliert)",
            "gateway": "192.168.1.1 (Simuliert)",
            "dns_servers": ["8.8.8.8 (Simuliert)", "1.1.1.1 (Simuliert)", "192.168.1.1 (Simuliert)"],
            "external_ip": get_external_ip()
        }

    try:
        # psutil: Interne IP-Adressen (Wählt die erste gefundene nicht-loopback IPv4-Adresse)
        internal_ip = "N/A"
        addrs = psutil.net_if_addrs()
        for interface, addresses in addrs.items():
            if interface != 'lo':  # 'lo' ist localhost/Loopback und wird ignoriert
                for addr in addresses:
                    if addr.family == 2:  # 2 bedeutet AF_INET (IPv4)
                        internal_ip = addr.address
                        break
                if internal_ip != "N/A":
                    break

        # psutil: DNS-Server und Gateway sind nicht direkt/einfach per psutil abrufbar.
        # Hier müssten wir entweder:
        # 1. Die alte subprocess-Logik beibehalten (für Linux-spezifische netzwerkdetails)
        # 2. Oder die Details (z.B. DNS) simulieren.
        # Wir behalten hier die alten Werte als Fallback, da es keine direkte psutil-Alternative gibt.

        return {
            "internal_ip": internal_ip,
            # Diese bleiben "N/A" oder müssten über externe Linux-Befehle (mit subprocess) geholt werden,
            # da psutil keinen direkten Zugriff auf DNS/Gateway-Routing-Tabellen bietet.
            "gateway": "Komplex (psutil kann das nicht)",
            "dns_servers": ["Komplex (psutil kann das nicht)"],
            "external_ip": get_external_ip()
        }

    except Exception:
        return {
            "internal_ip": "Fehler beim Abruf (psutil)",
            "gateway": "Fehler beim Abruf",
            "dns_servers": ["Fehler beim Abruf"],
            "external_ip": get_external_ip()
        }

# Datenbank


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            cpu_usage REAL,
            ram_usage REAL,
            cpu_temp REAL
        )
    ''')
    conn.commit()
    conn.close()


def collect_data_loop():
    while True:
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            if platform.system() == "Linux":
                cpu = psutil.cpu_percent(interval=1)
                ram = psutil.virtual_memory().percent
                temps = psutil.sensors_temperatures()
                temp = temps['cpu_thermal'][0].current if 'cpu_thermal' in temps else 0
            else:
                # Simulation für PC (Windows/Mac)
                cpu = random.uniform(15.0, 25.0)
                ram = random.uniform(30.0, 40.0)
                temp = random.uniform(40.0, 50.0)

            # Speichern
            cursor.execute('INSERT INTO metrics (cpu_usage, ram_usage, cpu_temp) VALUES (?, ?, ?)',
                           (round(cpu, 1), round(ram, 1), round(temp, 1)))

            # DB-Pflege: Nur die letzten 50 Einträge behalten, um Überfüllung/Doppler zu vermeiden
            cursor.execute(
                'DELETE FROM metrics WHERE id NOT IN (SELECT id FROM metrics ORDER BY id DESC LIMIT 50)')

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Fehler: {e}")

        time.sleep(10)

# Routen


@app.route('/api/chart-data')
def chart_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT timestamp, cpu_usage, ram_usage, cpu_temp FROM metrics GROUP BY timestamp ORDER BY id DESC LIMIT 20')
    rows = cursor.fetchall()
    conn.close()

    rows.reverse()

    return jsonify({
        "labels": [row[0].split()[1] for row in rows],
        "cpu": [row[1] for row in rows],
        "ram": [row[2] for row in rows],
        "temp": [row[3] for row in rows]
    })


@app.route('/logs')
def view_logs():
    # Logs (tail) muss subprocess behalten, da es eine direkte Interaktion mit der Shell ist
    import subprocess
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
    # --- Windows/Mac Simulation (bleibt unverändert) ---
    if platform.system() != 'Linux':
        current_time = int(time.time())
        temp_sim = 45.0 + (current_time % 10) * 0.1
        cpu_sim = 20.0 + (current_time % 50) / 5
        ram_sim = 30.0 + (current_time % 20) / 2

        return jsonify({
            "temperature": round(temp_sim, 1),
            "cpu_percent": round(cpu_sim, 1),
            "ram_percent": round(ram_sim, 1),
            "disk_percent": 15,
            "disk_total": "250G",
            "disk_used": "37G",
            "uptime": "up 3 hours, 14 minutes",
            "message": "Daten simuliert (Lokaler Test)"
        })

    # --- ECHTE DATEN (NEU: psutil) ---
    try:
        # 1. Temperatur (psutil.sensors_temperatures() ist Linux/Pi-spezifisch)
        # Die Struktur kann variieren, 'cpu_thermal' ist typisch für Pi.
        if psutil.sensors_temperatures():
            temp_list = psutil.sensors_temperatures().get(
                'cpu_thermal', psutil.sensors_temperatures().get('coretemp'))
            cpu_temp = round(temp_list[0].current, 1) if temp_list else "N/A"
        else:
            cpu_temp = "N/A (Sensoren nicht verfügbar)"

        # 1.1 CPU-Auslastung (psutil.cpu_percent())
        cpu_percent = round(psutil.cpu_percent(interval=1), 1)

        # 2. Uptime (sekunden --> formatierte Ausgabe)
        uptime_seconds = time.time() - psutil.boot_time()
        # Formatieren (z.B. in 'up 3 days, 14 hours') ist komplex,
        # wir geben Sekunden zurück oder formatieren es selbst:
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        uptime_str = f"up {days} Tage, {hours} Stunden"

        # 3. RAM-Nutzung (psutil.virtual_memory())
        ram_info = psutil.virtual_memory()
        ram_percent = round(ram_info.percent, 1)

        # 4. Festplattennutzung (psutil.disk_usage('/'))
        disk_info = psutil.disk_usage('/')
        disk_percent = disk_info.percent

        # Formatierung für Total und Used: psutil gibt Bytes zurück, wir formatieren in GB/MB.
        def format_bytes(bytes_value):
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if bytes_value < 1024.0:
                    return f"{bytes_value:.1f}{unit}"
                bytes_value /= 1024.0
            return f"{bytes_value:.1f}TB"  # Für extrem große Platten

        disk_total = format_bytes(disk_info.total)
        disk_used = format_bytes(disk_info.used)

        return jsonify({
            "temperature": cpu_temp,
            "cpu_percent": cpu_percent,
            "ram_percent": ram_percent,
            "disk_percent": disk_percent,
            "disk_total": disk_total,
            "disk_used": disk_used,
            "uptime": uptime_str,
            "message": "Daten erfolgreich abgerufen mit psutil"
        })
    except Exception as e:
        return jsonify({
            "error": "Fehler beim Abrufen der Systemdaten mit psutil",
            "details": str(e)
        }), 500


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/cpu-info')
def cpu_info():
    return render_template('cpu_info.html')


@app.route('/cpu-temp-info')
def cpu_temp_info():
    return render_template('cpu_temp_info.html')


@app.route('/ram-info')
def ram_info():
    return render_template('ram_info.html')


if __name__ == '__main__':
    init_db()
    import os
    if os.environ.get('Werkzeug_Run_Main'):
        data_thread = threading.Thread(target=collect_data_loop, daemon=True)
        data_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True)
