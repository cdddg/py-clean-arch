import pytest


@pytest.mark.anyio
@pytest.mark.dependency
async def test_create_pokemon(client):
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
        'previous_evolutions': [],
        'next_evolutions': [],
    }

    # test create 0002
    response = await client.post(
        '/pokemons',
        json={
            'no': '0002',
            'name': 'Ivysaur',
            'type_names': ['Grass', 'Poison'],
            'previous_evolution_numbers': ['0001'],
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
        'previous_evolutions': [{'no': '0001', 'name': 'Bulbasaur'}],
        'next_evolutions': [],
    }

    # test create 0003
    response = await client.post(
        '/pokemons',
        json={
            'no': '0003',
            'name': 'Venusaur',
            'type_names': ['Grass', 'Poison'],
            'previous_evolution_numbers': ['0001', '0002'],
        },
    )
    data = response.json()
    data.get('types', []).sort(key=lambda k: k['name'])
    data.get('previous_evolutions', []).sort(key=lambda k: k['no'])
    assert response.status_code == 201
    assert data == {
        'no': '0003',
        'name': 'Venusaur',
        'types': [
            {'id': data['types'][0]['id'], 'name': 'Grass'},
            {'id': data['types'][1]['id'], 'name': 'Poison'},
        ],
        'previous_evolutions': [
            {'no': '0001', 'name': 'Bulbasaur'},
            {'no': '0002', 'name': 'Ivysaur'},
        ],
        'next_evolutions': [],
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_pokemon'])
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
        'previous_evolutions': [],
        'next_evolutions': [],
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_pokemon'])
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
            'previous_evolutions': [],
            'next_evolutions': [],
        },
        {
            'no': '0004',
            'name': 'Charmander',
            'types': [
                {'id': data[1]['types'][0]['id'], 'name': 'Fire'},
            ],
            'previous_evolutions': [],
            'next_evolutions': [],
        },
    ]


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_pokemon'])
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
            'previous_evolution_numbers': ['9001'],
            'next_evolution_numbers': ['9003'],
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
        'previous_evolutions': [
            {'no': '9001', 'name': 'AAA'},
        ],
        'next_evolutions': [
            {'no': '9003', 'name': 'CCC'},
        ],
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_pokemon'])
async def test_delete_pokemon(client):
    # pre-work
    _ = await client.post('/pokemons', json={'no': '9001', 'name': 'AAA', 'type_names': ['A']})

    # test delete
    response = await client.delete('/pokemons/9001')
    assert response.status_code == 204


@pytest.mark.anyio
@pytest.mark.dependency
async def test_create_trainer(client):
    response = await client.post(
        '/trainers',
        json={'name': 'Ash', 'region': 'Kanto', 'badge_count': 0},
    )
    data = response.json()
    assert response.status_code == 201
    assert data['id'] is not None
    assert data == {
        'id': data['id'],
        'name': 'Ash',
        'region': 'Kanto',
        'badge_count': 0,
        'team': [],
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_get_trainer(client):
    # pre-work: create trainer
    response = await client.post(
        '/trainers',
        json={'name': 'Ash', 'region': 'Kanto', 'badge_count': 0},
    )
    assert response.status_code == 201
    trainer_id = response.json()['id']

    # test get
    response = await client.get(f'/trainers/{trainer_id}')
    data = response.json()
    assert response.status_code == 200
    assert data == {
        'id': trainer_id,
        'name': 'Ash',
        'region': 'Kanto',
        'badge_count': 0,
        'team': [],
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_get_trainers(client):
    # pre-work
    response = await client.post(
        '/trainers',
        json={'name': 'Ash', 'region': 'Kanto', 'badge_count': 0},
    )
    assert response.status_code == 201
    response = await client.post(
        '/trainers',
        json={'name': 'Misty', 'region': 'Kanto', 'badge_count': 2},
    )
    assert response.status_code == 201

    # test get list
    response = await client.get('/trainers')
    data = response.json()
    assert response.status_code == 200
    assert len(data) >= 2


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_update_trainer(client):
    # pre-work
    response = await client.post(
        '/trainers',
        json={'name': 'Ash', 'region': 'Kanto', 'badge_count': 0},
    )
    assert response.status_code == 201
    trainer_id = response.json()['id']

    # test update
    response = await client.patch(
        f'/trainers/{trainer_id}',
        json={'name': 'Ash Ketchum', 'badge_count': 3},
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        'id': trainer_id,
        'name': 'Ash Ketchum',
        'region': 'Kanto',
        'badge_count': 3,
        'team': [],
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_delete_trainer(client):
    # pre-work
    response = await client.post(
        '/trainers',
        json={'name': 'Ash', 'region': 'Kanto', 'badge_count': 0},
    )
    assert response.status_code == 201
    trainer_id = response.json()['id']

    # test delete
    response = await client.delete(f'/trainers/{trainer_id}')
    assert response.status_code == 204

    # verify deleted
    response = await client.get(f'/trainers/{trainer_id}')
    assert response.status_code == 404


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_catch_pokemon(client):
    # pre-work: create pokemon and trainer
    await client.post(
        '/pokemons',
        json={'no': '0025', 'name': 'Pikachu', 'type_names': ['Electric']},
    )
    response = await client.post(
        '/trainers',
        json={'name': 'Ash', 'region': 'Kanto', 'badge_count': 0},
    )
    trainer_id = response.json()['id']

    # test catch
    response = await client.post(
        f'/trainers/{trainer_id}/catch',
        json={'pokemon_no': '0025'},
    )
    data = response.json()
    assert response.status_code == 200
    assert len(data['team']) == 1
    assert data['team'][0]['no'] == '0025'
    assert data['team'][0]['name'] == 'Pikachu'


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_catch_pokemon_duplicate(client):
    # pre-work
    await client.post(
        '/pokemons',
        json={'no': '0025', 'name': 'Pikachu', 'type_names': ['Electric']},
    )
    response = await client.post(
        '/trainers',
        json={'name': 'Ash', 'region': 'Kanto', 'badge_count': 0},
    )
    trainer_id = response.json()['id']

    # catch first time
    response = await client.post(
        f'/trainers/{trainer_id}/catch',
        json={'pokemon_no': '0025'},
    )
    assert response.status_code == 200

    # catch duplicate → 409
    response = await client.post(
        f'/trainers/{trainer_id}/catch',
        json={'pokemon_no': '0025'},
    )
    assert response.status_code == 409


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_catch_pokemon_team_full(client):
    # pre-work: create 7 pokemon and 1 trainer
    for i in range(1, 8):
        await client.post(
            '/pokemons',
            json={'no': f'000{i}', 'name': f'Pokemon{i}', 'type_names': ['Normal']},
        )
    response = await client.post(
        '/trainers',
        json={'name': 'Ash', 'region': 'Kanto', 'badge_count': 0},
    )
    trainer_id = response.json()['id']

    # catch 6 pokemon
    for i in range(1, 7):
        response = await client.post(
            f'/trainers/{trainer_id}/catch',
            json={'pokemon_no': f'000{i}'},
        )
        assert response.status_code == 200

    # catch 7th → 400
    response = await client.post(
        f'/trainers/{trainer_id}/catch',
        json={'pokemon_no': '0007'},
    )
    assert response.status_code == 400


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_release_pokemon(client):
    # pre-work
    await client.post(
        '/pokemons',
        json={'no': '0025', 'name': 'Pikachu', 'type_names': ['Electric']},
    )
    response = await client.post(
        '/trainers',
        json={'name': 'Ash', 'region': 'Kanto', 'badge_count': 0},
    )
    trainer_id = response.json()['id']
    await client.post(
        f'/trainers/{trainer_id}/catch',
        json={'pokemon_no': '0025'},
    )

    # test release
    response = await client.post(
        f'/trainers/{trainer_id}/release',
        json={'pokemon_no': '0025'},
    )
    data = response.json()
    assert response.status_code == 200
    assert len(data['team']) == 0


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_release_pokemon_not_owned(client):
    # pre-work
    response = await client.post(
        '/trainers',
        json={'name': 'Ash', 'region': 'Kanto', 'badge_count': 0},
    )
    trainer_id = response.json()['id']

    # release pokemon not owned → 400
    response = await client.post(
        f'/trainers/{trainer_id}/release',
        json={'pokemon_no': '9999'},
    )
    assert response.status_code == 400


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_trade_pokemon(client):
    # pre-work: create 2 pokemon and 2 trainers
    await client.post(
        '/pokemons',
        json={'no': '0025', 'name': 'Pikachu', 'type_names': ['Electric']},
    )
    await client.post(
        '/pokemons',
        json={'no': '0004', 'name': 'Charmander', 'type_names': ['Fire']},
    )
    response = await client.post(
        '/trainers',
        json={'name': 'Ash', 'region': 'Kanto', 'badge_count': 0},
    )
    trainer_id = response.json()['id']
    response = await client.post(
        '/trainers',
        json={'name': 'Gary', 'region': 'Kanto', 'badge_count': 0},
    )
    other_trainer_id = response.json()['id']

    # catch pokemon
    await client.post(f'/trainers/{trainer_id}/catch', json={'pokemon_no': '0025'})
    await client.post(f'/trainers/{other_trainer_id}/catch', json={'pokemon_no': '0004'})

    # test trade
    response = await client.post(
        '/trainers/trade',
        json={
            'trainer_id': trainer_id,
            'other_trainer_id': other_trainer_id,
            'pokemon_no': '0025',
            'other_pokemon_no': '0004',
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data['trainer']['team'][0]['no'] == '0004'
    assert data['other_trainer']['team'][0]['no'] == '0025'
