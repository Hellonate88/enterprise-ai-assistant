from fastapi import FastAPI


app = FastAPI(
    title="Enterprise AI Assistant API",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "running",
        "service": "AI Assistant API"
    }