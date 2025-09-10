from fastapi import FastAPI

from app.routers.answers import answers_router
from app.routers.questions import questions_router

app = FastAPI()


app.include_router(questions_router)
app.include_router(answers_router)