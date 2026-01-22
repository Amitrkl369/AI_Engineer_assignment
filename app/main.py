from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.api.v1.extract import router as extract_router

app = FastAPI(title="Marksheet Extraction API")
app.include_router(extract_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Marksheet Extraction API. Use /api/v1/extract"}

@app.get("/frontend")
def get_frontend():
    return FileResponse("frontend_interactive.html", media_type="text/html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
