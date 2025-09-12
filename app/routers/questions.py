from fastapi import APIRouter, HTTPException

from app.schemas import QuestionRead, QuestionCreate, QuestionWithAnswersRead
from app.services.dao import QuestionsDAO
from app.services.logger import logger

questions_router = APIRouter(
    prefix='/questions',
    tags=['Вопросы']
)


@questions_router.get('/')
async def get_questions() -> list[QuestionRead]:
    logger.info('Запрос на получение всех вопросов')

    return await QuestionsDAO.find_all()


@questions_router.post('/')
async def add_question(data: QuestionCreate) -> QuestionRead:
    logger.info(f'Создание нового вопроса: {data.text[:50]}...')

    return await QuestionsDAO.add_question(text=data.text)


@questions_router.get('/{id}')
async def get_question(id: int) -> QuestionWithAnswersRead:
    logger.info(f'Запрос на получение вопроса {id} с ответами')

    question = await QuestionsDAO.get_with_answers(id)

    if not question:
        logger.warning(f'Вопрос {id} не найден')
        raise HTTPException(status_code=404, detail='Вопрос не найден')

    logger.info(f'Вопрос {id} найден с {len(question.answers)} ответами')

    return question


@questions_router.delete('/{id}')
async def delete_question(id: int) -> dict[str, int]:
    logger.info(f'Запрос на удаление вопроса {id}')

    deleted = await QuestionsDAO.delete_by_id(id)

    if not deleted:
        logger.warning(f'Вопрос {id} не найден для удаления')
        raise HTTPException(status_code=404, detail='Вопрос не найден')

    logger.info(f'Вопрос {id} успешно удален')

    return {'deleted': deleted}