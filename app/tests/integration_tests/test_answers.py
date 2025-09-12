import pytest
from httpx import AsyncClient


async def create_question(client: AsyncClient, text: str = 'Q for answers') -> int:
    resp = await client.post('/questions/', json={'text': text})
    assert resp.status_code == 200
    return resp.json()['id']


async def test_answers_crud(client: AsyncClient):
    # create question
    qid = await create_question(client)

    # add answer
    a_resp = await client.post(f'/questions/{qid}/answers/', json={'user_id': 'u_1', 'text': 'test_an'})
    assert a_resp.status_code == 200
    answer = a_resp.json()
    aid = answer['id']
    assert answer['question_id'] == qid

    # get answer
    g_resp = await client.get(f'/answers/{aid}')
    assert g_resp.status_code == 200
    assert g_resp.json()['id'] == aid

    # delete answer
    d_resp = await client.delete(f'/answers/{aid}')
    assert d_resp.status_code == 200
    assert d_resp.json()['deleted'] == 1


@pytest.mark.parametrize('make_question,user_id,text,status_code', [
    (True, 'u_1', 'test_text', 200),
    (False, 'u_1', 'test_text', 404),
])
async def test_make_answer(make_question, user_id, text, status_code, client: AsyncClient):
    if make_question:
        qid = await create_question(client)
    else:
        qid = 999999

    resp = await client.post(f'/questions/{qid}/answers/', json={'user_id': user_id, 'text': text})
    assert resp.status_code == status_code



async def test_same_user_multiple_answers_allowed(client: AsyncClient):
    qid = await create_question(client, 'Multi answers allowed?')

    # same user posts multiple answers
    a1 = await client.post(f'/questions/{qid}/answers/', json={'user_id': 'u_2', 'text': 'first'})
    a2 = await client.post(f'/questions/{qid}/answers/', json={'user_id': 'u_2', 'text': 'second'})
    assert a1.status_code == 200
    assert a2.status_code == 200


async def test_cascade_delete_answers_with_question(client: AsyncClient):
    qid = await create_question(client, 'To be deleted')

    # add answers and collect ids
    answer_ids = []
    for i in range(3):
        a_resp = await client.post(f'/questions/{qid}/answers/', json={'user_id': f'u-{i}', 'text': f'ans-{i}'})
        assert a_resp.status_code == 200
        answer_ids.append(a_resp.json()['id'])

    # delete question
    d = await client.delete(f'/questions/{qid}')
    assert d.status_code == 200

    # check if answers gone
    for aid in answer_ids:
        ga = await client.get(f'/answers/{aid}')
        assert ga.status_code == 404