import os
import uvicorn

if __name__ == "__main__":
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    # Must bind to 0.0.0.0 to be accessible externally
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)