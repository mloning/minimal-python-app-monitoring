from fastapi import FastAPI
import logging.config
import logging

_LOG_CONFIG = {
   "version": 1,
   "disable_existing_loggers" : False,
   "handlers" : {
      "console": {
         "class": "logging.StreamHandler",
         "stream": "ext://sys.stdout",
         "formatter": "default",
      },
   },
   "formatters" : {
      "default": {
         "()": "uvicorn.logging.DefaultFormatter",
         "fmt": "%(asctime)s %(levelprefix)s %(message)s",
         "datefmt": "%Y-%m-%d %H:%M:%S",
         },
      },
   "loggers": {
      "": {"handlers": ["console"], "level": "DEBUG"}
   },
}
logging.config.dictConfig(_LOG_CONFIG)

logger = logging.getLogger()

app = FastAPI()


@app.get("/")
async def root():
   logger.info("Received request")
   message = "Hello World!"
   logger.debug("Created message")
   return {"message": message}