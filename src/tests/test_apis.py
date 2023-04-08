import pytest


# def setup_module():

#     from pkg.repositories.rdbms.pokemon.orm import DeclarativeMeta
#     from settings.db import async_engine
#     DeclarativeMeta.metadata.create_all(async_engine)

import os, pprint; pprint.pprint(dict(os.environ))


@pytest.mark.anyio
async def test_create_pokemon(client, session):
    response = await client.post(
        '/pokemons',
        json={'no': '0001', 'name': 'Bulbasaur', 'type_names': ['Grass', 'Poison']},
    )
    data = response.json()
    assert response.status_code == 201

    data['types'].sort(key=lambda k: k['name'])
    assert data == {
        'no': '0001',
        'name': 'Bulbasaur',
        'types': [
            {'id': data['types'][0]['id'], 'name': 'Grass'},
            {'id': data['types'][1]['id'], 'name': 'Poison'},
        ],
        'before_evolutions': [],
        'after_evolutions': [],
    }
    # assert get_session().query(Pokemon).filter_by(no='006').count() == 1


# def test_get_pokemon():
#     response = client.get('/pokemons/006')
#     assert response.status_code == 200

#     data = response.json()
#     data['types'].sort(key=lambda k: k['name'])
#     assert data == {
#         'id': '006',
#         'no': '006',
#         'name': 'CHARIZARD',
#         'types': [
#             {'id': data['types'][0]['id'], 'name': 'FIRE'},
#             {'id': data['types'][1]['id'], 'name': 'FLYING'},
#         ],
#         'evolutions': {'before': [], 'after': []},
#     }


# def test_update_pokemon():
#     response = client.patch(
#         '/pokemons/006',
#         json={'name': 'CHARIZARD_2', 'types': ['NONE']},
#     )
#     data = response.json()
#     assert response.status_code == 200
#     assert data == {
#         'id': '006',
#         'no': '006',
#         'name': 'CHARIZARD_2',
#         'types': [
#             {'id': data['types'][0]['id'], 'name': 'NONE'},
#         ],
#         'evolutions': {'before': [], 'after': []},
#     }


# def test_delete_pokemon():
#     assert get_session().query(Pokemon).filter_by(no='006').count() == 1

#     response = client.delete('/pokemons/006')
#     data = response.json()
#     assert response.status_code == 200
#     assert data == {
#         'id': '006',
#         'no': '006',
#         'name': 'CHARIZARD_2',
#         'types': [
#             {'id': data['types'][0]['id'], 'name': 'NONE'},
#         ],
#         'evolutions': {'before': [], 'after': []},
#     }


# def test_add_evolution():
#     # create pokemon
#     client.post(
#         '/pokemons/create',
#         json={'no': '004', 'name': 'CHARMANDER', 'types': ['FIRE']},
#     )
#     client.post(
#         '/pokemons/create',
#         json={'no': '005', 'name': 'CHARMELEON', 'types': ['FIRE']},
#     )
#     client.post(
#         '/pokemons/create',
#         json={'no': '006', 'name': 'CHARIZARD', 'types': ['FIRE', 'FLYING']},
#     )

#     # add evolution
#     response = client.post('/pokemons/004/evolution', json={'evolutions_no': ['005']})
#     data = response.json()
#     assert response.status_code == 200
#     assert data == {
#         'id': '004',
#         'no': '004',
#         'name': 'CHARMANDER',
#         'types': [{'id': data['types'][0]['id'], 'name': 'FIRE'}],
#         'evolutions': {
#             'before': [],
#             'after': [{'id': '005', 'no': '005', 'name': 'CHARMELEON'}],
#         },
#     }

#     response = client.post('/pokemons/005/evolution', json={'evolutions_no': ['006']})
#     data = response.json()
#     assert response.status_code == 200
#     assert data == {
#         'id': '005',
#         'no': '005',
#         'name': 'CHARMELEON',
#         'types': [{'id': data['types'][0]['id'], 'name': 'FIRE'}],
#         'evolutions': {
#             'before': [{'id': '004', 'no': '004', 'name': 'CHARMANDER'}],
#             'after': [{'id': '006', 'no': '006', 'name': 'CHARIZARD'}],
#         },
#     }
