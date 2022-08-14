from fastapi import FastAPI
import logging
import logging_loki

logger = logging.getLogger(__file__)

# TODO bug fix for logging_loki library: https://github.com/GreyZmeem/python-logging-loki/issues/17
logging_loki.emitter.LokiEmitter.level_rag = "level"

handler = logging_loki.LokiHandler(
   url="http://loki-stack:3100/loki/api/v1/push",
   tags={"app": "minimal-app"},
   version="1",
)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

app = FastAPI()


@app.get("/")
async def root():
    logger.info("Received request")
    return {"message": "Hello World"}