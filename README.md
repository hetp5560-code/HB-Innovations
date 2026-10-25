# HB Innovations

**Tagline:** Innovate Today. Inspire Tomorrow.

HB Innovations is a Flask-based web application with resume-building tools, profile and education management, projects, skills, certificates, photo editing, birthday templates, and a collage maker.

## Technology
- Python and Flask
- SQLite
- HTML, CSS, JavaScript
- Bootstrap

## Run locally (Windows)
1. Install Python.
2. Open this folder in VS Code.
3. Open Terminal in this folder.
4. Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
5. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
6. Run:
   ```powershell
   python app.py
   ```
7. Open `http://127.0.0.1:5000` in your browser.

## GitHub and hosting rename checklist
This ZIP updates the project files and on-site branding. It does **not** change remote accounts by itself.

1. On GitHub, open the existing repository **AutoCVDesigner** → **Settings** → **General** → change Repository name to `HB-Innovations` → **Rename**.
2. In Render (or the current hosting provider), open the existing web service settings and change the service name to `hb-innovations` if that option is available.
3. If the hosting provider's generated URL changes, update any saved links. A custom domain needs its DNS and hosting settings updated separately.
4. Push these updated project files to the renamed GitHub repository so the host deploys the new version.
5. After deployment, test the home page, login, registration, dashboard, resume pages, photo editor, and collage maker.

Keep the existing database and environment variables/backups safe before replacing deployed files. Do not upload `.env`, passwords, API keys, or other secrets to GitHub.
