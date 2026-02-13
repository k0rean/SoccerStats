# SoccerStats Web Dashboard

A modern Streamlit dashboard for soccer statistics visualization.

## Features

- League selection (Premier League, La Liga, Bundesliga, Serie A, etc.)
- Team performance analysis
- Goals, corners, fouls, cards visualizations
- Home/Away split statistics
- Interactive charts with Plotly

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Docker

```bash
docker build -t soccerstats .
docker run -p 8501:8501 soccerstats
```
