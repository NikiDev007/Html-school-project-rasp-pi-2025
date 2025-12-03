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


@app.route('/api/status')
def status_api():

    temp_raw = get_system_info(
        ['cat', '/sys/class/thermal/thermal_zone0/temp'])
    cpu_temp = round(int(temp_raw) / 1000, 1) if temp_raw.isdigit() else "N/A"

    uptime = get_system_info(['uptime', '-p'])

    free_output = get_system_info(['free', '-m'])
    ram_percent = parse_ram_usage(ram_output)

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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
