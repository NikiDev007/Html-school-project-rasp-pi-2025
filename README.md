# 🚀 PiStatus Dashboard

Ein modernes, webbasiertes Monitoring-Dashboard für den Raspberry Pi. Dieses Projekt visualisiert Systemdaten wie CPU-Last, Arbeitsspeicher, Temperatur und Festplattenbelegung in Echtzeit.

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
- Implementierung eines konsistenten Favicon-Systems.
- Erstes CSS-Layout für ein einheitliches Design.

### Phase 2: Backend-Integration (Home-Office)
- Umstieg auf **Flask** als Web-Framework.
- Entwicklung der `app.py` zur Datenbereitstellung.
- Implementierung der `status.js`, um Daten dynamisch (AJAX/Fetch) ohne Seiten-Reload zu laden.

### Phase 3: Optimierung & Performance
- **Refactoring:** Wechsel von `subprocess` zu `psutil` für effizientere und plattformunabhängige Datenabfrage.
- **Datenpersistenz:** Einführung von **SQLite3** zur Aufzeichnung der System-Historie.
- **UI-Finish:** Hinzufügen von Lade-Animationen, Hover-Effekten und Optimierung der Barrierefreiheit.

---

## 💻 Tech-Stack
| Bereich | Technologie |
| :--- | :--- |
| **Backend** | Python 3, Flask, psutil |
| **Datenbank** | SQLite3 |
| **Frontend** | JavaScript (ES6), HTML5, CSS3 (Flexbox & Keyframes) |
| **Tools** | Git/GitHub, Visual Studio Code |

---

## 📂 Projektstruktur
```text
.
├── app.py              # Flask Backend & System-Logik
├── database.db         # SQLite Datenbank für Historie
├── static/             # Statische Dateien
│   ├── css/            # Stylesheets & Animationen
│   ├── js/             # Frontend-Logik (status.js)
│   └── favicon.ico     # Projekt-Icon
└── templates/          # HTML-Templates (index, dashboard, logs, network)
