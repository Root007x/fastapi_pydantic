from fastapi import FastAPI
import uvicorn
from auth import models
from auth.db import engine
from auth.routes import router


app = FastAPI()


models.Base.metadata.create_all(bind = engine)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app=app, host = "127.0.0.1", port = 5555)
    
    