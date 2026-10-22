# ApplicationTracker

A Python app that scans Gmail for internship application updates and organizes them in a simple dashboard.

## Features
- Detects application updates from Gmail
- Classifies emails as Applied, Assessment, Interview, Offer, Rejected, or Update
- Search and filter emails in a Streamlit dashboard
- Uses read-only Gmail access

## Tech Stack
- Python
- Gmail API and Google OAuth 2.0
- Streamlit
- Pandas
- Pytest

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/AyushG012/application-tracker.git
   cd application-tracker
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

3. Configure Google Cloud, enable the Gmail API, and create a Desktop OAuth client. Save the downloaded file as `credentials.json` in the project folder.

4. Run the app:
   ```bash
   python -m streamlit run app.py
   ```

## Tests
```bash
python -m pytest -v
```

## Security
Never upload `credentials.json` or `token.json` to GitHub. Both are excluded through `.gitignore`.
