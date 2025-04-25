from main import app
import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use PORT from environment or default to 8000
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        workers=4,  # Adjust based on your server's CPU cores
        log_level="info",
        access_log=True,
    ) 