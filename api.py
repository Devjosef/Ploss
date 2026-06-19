#!/usr/bin/env python3

import asyncio
import json
import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict

from core.storage import StorageManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ploss_api")

db = StorageManager()
templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(_: FastAPI):
    db.init_storage()
    yield
    if hasattr(db, "close"):
        db.close()

app = FastAPI(
    title="Ploss API",
    description="Continuous network diagnostics API",
    version="1.0.0",
    lifespan=lifespan
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info("%s %s | Status: %s | %.2fms", request.method, request.url.path, response.status_code, process_time)
    return response


class Metric(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    timestamp: str
    target: str
    summary: str
    status_flag: str
    latency_ms: Optional[float] = None
    loss_pct: Optional[float] = None
    jitter_ms: Optional[float] = None


class Incident(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    timestamp: str
    target: str
    structural_fault_summary: str
    bottleneck_hop: Optional[int] = None
    bottleneck_host: Optional[str] = None
    bottleneck_loss_pct: Optional[float] = None


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/partials/metrics", response_class=HTMLResponse)
def partial_metrics(request: Request, target: Optional[str] = None, limit: int = 40):
    rows = db.get_metrics_timeline(target=target, limit=limit)
    return templates.TemplateResponse("partials/metrics_rows.html", {"request": request, "rows": rows})


@app.get("/partials/engine", response_class=HTMLResponse)
def partial_engine(request: Request, limit: int = 1):
    incidents = db.get_all_incidents(limit=limit)
    incident = incidents[0] if incidents else None
    return templates.TemplateResponse("partials/incident_engine.html", {"request": request, "incident": incident})


@app.get("/partials/route/{incident_id}", response_class=HTMLResponse)
def partial_route(request: Request, incident_id: int):
    row = db.get_incident(incident_id)
    if not row:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")

    raw = json.loads(row[7]) if row[7] else {}
    hops = raw.get("hops", [])
    analysis = raw.get("analyzer", {}) or raw.get("analysis", {})
    return templates.TemplateResponse("partials/route_path.html", {"request": request, "hops": hops, "analysis": analysis})


@app.get("/metrics", response_model=List[Metric])
def get_metrics(target: Optional[str] = None, limit: int = 100):
    rows = db.get_metrics_timeline(target=target, limit=limit)
    return [
        {
            "id": r[0],
            "timestamp": r[1],
            "target": r[2],
            "summary": r[3],
            "status_flag": r[4],
            "latency_ms": r[5],
            "loss_pct": r[6],
            "jitter_ms": r[7],
        }
        for r in rows
    ]


@app.get("/incidents", response_model=List[Incident])
def get_incidents(limit: int = 100):
    rows = db.get_all_incidents(limit=limit)
    return [
        {
            "id": r[0],
            "timestamp": r[1],
            "target": r[2],
            "structural_fault_summary": r[3],
            "bottleneck_hop": r[4],
            "bottleneck_host": r[5],
            "bottleneck_loss_pct": r[6],
        }
        for r in rows
    ]


@app.get("/incident/{incident_id}", response_model=Incident)
def get_incident(incident_id: int):
    row = db.get_incident(incident_id)
    if not row:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
    return {
        "id": row[0],
        "timestamp": row[1],
        "target": row[2],
        "structural_fault_summary": row[3],
        "bottleneck_hop": row[4],
        "bottleneck_host": row[5],
        "bottleneck_loss_pct": row[6],
    }


@app.post("/report/{incident_id}")
async def generate_report(incident_id: int):
    row = db.get_incident(incident_id)
    if not row:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")

    report_data = {
        "id": row[0],
        "timestamp": row[1],
        "target": row[2],
        "summary": row[3],
        "evidence": {
            "bottleneck_hop": row[4],
            "bottleneck_host": row[5],
            "bottleneck_loss_pct": row[6]
        },
        "raw_runlog": json.loads(row[7]) if row[7] else {}
    }

    report_path = f"ploss_report_incident_{incident_id}.json"
    await asyncio.to_thread(Path(report_path).write_text, json.dumps(report_data, indent=2))

    return {
        "message": f"Report saved to: {report_path}",
        "path": report_path,
        "incident_id": incident_id
    }


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)