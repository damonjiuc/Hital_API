from app.database.engine import session_maker

from sqlalchemy import select, delete, insert

from app.database.models import Answer, Question


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls):
        async with session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_by_id(cls, model_id: int):
        async with session_maker() as session:
            query = select(cls.model).where(cls.model.id == model_id)
            result = await session.execute(query)
            return result.scalars().one_or_none()


    @classmethod
    async def add(cls, **data):
        async with session_maker() as session:
            obj = cls.model(**data)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj


    @classmethod
    async def delete_by_id(cls, model_id: int):
        async with session_maker() as session:
            query = delete(cls.model).where(cls.model.id == model_id)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount


class QuestionsDAO(BaseDAO):
    model = Question

    @classmethod
    async def add_question(cls, text: str):
        return await cls.add(text=text)


class AnswersDAO(BaseDAO):
    model = Answer

    @classmethod
    async def add_answer(cls, question_id: int, user_id: str, text: str):
        return await cls.add(question_id=question_id, user_id=user_id, text=text)