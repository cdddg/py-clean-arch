import pytest

from tests.conftest import deep_compare


@pytest.mark.anyio
async def test_pokemon_evolution_chain(client):
    # Step 1: Create Pokemon 'Ivysaur' with number '0002'
    response = await client.post(
        '/pokemons', json={'no': '0002', 'name': 'Ivysaur', 'type_names': ['Grass', 'Poison']}
    )
    assert response.status_code == 201
    assert deep_compare(
        response.json(),
        {
            'no': '0002',
            'name': 'Ivysaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [],
            'next_evolutions': [],
        },
    )

    # Step 1-1: Attempt to create a duplicate 'Ivysaur' should fail
    response = await client.post(
        '/pokemons', json={'no': '0002', 'name': 'Ivysaur', 'type_names': ['Grass', 'Poison']}
    )
    assert response.status_code == 409

    # Step 2: Create Pokemon 'Bulbasaur' with number '0001'
    response = await client.post(
        '/pokemons', json={'no': '0001', 'name': 'Bulbasaur', 'type_names': ['Grass', 'Poison']}
    )
    assert response.status_code == 201
    assert deep_compare(
        response.json(),
        {
            'no': '0001',
            'name': 'Bulbasaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [],
            'next_evolutions': [],
        },
    )

    # Step 2-2: Attempt to create a duplicate 'Bulbasaur' should fail
    response = await client.post(
        '/pokemons', json={'no': '0001', 'name': 'Bulbasaur', 'type_names': ['Grass', 'Poison']}
    )
    assert response.status_code == 409

    # Step 2-3: Update 'Bulbasaur' to add 'Ivysaur' as next evolution
    response = await client.patch('/pokemons/0001', json={'next_evolution_numbers': ['0002']})
    assert response.status_code == 200
    assert deep_compare(
        response.json(),
        {
            'no': '0001',
            'name': 'Bulbasaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [],
            'next_evolutions': [
                {'no': '0002', 'name': 'Ivysaur'},
            ],
        },
    )

    # Step 3: Create Pokemon 'Venusaur' with number '0003'
    response = await client.post(
        '/pokemons', json={'no': '0003', 'name': 'Venusaur', 'type_names': ['Grass', 'Poison']}
    )
    assert response.status_code == 201
    assert deep_compare(
        response.json(),
        {
            'no': '0003',
            'name': 'Venusaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [],
            'next_evolutions': [],
        },
    )

    # Step 3-1: Attempt to create a duplicate 'Venusaur' should fail
    response = await client.post(
        '/pokemons', json={'no': '0003', 'name': 'Venusaur', 'type_names': ['Grass', 'Poison']}
    )
    assert response.status_code == 409

    # Step 3-2: Update 'Venusaur' to add 'Bulbasaur' and 'Ivysaur' as previous evolutions
    response = await client.patch(
        '/pokemons/0003', json={'previous_evolution_numbers': ['0001', '0002']}
    )
    assert response.status_code == 200
    assert deep_compare(
        response.json(),
        {
            'no': '0003',
            'name': 'Venusaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [
                {'no': '0001', 'name': 'Bulbasaur'},
                {'no': '0002', 'name': 'Ivysaur'},
            ],
            'next_evolutions': [],
        },
    )

    # Test retrieval of each Pokemon to verify correct evolution links
    # Step 4-1: Retrieve 'Bulbasaur'
    response = await client.get('/pokemons/0001')
    assert response.status_code == 200
    assert deep_compare(
        response.json(),
        {
            'no': '0001',
            'name': 'Bulbasaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [],
            'next_evolutions': [
                {'no': '0002', 'name': 'Ivysaur'},
                {'no': '0003', 'name': 'Venusaur'},
            ],
        },
    )

    # Step 4-2: Retrieve 'Ivysaur'
    response = await client.get('/pokemons/0002')
    assert response.status_code == 200
    assert deep_compare(
        response.json(),
        {
            'no': '0002',
            'name': 'Ivysaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [
                {'no': '0001', 'name': 'Bulbasaur'},
            ],
            'next_evolutions': [
                {'no': '0003', 'name': 'Venusaur'},
            ],
        },
    )

    # Step 4-3: Retrieve 'Venusaur'
    response = await client.get('/pokemons/0003')
    assert response.status_code == 200
    assert deep_compare(
        response.json(),
        {
            'no': '0003',
            'name': 'Venusaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [
                {'no': '0001', 'name': 'Bulbasaur'},
                {'no': '0002', 'name': 'Ivysaur'},
            ],
            'next_evolutions': [],
        },
    )

    # Step 5: Delete 'Ivysaur'
    response = await client.delete('/pokemons/0002')
    assert response.status_code == 204

    # Confirm deletion impact
    # Step 6-1: Check 'Bulbasaur' evolution details post-deletion of 'Ivysaur'
    response = await client.get('/pokemons/0001')
    assert response.status_code == 200
    assert deep_compare(
        response.json(),
        {
            'no': '0001',
            'name': 'Bulbasaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [],
            'next_evolutions': [
                {
                    'no': '0003',
                    'name': 'Venusaur',
                },  # This update shows Ivysaur has been removed correctly.
            ],
        },
    )

    # Step 6-2: Check 'Ivysaur' no longer exists
    response = await client.get('/pokemons/0002')
    assert response.status_code == 404

    # Step 6-3: Verify 'Venusaur' still lists 'Bulbasaur' as previous evolution
    response = await client.get('/pokemons/0003')
    assert response.status_code == 200
    assert deep_compare(
        response.json(),
        {
            'no': '0003',
            'name': 'Venusaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'},
            ],
            'previous_evolutions': [
                {
                    'no': '0001',
                    'name': 'Bulbasaur',
                },  # Updated to show only Bulbasaur remains after deletion of Ivysaur.
            ],
            'next_evolutions': [],
        },
    )


@pytest.mark.anyio
async def test_trainer_team_management(client):
    # Step 1: Create Pokemon
    for no, name, types in [
        ('0025', 'Pikachu', ['Electric']),
        ('0004', 'Charmander', ['Fire']),
        ('0007', 'Squirtle', ['Water']),
    ]:
        response = await client.post(
            '/pokemons',
            json={'no': no, 'name': name, 'type_names': types},
        )
        assert response.status_code == 201, f'Failed to create Pokemon {no}'

    # Step 2: Create Trainers
    response = await client.post(
        '/trainers',
        json={'name': 'Ash', 'region': 'Kanto', 'badge_count': 0},
    )
    assert response.status_code == 201
    ash_id = response.json()['id']

    response = await client.post(
        '/trainers',
        json={'name': 'Gary', 'region': 'Kanto', 'badge_count': 2},
    )
    assert response.status_code == 201
    gary_id = response.json()['id']

    # Step 3: Catch Pokemon
    response = await client.post(
        f'/trainers/{ash_id}/catch',
        json={'pokemon_no': '0025'},
    )
    assert response.status_code == 200
    assert len(response.json()['team']) == 1

    response = await client.post(
        f'/trainers/{ash_id}/catch',
        json={'pokemon_no': '0007'},
    )
    assert response.status_code == 200
    assert len(response.json()['team']) == 2

    response = await client.post(
        f'/trainers/{gary_id}/catch',
        json={'pokemon_no': '0004'},
    )
    assert response.status_code == 200
    assert len(response.json()['team']) == 1

    # Step 4: Trade Pokemon - Ash's Pikachu for Gary's Charmander
    response = await client.post(
        '/trainers/trade',
        json={
            'trainer_id': ash_id,
            'other_trainer_id': gary_id,
            'pokemon_no': '0025',
            'other_pokemon_no': '0004',
        },
    )
    assert response.status_code == 200
    trade_data = response.json()
    ash_team_nos = [p['no'] for p in trade_data['trainer']['team']]
    gary_team_nos = [p['no'] for p in trade_data['other_trainer']['team']]
    assert '0004' in ash_team_nos
    assert '0007' in ash_team_nos
    assert '0025' in gary_team_nos

    # Step 5: Delete Pokemon 0004 → should be removed from Ash's team
    response = await client.delete('/pokemons/0004')
    assert response.status_code == 204

    # Verify Ash's team no longer has 0004
    response = await client.get(f'/trainers/{ash_id}')
    assert response.status_code == 200
    ash_data = response.json()
    ash_team_nos = [p['no'] for p in ash_data['team']]
    assert '0004' not in ash_team_nos
    assert '0007' in ash_team_nos

    # Step 6: Delete Trainer Gary → should succeed cleanly
    response = await client.delete(f'/trainers/{gary_id}')
    assert response.status_code == 204

    # Verify Gary is gone
    response = await client.get(f'/trainers/{gary_id}')
    assert response.status_code == 404

    # Step 7: Verify Ash still exists
    response = await client.get(f'/trainers/{ash_id}')
    assert response.status_code == 200
    assert response.json()['name'] == 'Ash'
