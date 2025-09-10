from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.database.engine import session_maker
from app.database.models import Answer, Question
from app.services.logger import logger


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls):
        logger.info(f'Получение всех записей из {cls.model.__tablename__}')
        async with session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f'Найдено {len(records)} записей в {cls.model.__tablename__}')
            return records

    @classmethod
    async def get_by_id(cls, model_id: int):
        logger.info(f'Поиск записи {model_id} в {cls.model.__tablename__}')
        async with session_maker() as session:
            query = select(cls.model).where(cls.model.id == model_id)
            result = await session.execute(query)
            record = result.scalars().one_or_none()
            if record:
                logger.info(f'Запись {model_id} найдена в {cls.model.__tablename__}')
            else:
                logger.warning(f'Запись {model_id} не найдена в {cls.model.__tablename__}')
            return record


    @classmethod
    async def add(cls, **data):
        logger.info(f'Создание новой записи в {cls.model.__tablename__}')
        async with session_maker() as session:
            obj = cls.model(**data)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            logger.info(f'Запись {obj.id} успешно создана в {cls.model.__tablename__}')
            return obj


    @classmethod
    async def delete_by_id(cls, model_id: int):
        logger.info(f'Удаление записи {model_id} из {cls.model.__tablename__}')
        async with session_maker() as session:
            query = delete(cls.model).where(cls.model.id == model_id)
            result = await session.execute(query)
            await session.commit()
            deleted_count = result.rowcount
            if deleted_count > 0:
                logger.info(f'Запись {model_id} успешно удалена из {cls.model.__tablename__}')
            else:
                logger.warning(f'Запись {model_id} не найдена для удаления в {cls.model.__tablename__}')
            return deleted_count


class QuestionsDAO(BaseDAO):
    model = Question

    @classmethod
    async def add_question(cls, text: str):
        return await cls.add(text=text)


    @classmethod
    async def get_with_answers(cls, model_id: int):
        logger.info(f'Поиск записи {model_id} с ответами в {cls.model.__tablename__}')
        async with session_maker() as session:
            query = (
                select(cls.model)
                .where(cls.model.id == model_id)
                .options(selectinload(cls.model.answers))
            )
            result = await session.execute(query)
            record = result.scalars().one_or_none()
            if record:
                logger.info(f'Запись {model_id} с {len(record.answers)} ответами найдена в {cls.model.__tablename__}')
            else:
                logger.warning(f'Запись {model_id} не найдена в {cls.model.__tablename__}')
            return record


class AnswersDAO(BaseDAO):
    model = Answer

    @classmethod
    async def add_answer(cls, question_id: int, user_id: str, text: str):
        logger.info(f'Создание ответа для вопроса {question_id} от пользователя {user_id}')
        question = await QuestionsDAO.get_by_id(question_id)
        if not question:
            logger.error(f'Вопрос {question_id} не найден при создании ответа')
            raise HTTPException(status_code=404, detail='Вопрос не найден')

        logger.info(f'Вопрос {question_id} найден, создаем ответ')
        return await cls.add(question_id=question_id, user_id=user_id, text=text)