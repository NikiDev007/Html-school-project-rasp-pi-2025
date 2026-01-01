# 🚀 PiStatus Dashboard

Ein modernes, webbasiertes Monitoring-Dashboard für den Raspberry Pi. Dieses Projekt visualisiert Systemdaten wie CPU-Last, Arbeitsspeicher, Temperatur und Festplattenbelegung in Echtzeit.

---

## 🏁 Schnellstart-Anleitung

Um das Projekt ohne manuelle Konsolen-Eingaben zu testen, folgen Sie bitte diesen Schritten:

1. **Vorbereitung:** Stellen Sie sicher, dass **Python** installiert ist.
2. **Start:** Klicken Sie doppelt auf die Datei **`Schnellstart.Ink`** im Hauptordner.
3. **Automatik:** Die Datei installiert fehlende Bibliotheken (`flask`, `psutil`), startet den Server und öffnet automatisch Ihren Browser auf `http://127.0.0.1:5000`.
4. **Beenden:** Drücken Sie im Konsolenfenster **STRG + C** oder schließen Sie das Fenster.

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
