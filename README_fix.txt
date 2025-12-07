
Project patched for local development (Python 3.10 / 3.11 recommended)

Changes made:
- Switched DATABASES to sqlite3 for zero-config local run.
- Set ALLOWED_HOSTS to ['127.0.0.1','localhost'] and enabled CORS_ALLOW_ALL_ORIGINS for local testing.
- Added requirements.txt with the needed packages.
- Backed up original settings.py to project/settings.py.bak

How to run locally:
1) Create & activate venv (PowerShell):
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # or .venv\Scripts\activate

2) Upgrade pip and install dependencies:
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt

3) Download spaCy model:
   python -m spacy download en_core_web_sm

4) Run migrations and start server:
   python manage.py migrate
   python manage.py runserver

5) In another terminal, run Streamlit frontend if you use it:
   streamlit run streamlit_app/main.py   # or streamlit_app/pages as earlier

Notes:
- If you want to use PostgreSQL again, restore project/settings.py.bak into project/settings.py and configure DB.
- If any package install fails on Python 3.13, switch to Python 3.11 or 3.10.
