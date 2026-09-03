from fastapi import FastAPI

app = FastAPI(title="Cairn API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "cairn-api"}
