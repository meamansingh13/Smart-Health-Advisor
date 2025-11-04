# How to run Smart Health Advisor (Windows / PowerShell)

This guide helps you set up and run the project locally on Windows using PowerShell. It covers creating/activating a virtual environment, installing dependencies, configuring the `.env` file (including the optional `ALTERNATE_MEDICINE_API` key), and running the app and a quick-check script.

Prerequisites
- Python 3.10+ installed and on PATH
- Git (optional)

Quick checklist
1. Create/activate virtual environment
2. Install dependencies
3. Copy `.env.example` to `.env` and fill any keys you want (optional: `ALTERNATE_MEDICINE_API`)
4. Run the app: `python main.py`
5. Open your browser to `http://127.0.0.1:5000/chat`

Commands (PowerShell)

1) Create a venv (only if you don't already have one):

```powershell
cd "D:\7TH SEM Smart Health Advisor"
python -m venv .venv
```

2) Activate the venv (PowerShell):

```powershell
& "${PWD}\.venv\Scripts\Activate.ps1"
# or if you prefer, absolute path similar to what's shown in your terminal
& "D:/7TH SEM Smart Health Advisor/.venv/Scripts/Activate.ps1"
```

3) Install dependencies:

```powershell
pip install -r "D:\7TH SEM Smart Health Advisor\requirements.txt"
```

4) Add environment variables

- Copy `.env.example` to `.env` and edit as needed. At minimum you should set a `FLASK_SECRET_KEY` for sessions. If you want provider-based priced alternatives, set `ALTERNATE_MEDICINE_API` to your provider API key. Optionally set `ALTERNATE_MEDICINE_ENDPOINT` to your provider endpoint.

PowerShell example:

```powershell
cd "D:\7TH SEM Smart Health Advisor"
copy .env.example .env
# Then open .env in an editor and paste your values, or use set-content to write lines (not recommended for secrets)
notepad .env
```

Add lines like (do not commit this file):

```
ALTERNATE_MEDICINE_API=your_provider_api_key_here
ALTERNATE_MEDICINE_ENDPOINT=https://api.yourprovider.example/search
FLASK_SECRET_KEY=change_this_to_a_real_secret
```

5) Start the app (development mode):

```powershell
python "D:\7TH SEM Smart Health Advisor\main.py"
```

By default Flask runs on http://127.0.0.1:5000. Open your browser and visit:

- Chat / alternate medicine UI: http://127.0.0.1:5000/chat
- Home / symptom predictor: http://127.0.0.1:5000/

6) Run the quick-check script (optional)

This script exercises the local alternatives logic and prints sample results.

```powershell
python "D:\7TH SEM Smart Health Advisor\scripts\check_alternatives.py"
```

Notes & troubleshooting
- If you see a scikit-learn unpickle version warning (from loading `models/svc.pkl`), it means the pickle was created with a different scikit-learn version. It may still work but could produce inconsistent results. To avoid the warning either:
  - install the scikit-learn version used to create the pickle (see project history), or
  - retrain and repickle the model with your local scikit-learn version.

- If the `ALTERNATE_MEDICINE_API` is not set, the app will use the bundled dataset `datasets/medications.csv` and return dataset-based alternatives (no prices).

- If you set `ALTERNATE_MEDICINE_API`, the app will attempt to call the provider endpoint (default placeholder is `https://api.medalternatives.example/search` or whatever you set in `ALTERNATE_MEDICINE_ENDPOINT`). The app sends the API key in a Bearer Authorization header. Make sure the provider uses that scheme or adapt `main.py` accordingly.

- If you get network/timeouts when calling an external provider, the app falls back to local dataset suggestions.

Security
- Never commit your `.env` file to source control. Keep API keys private.

Next steps (optional)
- If you want me to wire up a specific medicine-pricing provider, share the API docs or an example response and I will implement parsing and show prices/links in the UI.
- Add unit tests for the alternate-medicine helpers and endpoint (I can add `pytest` if you'd like).

If anything breaks while following these steps, paste the terminal output here and I'll help debug it.
