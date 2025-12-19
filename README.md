# 🏎️ PIT STOP: F1 Strategy & Telemetry Analytics

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-blue?style=for-the-badge&logo=docker&logoColor=white)
![FastF1](https://img.shields.io/badge/Data-FastF1-red?style=for-the-badge)

**PIT STOP** is a full-stack data analytics web application designed to simulate Formula 1 race strategies and visualize complex driver telemetry. Built with a **Flask** backend and the **FastF1 API**, it leverages **Machine Learning** to model tire degradation and provides interactive tools for head-to-head driver comparisons.

---

## 🚀 Key Features

### 1. 🧠 Predictive Strategy Simulator
Uses a **Linear Regression** model (Scikit-Learn) to predict race outcomes based on historical tire data.
- **Race Time Prediction:** Estimates total race time and tire degradation slope.
- **Pit Window Logic:** Recommends the optimal lap to pit based on 1-stop or 2-stop strategies.
- **Dynamic Track Mapping:** Generates circuit layouts using X/Y coordinates from qualifying telemetry.

### 2. 📊 Telemetry Dashboard
A comparative tool for detailed driver analysis (e.g., *Verstappen vs. Hamilton*).
- **Speed Traces:** Interactive line charts showing speed vs. track distance to analyze braking points and cornering speeds.
- **Race Pace Analysis:** Scatter plots comparing lap-by-lap consistency and identifying tire drop-off points.
- **Session Metadata:** Automated retrieval of race winner statistics and team details.

---

## 🛠️ Tech Stack & Tools

### Core Frameworks
* **Backend:** Python 3.11, Flask 3.0
* **Frontend:** HTML5, Jinja2 Templating, Bootstrap 5, Custom CSS
* **Containerization:** Docker, Docker Compose

### Data Science & Libraries
* **[FastF1](https://github.com/theOehrly/Fast-F1):** For retrieving official timing, telemetry, and session data.
* **Pandas & NumPy:** For data manipulation, cleaning, and time-series resampling.
* **Scikit-Learn:** For the Linear Regression models used in strategy prediction.
* **Plotly:** For generating interactive, responsive charts (JSON serialization).

---

## 📂 Project Structure

```text
pit_stop/
├── app.py                  # Main application entry point & route controller
├── Dockerfile              # Production-ready Docker image configuration
├── docker-compose.yml      # Service orchestration & volume mapping
├── requirements.txt        # List of Python dependencies
├── cache/                  # Persistent storage for FastF1 API data
├── utils/
│   ├── __init__.py
│   └── f1_data.py          # ETL pipeline, ML logic & Helper functions
├── static/
│   ├── css/
│   │   └── style.css       # Custom F1-themed dark mode styling
│   └── js/
└── templates/              # Jinja2 HTML Templates
    ├── base.html           # Master layout
    ├── home.html           # Landing page
    ├── simulator.html      # Strategy input & visualization page
    └── telemetry.html      # Driver comparison dashboard