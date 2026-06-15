import logging
from fastapi import FastAPI
import uvicorn
from routes import book_routes

logging.basicConfig(
    level=logging.DEBUG,
    format= "%(asctime)s | %(levelname)s | %(massage)s", 
    handlers= [logging.StreamHandler(), logging.FileHandler("logs/ app.log")]
)
logger = logging.getLogger(__name__)


app = FastAPI()

app.include_router(book_routes.router, prefix="/books", tags=["books"])



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
