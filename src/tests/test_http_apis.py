import pytest


@pytest.mark.anyio
async def test_create_pokemon(client, engine, session):
    # test create 0001
    response = await client.post(
        '/pokemons',
        json={'no': '0001', 'name': 'Bulbasaur', 'type_names': ['Grass', 'Poison']},
    )
    data = response.json()
    data.get('types', []).sort(key=lambda k: k['name'])
    assert response.status_code == 201
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

    # test create 0002
    response = await client.post(
        '/pokemons',
        json={
            'no': '0002',
            'name': 'Ivysaur',
            'type_names': ['Grass', 'Poison'],
            'before_evolution_numbers': ['0001'],
        },
    )
    data = response.json()
    data.get('types', []).sort(key=lambda k: k['name'])
    assert response.status_code == 201
    assert data == {
        'no': '0002',
        'name': 'Ivysaur',
        'types': [
            {'id': data['types'][0]['id'], 'name': 'Grass'},
            {'id': data['types'][1]['id'], 'name': 'Poison'},
        ],
        'before_evolutions': [{'no': '0001', 'name': 'Bulbasaur'}],
        'after_evolutions': [],
    }

    # test create 0003
    response = await client.post(
        '/pokemons',
        json={
            'no': '0003',
            'name': 'Venusaur',
            'type_names': ['Grass', 'Poison'],
            'before_evolution_numbers': ['0001', '0002'],
        },
    )
    data = response.json()
    data.get('types', []).sort(key=lambda k: k['name'])
    data.get('before_evolutions', []).sort(key=lambda k: k['no'])
    assert response.status_code == 201
    assert data == {
        'no': '0003',
        'name': 'Venusaur',
        'types': [
            {'id': data['types'][0]['id'], 'name': 'Grass'},
            {'id': data['types'][1]['id'], 'name': 'Poison'},
        ],
        'before_evolutions': [
            {'no': '0001', 'name': 'Bulbasaur'},
            {'no': '0002', 'name': 'Ivysaur'},
        ],
        'after_evolutions': [],
    }


@pytest.mark.anyio
async def test_get_pokemon(client):
    # pre-work
    response = await client.post(
        '/pokemons',
        json={'no': '0001', 'name': 'Bulbasaur', 'type_names': ['Grass', 'Poison']},
    )
    assert response.status_code == 201

    # test get existed
    response = await client.get('/pokemons/0001')
    data = response.json()
    data.get('types', []).sort(key=lambda k: k['name'])
    assert response.status_code == 200
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


@pytest.mark.anyio
async def test_get_pokemons(client):
    # pre-work
    response = await client.post(
        '/pokemons',
        json={'no': '0001', 'name': 'Bulbasaur', 'type_names': ['Grass', 'Poison']},
    )
    assert response.status_code == 201
    response = await client.post(
        '/pokemons',
        json={'no': '0004', 'name': 'Charmander', 'type_names': ['Fire']},
    )
    assert response.status_code == 201

    # test get list
    response = await client.get('/pokemons')
    data = response.json()
    data.sort(key=lambda k: k['no'])
    assert response.status_code == 200
    assert data == [
        {
            'no': '0001',
            'name': 'Bulbasaur',
            'types': [
                {'id': data[0]['types'][0]['id'], 'name': 'Grass'},
                {'id': data[0]['types'][1]['id'], 'name': 'Poison'},
            ],
            'before_evolutions': [],
            'after_evolutions': [],
        },
        {
            'no': '0004',
            'name': 'Charmander',
            'types': [
                {'id': data[1]['types'][0]['id'], 'name': 'Fire'},
            ],
            'before_evolutions': [],
            'after_evolutions': [],
        },
    ]


@pytest.mark.anyio
async def test_update_pokemon(client):
    # pre-work
    response = await client.post(
        '/pokemons', json={'no': '9001', 'name': 'AAA', 'type_names': ['A']}
    )
    assert response.status_code == 201
    response = await client.post(
        '/pokemons', json={'no': '9002', 'name': 'BBB', 'type_names': ['B']}
    )
    assert response.status_code == 201
    response = await client.post(
        '/pokemons', json={'no': '9003', 'name': 'CCC', 'type_names': ['C']}
    )
    assert response.status_code == 201

    # test update
    response = await client.patch(
        '/pokemons/9002',
        json={
            'name': 'BBB-2',
            'type_names': ['B-2'],
            'before_evolution_numbers': ['9001'],
            'after_evolution_numbers': ['9003'],
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        'no': '9002',
        'name': 'BBB-2',
        'types': [
            {'id': data['types'][0]['id'], 'name': 'B-2'},
        ],
        'before_evolutions': [{'no': '9001', 'name': 'AAA'}],
        'after_evolutions': [{'no': '9003', 'name': 'CCC'}],
    }


@pytest.mark.anyio
async def test_delete_pokemon(client):
    # pre-work
    response = await client.post(
        '/pokemons', json={'no': '9001', 'name': 'AAA', 'type_names': ['A']}
    )

    # test delete
    response = await client.delete('/pokemons/9001')
    assert response.status_code == 204
