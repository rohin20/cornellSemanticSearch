from main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,  # Adjust based on your server's CPU cores
        log_level="info",
        access_log=True,
    ) 