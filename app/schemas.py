from datetime import datetime
from pydantic import BaseModel, ConfigDict


class QuestionBase(BaseModel):
    text: str


class QuestionCreate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnswerBase(BaseModel):
    question_id: int
    user_id: str
    text: str


class AnswerCreate(AnswerBase):
    pass


class AnswerRead(AnswerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)