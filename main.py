import logging
from fastapi import FastAPI
import uvicorn

logging.basicConfig(
    level=logging.DEBUG,
    format= "%(asctime)s | %(levelname)s | %(massage)s", 
    handlers= [logging.StreamHandler(), logging.FileHandler("logs/ app.log")]
)
logger = logging.getLogger(__name__)


app = FastAPI()



if __name__ == "__main__":
    uvicorn.run("main:app0", host="127.0.0.1", port=8000, reload=True)
