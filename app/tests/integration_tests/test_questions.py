import pytest
from httpx import AsyncClient


async def test_questions_crud(client: AsyncClient):
    # create
    resp = await client.post('/questions/', json={'text': 'Test question'})
    assert resp.status_code == 200
    created = resp.json()
    assert created['text'] == 'Test question'
    qid = created['id']

    # list
    resp = await client.get('/questions/')
    assert resp.status_code == 200
    items = resp.json()
    assert any(q['id'] == qid for q in items)

    # get with answers
    resp = await client.get(f'/questions/{qid}')
    assert resp.status_code == 200
    data = resp.json()
    assert data['id'] == qid
    assert 'answers' in data

    # delete
    resp = await client.delete(f'/questions/{qid}')
    assert resp.status_code == 200
    assert resp.json()['deleted'] == 1