# TaxiMonitor

Simple taxi monitoring example. This repository contains a central server that receives taxi location updates and multiple taxi clients that send periodic location reports.

**Project Structure**
```
taxi_monitor/
├── __init__.py
├── server.py         # WebSocket server with zone detection and CLI
├── taxi_client.py    # Simulated taxi clients
└── zones.py          # Polygon-based zone definitions
pyproject.toml        # Project metadata and dependencies
README.md             # This file
```

**Requirements**
- Python 3.10+
- Dependencies: websockets, numpy, matplotlib

Installation & Setup (PowerShell)

Clone/navigate to the project and set up a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e .
```

Run the server using the installed console script:

```powershell
taximonitor-server
```

Or run via module invocation:

```powershell
python -m taxi_monitor.server
```

Run the clients (in another terminal):

```powershell
python -m taxi_monitor.taxi_client
```

**Server CLI**

After starting the server you can use the interactive CLI prompt to inspect connected taxis:

- Commands:
  - `l` : show connected taxis
  - `z <TAXI_ID>` : show latitude, longitude, and current zone
  - `exit` : stop the CLI (server remains until Ctrl+C)

**Troubleshooting**

- Port in use: If you get an error binding to `0.0.0.0:64000`, another process is using the port. On Windows run:

```powershell
Get-NetTCPConnection -LocalPort 64000 | Select-Object OwningProcess, State
Stop-Process -Id <PID> -Force
```

- Keepalive ping timeouts: If you see `keepalive ping timeout` errors, the server will retry and you can increase the server-side `ping_timeout` in `server.py`. The project already increases `ping_interval`/`ping_timeout` to reduce false timeouts.

- JSON / field mismatches: The server expects messages with keys `id`, `latitude`, and `longitude` (from `taxi_client.py`). If you changed the keys, ensure both client and server match.

**Notes**

- The server attempts safe sends to avoid exceptions when clients disconnect unexpectedly. If you need more verbose logs, enable additional prints in `server.py`.

**License**

GNU General Public License v3 (GPL-3.0-or-later)
