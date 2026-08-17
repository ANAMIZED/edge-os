"""Edge OS FastAPI application."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from edge_os import __version__
except Exception:
    __version__ = "0.1.0"

app = FastAPI(
    title="Edge OS",
    description="Autonomous Agentic Operating System for RWA perpetual futures arbitrage.",
    version=__version__,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "edge-os", "version": __version__}


@app.get("/v1/status")
def status():
    return {
        "service": "edge-os",
        "version": __version__,
        "surfaces": ["cli", "sdk", "api", "mcp", "workflows"],
    }


@app.post("/v1/scan")
def scan():
    """Offline mock funding scan."""
    return {
        "opportunities": [],
        "mode": "mock",
        "message": "Offline mock scan — wire live venues for production.",
    }


@app.post("/v1/workflows/funding-arb")
def funding_arb_workflow(goal: str = "scan-and-size"):
    try:
        from edge_os.workflows import run_funding_arb_workflow

        return run_funding_arb_workflow(goal=goal)
    except Exception as e:
        return {"error": str(e), "mode": "mock"}


def run():
    import uvicorn

    uvicorn.run("edge_os.api.main:app", host="0.0.0.0", port=8080, reload=False)


if __name__ == "__main__":
    run()
