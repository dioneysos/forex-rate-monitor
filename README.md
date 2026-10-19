# forex-rate-monitor

Real-time foreign exchange rate monitor with WebSocket push and email/webhook alerting. Designed for cross-border trade teams that need to react quickly to rate fluctuations.

## Features
- Real-time rate polling from public FX APIs
- Configurable threshold alerts (e.g. alert when USD/CNY > 7.30)
- WebSocket endpoint for live dashboard
- Email + Webhook (Feishu/Slack) notifications
- Historical rate logging to SQLite

## Quick Start
```bash
pip install -r requirements.txt
cp config.example.yaml config.yaml
# Edit config.yaml with your currency pairs and alert thresholds
python app.py
# Dashboard: http://localhost:8000
# WebSocket: ws://localhost:8000/ws/rates
```

## Tech Stack
- Python 3.10+ / FastAPI
- WebSockets
- SQLite (rate history)
- APScheduler (polling)