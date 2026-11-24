# API Dashboard

A command-line dashboard that pulls data from three API endpoints, processes each one, and prints a summary report plus a JSON export.

At the moment each endpoint is simulated by a function that returns a hardcoded dict mirroring the real API response. Swapping in real `requests.get()` calls is a small change (see below).

## Endpoints

| Endpoint | Function | Returns |
|---|---|---|
| `GET /v1/members?city=Nairobi` | `fetch_members()` | List of members with today's stats |
| `GET /v1/weekly-summary` | `fetch_weekly_summary()` | Aggregated step data for the past 7 days across all members |
| `GET /v1/skills/active` | `fetch_active_skills()` | Active SMP skills being taught this week |

## What it does

1. **Fetch** - calls the three `fetch_*` functions and prints a record count for each.
2. **Process** - `process_members`, `process_weekly` and `process_skills` compute the stats (goal hitters, averages, best day, most popular skill, and so on).
3. **Display** - prints a three-section dashboard: member performance, weekly steps (with a text bar chart), and active skills.
4. **Export** - prints a compact summary as JSON.

## Requirements

- Python 
- No third-party packages needed right now 

## Usage

```bash
git clone https://github.com/mawazob/api-dashboard
cd api-dashboard
python dashboard.py
```

Optional: use a virtual environment before installing anything.

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

The daily step goal is set by the `STEP_GOAL` variable near the top of Step 2 (default: `10000`).

## Moving to a real API

Replace the body of each `fetch_*` function with a `requests.get()` call, for example:

```python
import requests

def fetch_members():
    response = requests.get("https://your-api.example.com/v1/members", params={"city": "Nairobi"})
    response.raise_for_status()
    return response.json()
```

## Project structure

```
.
├── dashboard.py        # the script
├── requirements.txt    # dependencies
├── README.md           # this file
└── .gitignore          # files git should skip
```