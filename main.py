import logging
from fastapi import FastAPI
import uvicorn
from routes import book_routes, member_routes, report_routes
from database import db_connection 

logging.basicConfig(
    level=logging.DEBUG,
    format= "%(asctime)s | %(levelname)s | %(message)s", 
    handlers= [logging.StreamHandler(), logging.FileHandler("logs/ app.log")]
)
logger = logging.getLogger(__name__)

db_connection.create_tables()

app = FastAPI()

app.include_router(book_routes.router, prefix="/books", tags=["books"])
app.include_router(member_routes.router, prefix="/members", tags=["members"])
app.include_router(report_routes.router, prefix="/reports", tags=["reports"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
