from fastapi import FastAPI
import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

app = FastAPI()


@app.get("/")
async def root():
    logger.info("Received request")

    logger.debug()
    return {"message": "Hello World"}