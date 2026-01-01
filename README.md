# 🚀 PiStatus Dashboard

Ein modernes, webbasiertes Monitoring-Dashboard für den Raspberry Pi. Dieses Projekt visualisiert Systemdaten wie CPU-Last, Arbeitsspeicher, Temperatur und Festplattenbelegung in Echtzeit.

---

## 🏁 Schnellstart-Anleitung

Da das Projekt eine laufende Python-Umgebung benötigt, folgen Sie bitte dieser einfachen Anleitung, um das Dashboard auf Ihrem Rechner zu starten:

### Schritt 1: Das Projekt herunterladen
1. Klicken Sie oben rechts auf der GitHub-Seite auf den grünen Button **"Code"**.
2. Wählen Sie im Menü den Punkt **"Download ZIP"**.
3. Speichern Sie die Datei und entpacken Sie den gesamten Inhalt in einen Ordner Ihrer Wahl.

### Schritt 2: Vorbereitung
Stellen Sie sicher, dass **Python** auf Ihrem System installiert ist. 
*(Falls nicht vorhanden, kann es unter [python.org](https://www.python.org/) heruntergeladen werden).*

### Schritt 3: Das Programm starten
1. Öffnen Sie den entpackten Projektordner.
2. Suchen Sie die Datei **`Start_Dashboard.bat`** im Ordner **`pi-dashboard`**. 
3. **Doppelklicken** Sie auf diese Datei.

### Schritt 4: Automatischer Ablauf
Es öffnet sich ein schwarzes Konsolenfenster. Bitte warten Sie kurz, während das Skript:
- Die benötigten Bibliotheken (`flask`, `psutil`) automatisch installiert.
- Den Server im Hintergrund startet.
- Nach ca. 3 Sekunden **automatisch Ihren Webbrowser** mit der Adresse `http://127.0.0.1:5000` öffnet.

### Schritt 5: Beenden
Um die Begutachtung zu beenden, schließen Sie einfach das Konsolenfenster oder drücken Sie darin die Tasten **STRG + C**.

---

## 📊 Features
- **Echtzeit-Monitoring:** Automatische Aktualisierung der Systemwerte alle 5 Sekunden via Fetch API.
- **Historische Daten:** Speicherung der Werte in einer SQLite3-Datenbank und Visualisierung in Graphen.
- **System-Logs:** Integrierte Ansicht der System-Logs direkt im Browser.
- **Netzwerk-Analyse:** Anzeige von IP-Adresse, Gateway und DNS-Servern.
- **Responsives Design:** Optimiert für Desktop und mobile Endgeräte mit modernen CSS-Animationen.

---

## 🛠 Entwicklung & Meilensteine

### Phase 1: Grundlagen (Schule)
- Erstellung der HTML-Grundstruktur und des Navigationsmenüs.
- Implementierung eines konsistenten Favicon-Systems (Research via SelfHTML).
- Erstes CSS-Layout für ein einheitliches Design.

### Phase 2: Backend-Integration (Home-Office)
- Umstieg auf **Flask** als Web-Framework.
- Entwicklung der `app.py` zur Datenbereitstellung.
- Implementierung der `status.js`, um Daten dynamisch (AJAX/Fetch) ohne Seiten-Reload zu laden.

### Phase 3: Optimierung & Performance
- **Refactoring:** Wechsel von `subprocess` zu **`psutil`** für eine effizientere Datenabfrage.
- **Datenpersistenz:** Einführung von **SQLite3** zur Aufzeichnung der System-Historie.
- **UI-Finish:** Lade-Animationen, Hover-Effekte und klare Trennung von Daten-Boxen.

---

## 💻 Tech-Stack
| Bereich | Technologie |
| :--- | :--- |
| **Backend** | Python 3, Flask, psutil |
| **Datenbank** | SQLite3 |
| **Frontend** | JavaScript (ES6), HTML5, CSS3 |

---

## 📂 Projektstruktur
```text
.
├── app.py              # Flask Backend & System-Logik
├── database.db         # SQLite Datenbank für Historie
├── START_DASHBOARD.bat # Windows-Starter (Ein-Klick-Start)
├── static/             # CSS-Styles, JS-Logik und Favicons
└── templates/          # HTML-Seiten (Index, Dashboard, Logs, Network)
