from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List


class QuestionCreate(BaseModel):
    text: str


class QuestionRead(BaseModel):
    id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnswerCreate(BaseModel):
    user_id: str
    text: str


class AnswerRead(BaseModel):
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionWithAnswersRead(QuestionRead):
    answers: List[AnswerRead] = []