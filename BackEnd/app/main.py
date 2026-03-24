from fastapi import FastAPI

app = FastAPI()

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "ok"}

