# fbreaper frontend (renamed)

This repository now uses a rebuilt Next.js App Router frontend named "fbreaper".

Notes:
- In this v0 preview, the Next.js app must live at the project root under `app/` to render. The brand, navigation, and code are for "fbreaper".
- The previous CRA folder `facebook-osint-dashboard/` is deprecated. You can remove it from your repo after installing/downloading.
- To point the UI at your Java backend, set `NEXT_PUBLIC_API_URL` (e.g., http://localhost:8080).

Main Routes:
- `/` — Dashboard home
- `/search` — OSINT search panel
- `/status` — Scraper status
- `/data` — Data viewer
- `/network` — Link analysis
