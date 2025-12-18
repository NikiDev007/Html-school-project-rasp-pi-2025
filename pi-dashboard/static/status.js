function fetchPiStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {

            document.getElementById('temp-value').textContent = data.temperature + ' °C';
            
            document.getElementById('cpu-value').textContent = data.cpu_percent + '%';

            document.getElementById('cpu-bar').style.width = data.cpu_percent + '%';

            document.getElementById('ram-value').textContent = data.ram_percent + '%';

            document.getElementById('ram-bar').style.width = data.ram_percent + '%';

            document.getElementById('disk-value').textContent = data.disk_percent + '%';
            document.getElementById('disk-bar').style.width = data.disk_percent + '%';
            document.getElementById('disk-used').textContent = data.disk_used;
            document.getElementById('disk-total').textContent = data.disk_total;
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