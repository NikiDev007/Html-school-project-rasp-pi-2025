import subprocess
from flask import Flask, jsonify, render_template

app = Flask(__name__)


def get_system_info(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()


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


# app.py: NUR DIESE FUNKTION ÄNDERN!
@app.route('/api/status')
def status_api():

    # *** SIMULIERTE DATEN FÜR LOKALEN WINDOWS-TEST ***
    # WICHTIG: Wenn du auf den Raspberry Pi wechselst, musst du wieder
    # den Original-Code mit den subprocess.run() Befehlen einfügen!

    return jsonify({
        "temperature": 45.5,                 # Feste Temperatur
        "uptime": "up 3 hours, 14 minutes",  # Feste Laufzeit
        "ram_percent": 35.0,                 # RAM-Auslastung in %
        "disk_percent": 15,                  # Festplattenauslastung in %
        "disk_total": "250G",                # Simulierte Festplattengröße
        "disk_used": "37G",                  # Simulierte Nutzung
        "message": "Daten simuliert (Lokaler Test)"
    })


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
