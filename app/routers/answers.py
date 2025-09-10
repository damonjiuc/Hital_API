from fastapi import APIRouter, HTTPException

from app.schemas import AnswerCreate, AnswerRead
from app.services.dao import AnswersDAO
from app.services.logger import logger

answers_router = APIRouter(tags=['Ответы'])


@answers_router.post('/questions/{id}/answers/')
async def add_answer(id: int, data: AnswerCreate) -> AnswerRead:
    logger.info(f'Создание ответа для вопроса {id} от пользователя {data.user_id}')
    return await AnswersDAO.add_answer(question_id=id, user_id=data.user_id, text=data.text)


@answers_router.get('/answers/{id}')
async def get_answer(id: int) -> AnswerRead:
    logger.info(f'Запрос на получение ответа {id}')
    answer = await AnswersDAO.get_by_id(id)
    if not answer:
        logger.warning(f'Ответ {id} не найден')
        raise HTTPException(status_code=404, detail='Ответ не найден')
    logger.info(f'Ответ {id} найден')
    return answer


@answers_router.delete('/answers/{id}')
async def delete_answer(id: int) -> dict[str, int]:
    logger.info(f'Запрос на удаление ответа {id}')
    deleted = await AnswersDAO.delete_by_id(id)
    if not deleted:
        logger.warning(f'Ответ {id} не найден для удаления')
        raise HTTPException(status_code=404, detail='Ответ не найден')
    logger.info(f'Ответ {id} успешно удален')
    return {'deleted': deleted}