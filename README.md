# Diameter Client/Server (Python)

Overview
- This repository contains simple Python scripts demonstrating use of a Diameter library: `diameter_client.py` and `diameter_server.py`.
- This repository contains simple Python scripts demonstrating use of a Diameter library: `diameter_client.py` and `diameter_server.py`.
- Dependencies are listed in `requirements.txt` (no virtualenv is included in this repository).

Requirements
- Python 3.11+
- pip

Quick setup
- Create and activate a virtual environment:

```bash
python3 -m venv env
source env/bin/activate   # Linux / macOS
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

Running
- Start the server (default behavior):

```bash
python diameter_server.py
```

- Run the client which interacts with the server or sends requests to a remote Diameter peer:

```bash
python diameter_client.py
```

Notes
- These scripts are minimal examples — adjust host/port, peer configuration, and dictionaries inside the scripts.
- These scripts are minimal examples — adjust host/port, peer configuration, and dictionaries inside the scripts.
- Activate your virtual environment before running commands so the `diameter` package is available.
- Look in your Python environment's `site-packages/diameter/` for the library implementation and examples of AVP and command definitions.

Development & Contribution
- Open an issue or submit a PR with improvements, examples, or tests.

License
- This project is released under the MIT License. See [LICENSE](LICENSE) for details.

Contact
- If you want help running these scripts or want additional examples, tell me what you want to do and I can add instructions or examples.
