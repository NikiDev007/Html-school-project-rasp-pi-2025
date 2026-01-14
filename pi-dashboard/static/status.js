function fetchPiStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {

            document.getElementById('temp-value').textContent = data.temperature + ' °C';

            document.getElementById('cpu-value').textContent = data.cpu_percent + '%';

            document.getElementById('cpu-bar').style.width = data.cpu_percent + '%';

            document.getElementById('ram-value').textContent = data.ram_percent + '%';

            document.getElementById('ram-bar').style.width = data.ram_percent + '%';

            document.getElementById('uptime-value').textContent = data.uptime;

            document.getElementById('status-message').textContent = data.message;
        })
        .catch(error => {
            document.getElementById('status-message').textContent = 'Fehler beim Abrufen der Daten:';
            console.error('Fetch error:', error);
        });
}

fetchPiStatus();
setInterval(fetchPiStatus, 5000);

function fetchSimulatedDisk() {
    fetch('/api/storage_disc_info')
        .then(response => response.json())
        .then(data => {
            const used = Object.values(data).reduce((a, b) => a + b, 0);
            const total = 250;
            const percent = Math.round((used / total) * 100);

            document.getElementById('disk-value').textContent = percent + '%';
            document.getElementById('disk-bar').style.width = percent + '%';
            document.getElementById('disk-used').textContent = used + ' GB';
            document.getElementById('disk-total').textContent = total + ' GB';
        });
}

fetchSimulatedDisk();