import asyncio
import pytest
import json
from sqlalchemy import insert
from httpx import AsyncClient, ASGITransport

from app.config import settings
from app.database.models import *
from app.database.engine import session_maker, engine
from app.main import app as fastapi_app


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert getattr(settings, 'MODE', 'DEV') == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'app/tests/mock_{model}.json', 'r') as file:
            return json.load(file)

    questions = open_mock_json('questions')
    answers = open_mock_json('answers')

    async with session_maker() as session:
        if questions:
            add_questions = insert(Question).values(questions)
            await session.execute(add_questions)
        if answers:
            add_answers = insert(Answer).values(answers)
            await session.execute(add_answers)

        await session.commit()


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def client():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac