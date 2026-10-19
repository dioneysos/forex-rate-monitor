import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from rate_fetcher import RateFetcher
from alert_manager import AlertManager
from db import RateDB

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

fetcher = RateFetcher()
alert_mgr = AlertManager()
db = RateDB()
scheduler = AsyncIOScheduler()
connected_clients: list[WebSocket] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(poll_rates, 'interval', seconds=30)
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(title="Forex Rate Monitor", lifespan=lifespan)

async def poll_rates():
    rates = await fetcher.fetch_all()
    db.save(rates)
    alerts = alert_mgr.check(rates)
    for alert in alerts:
        log.warning(f"ALERT: {alert}")
        await alert_mgr.notify(alert)
    message = {"rates": rates, "alerts": [str(a) for a in alerts]}
    for client in connected_clients[:]:
        try:
            await client.send_json(message)
        except Exception:
            connected_clients.remove(client)

@app.websocket("/ws/rates")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

@app.get("/api/rates")
async def get_rates():
    return fetcher.last_rates

@app.get("/api/history/{pair}")
async def get_history(pair: str, limit: int = 100):
    return db.get_history(pair, limit)