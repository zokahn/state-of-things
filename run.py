
import uvicorn
import logging
import traceback
from app.main import app

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("Starting the server...")
if __name__ == "__main__":
    try:
        print("Initializing uvicorn...")
        uvicorn.run(app, host="0.0.0.0", port=8002, log_level="debug")
    except Exception as e:
        print(f"An error occurred while starting the server: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        logger.error(f"An error occurred while starting the server: {str(e)}")
        logger.error(traceback.format_exc())
