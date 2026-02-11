import pytest


@pytest.mark.anyio
@pytest.mark.dependency
async def test_create_pokemon(client):
    # test create 0004, 0005, 0006
    mutation = """
        mutation {
            mutation1: createPokemon(input: {
                no: "0004",
                name: "Charmander",
                typeNames: ["FIRE"],
            }) {
                no
            }
            mutation2: createPokemon(input: {
                no: "0005",
                name: "Charmeleon",
                typeNames: ["FIRE"],
                previousEvolutionNumbers: ["0004"]
            }) {
                no
            }
            mutation3: createPokemon(input: {
                no: "0006",
                name: "Charizard",
                typeNames: ["FIRE", "FLYING"],
                previousEvolutionNumbers: ["0004", "0005"]
            }) {
                no
                name
                types {
                    name
                }
                previousEvolutions {
                    no
                    name
                }
                nextEvolutions {
                    no
                    name
                }
            }
        }
    """
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    for _, v in data.items():
        v.get('types', []).sort(key=lambda k: k['name'])
        v.get('previousEvolutions', []).sort(key=lambda k: k['no'])
        v.get('nextEvolutions', []).sort(key=lambda k: k['no'])
    assert response.status_code == 200
    assert data.get('error') is None
    assert data == {
        'data': {
            'mutation1': {'no': '0004'},
            'mutation2': {'no': '0005'},
            'mutation3': {
                'no': '0006',
                'name': 'Charizard',
                'types': [{'name': 'FIRE'}, {'name': 'FLYING'}],
                'previousEvolutions': [
                    {'no': '0004', 'name': 'Charmander'},
                    {'no': '0005', 'name': 'Charmeleon'},
                ],
                'nextEvolutions': [],
            },
        }
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_pokemon'])
async def test_get_pokemon(client):
    # pre-work
    mutation = """
        mutation {
            createPokemon(input: {
                no: "0004",
                name: "Charmander",
                typeNames: ["FIRE"],
            }) {
                no
            }
        }
    """
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('error') is None

    # test get existed
    query = """
        query {
            pokemon(no: "0004") {
                no
                name
                types {
                    name
                },
                previousEvolutions {
                    no
                    name
                },
                nextEvolutions {
                    no
                    name
                }
            }
        }
    """
    response = await client.post('/graphql', json={'query': query})
    data = response.json()
    data.get('data', {}).get('types', []).sort(key=lambda k: k['name'])
    data.get('data', {}).get('previous_evolutions', []).sort(key=lambda k: k['no'])
    data.get('data', {}).get('next_evolutions', []).sort(key=lambda k: k['no'])
    assert response.status_code == 200
    assert data.get('error') is None
    assert data == {
        'data': {
            'pokemon': {
                'no': '0004',
                'name': 'Charmander',
                'types': [{'name': 'FIRE'}],
                'previousEvolutions': [],
                'nextEvolutions': [],
            }
        }
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_pokemon'])
async def test_get_pokemons(client):
    # pre-work
    mutation = """
        mutation {
            mutation1: createPokemon(input: {
                no: "0004",
                name: "Charmander",
                typeNames: ["FIRE"],
            }) {
                no
            }
            mutation2: createPokemon(input: {
                no: "0005",
                name: "Charmeleon",
                typeNames: ["FIRE"],
                previousEvolutionNumbers: ["0004"]
            }) {
                no
            }
            mutation3: createPokemon(input: {
                no: "0006",
                name: "Charizard",
                typeNames: ["FIRE", "FLYING"],
                previousEvolutionNumbers: ["0004", "0005"]
            }) {
                no
            }
        }
    """
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('error') is None

    # test get list
    query = """
        query {
            pokemons {
                no
                name
                types {
                    name
                },
                previousEvolutions {
                    no
                },
                nextEvolutions {
                    no
                }
            }
        }
    """
    response = await client.post('/graphql', json={'query': query})
    data = response.json()
    data.get('data', {}).get('types', []).sort(key=lambda k: k['name'])
    data.get('data', {}).get('previous_evolutions', []).sort(key=lambda k: k['no'])
    data.get('data', {}).get('next_evolutions', []).sort(key=lambda k: k['no'])
    assert response.status_code == 200
    assert data.get('error') is None
    assert data == {
        'data': {
            'pokemons': [
                {
                    'no': '0004',
                    'name': 'Charmander',
                    'types': [{'name': 'FIRE'}],
                    'previousEvolutions': [],
                    'nextEvolutions': [{'no': '0005'}, {'no': '0006'}],
                },
                {
                    'no': '0005',
                    'name': 'Charmeleon',
                    'types': [{'name': 'FIRE'}],
                    'previousEvolutions': [{'no': '0004'}],
                    'nextEvolutions': [{'no': '0006'}],
                },
                {
                    'no': '0006',
                    'name': 'Charizard',
                    'types': [
                        {'name': 'FIRE'},
                        {'name': 'FLYING'},
                    ],
                    'previousEvolutions': [{'no': '0004'}, {'no': '0005'}],
                    'nextEvolutions': [],
                },
            ]
        }
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_pokemon'])
async def test_update_pokemon(client):
    # pre-work
    mutation = """
        mutation {
            mutation1: createPokemon(input: {
                no: "9004",
                name: "AAA",
                typeNames: ["A"],
            }) {
                no
            }
            mutation2: createPokemon(input: {
                no: "9005",
                name: "BBB",
                typeNames: ["B"]
            }) {
                no
            }
            mutation3: createPokemon(input: {
                no: "9006",
                name: "CCC",
                typeNames: ["C"],
                previousEvolutionNumbers: ["9004", "9005"]
            }) {
                no
            }
        }
    """
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('error') is None

    # test update
    mutation = """
        mutation {
            updatePokemon(no: "9006", input: {
                name: "XXX",
                typeNames: ["X"],
                previousEvolutionNumbers: [],
                nextEvolutionNumbers: ["9004", "9005"]
            }) {
                no
                name
                types {
                    name
                }
                previousEvolutions {
                    no
                    name
                }
                nextEvolutions {
                    no
                    name
                }
            }
        }
    """
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('error') is None
    assert data == {
        'data': {
            'updatePokemon': {
                'no': '9006',
                'name': 'XXX',
                'types': [{'name': 'X'}],
                'previousEvolutions': [],
                'nextEvolutions': [{'no': '9004', 'name': 'AAA'}, {'no': '9005', 'name': 'BBB'}],
            }
        }
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_pokemon'])
async def test_delete_pokemon(client):
    # pre-work
    mutation = """
        mutation {
            createPokemon(input: {
                no: "9004",
                name: "AAA",
                typeNames: ["A"],
            }) {
                no
            }
        }
    """
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('error') is None

    # test delete
    mutation = """
        mutation {
            deletePokemon(no: "9004")
        }
    """
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('error') is None
    assert data == {'data': {'deletePokemon': None}}


@pytest.mark.anyio
@pytest.mark.dependency
async def test_create_trainer(client):
    mutation = """
        mutation {
            createTrainer(input: {
                name: "Ash",
                region: "Kanto",
                badgeCount: 0
            }) {
                id
                name
                region
                badgeCount
                team {
                    no
                    name
                }
            }
        }
    """
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('errors') is None
    trainer = data['data']['createTrainer']
    assert trainer['id'] is not None
    assert data == {
        'data': {
            'createTrainer': {
                'id': trainer['id'],
                'name': 'Ash',
                'region': 'Kanto',
                'badgeCount': 0,
                'team': [],
            }
        }
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_get_trainer(client):
    # pre-work
    mutation = """
        mutation {
            createTrainer(input: {
                name: "Ash",
                region: "Kanto",
                badgeCount: 0
            }) {
                id
            }
        }
    """
    response = await client.post('/graphql', json={'query': mutation})
    trainer_id = response.json()['data']['createTrainer']['id']

    # test get
    query = f"""
        query {{
            trainer(id: "{trainer_id}") {{
                id
                name
                region
                badgeCount
                team {{
                    no
                    name
                }}
            }}
        }}
    """
    response = await client.post('/graphql', json={'query': query})
    data = response.json()
    assert response.status_code == 200
    assert data.get('errors') is None
    assert data == {
        'data': {
            'trainer': {
                'id': trainer_id,
                'name': 'Ash',
                'region': 'Kanto',
                'badgeCount': 0,
                'team': [],
            }
        }
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_get_trainers(client):
    # pre-work
    mutation = """
        mutation {
            t1: createTrainer(input: { name: "Ash", region: "Kanto", badgeCount: 0 }) { id }
            t2: createTrainer(input: { name: "Misty", region: "Kanto", badgeCount: 2 }) { id }
        }
    """
    response = await client.post('/graphql', json={'query': mutation})
    assert response.status_code == 200
    assert response.json().get('errors') is None

    # test get list
    query = """
        query {
            trainers {
                id
                name
                region
                badgeCount
            }
        }
    """
    response = await client.post('/graphql', json={'query': query})
    data = response.json()
    assert response.status_code == 200
    assert data.get('errors') is None
    assert len(data['data']['trainers']) >= 2


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_update_trainer(client):
    # pre-work
    mutation = """
        mutation {
            createTrainer(input: { name: "Ash", region: "Kanto", badgeCount: 0 }) {
                id
            }
        }
    """
    response = await client.post('/graphql', json={'query': mutation})
    trainer_id = response.json()['data']['createTrainer']['id']

    # test update
    mutation = f"""
        mutation {{
            updateTrainer(id: "{trainer_id}", input: {{
                name: "Ash Ketchum",
                badgeCount: 3
            }}) {{
                id
                name
                region
                badgeCount
            }}
        }}
    """
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('errors') is None
    assert data == {
        'data': {
            'updateTrainer': {
                'id': trainer_id,
                'name': 'Ash Ketchum',
                'region': 'Kanto',
                'badgeCount': 3,
            }
        }
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_delete_trainer(client):
    # pre-work
    mutation = """
        mutation {
            createTrainer(input: { name: "Ash", region: "Kanto", badgeCount: 0 }) {
                id
            }
        }
    """
    response = await client.post('/graphql', json={'query': mutation})
    trainer_id = response.json()['data']['createTrainer']['id']

    # test delete
    mutation = f"""
        mutation {{
            deleteTrainer(id: "{trainer_id}")
        }}
    """
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('errors') is None
    assert data == {'data': {'deleteTrainer': None}}


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_catch_pokemon(client):
    # pre-work: create pokemon and trainer
    pokemon_mutation = """
        mutation {
            createPokemon(input: {
                no: "0025",
                name: "Pikachu",
                typeNames: ["Electric"]
            }) {
                no
            }
        }
    """
    await client.post('/graphql', json={'query': pokemon_mutation})

    trainer_mutation = """
        mutation {
            createTrainer(input: { name: "Ash", region: "Kanto", badgeCount: 0 }) {
                id
            }
        }
    """
    response = await client.post('/graphql', json={'query': trainer_mutation})
    trainer_id = response.json()['data']['createTrainer']['id']

    # test catch
    mutation = f"""
        mutation {{
            catchPokemon(id: "{trainer_id}", input: {{
                pokemonNo: "0025"
            }}) {{
                id
                name
                team {{
                    no
                    name
                }}
            }}
        }}
    """
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('errors') is None
    assert len(data['data']['catchPokemon']['team']) == 1
    assert data['data']['catchPokemon']['team'][0]['no'] == '0025'


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_release_pokemon(client):
    # pre-work
    await client.post(
        '/graphql',
        json={
            'query': """
            mutation {
                createPokemon(input: { no: "0025", name: "Pikachu", typeNames: ["Electric"] }) { no }
            }
        """
        },
    )
    response = await client.post(
        '/graphql',
        json={
            'query': """
            mutation {
                createTrainer(input: { name: "Ash", region: "Kanto", badgeCount: 0 }) { id }
            }
        """
        },
    )
    trainer_id = response.json()['data']['createTrainer']['id']

    # catch first
    await client.post(
        '/graphql',
        json={
            'query': f"""
            mutation {{
                catchPokemon(id: "{trainer_id}", input: {{ pokemonNo: "0025" }}) {{ id }}
            }}
        """
        },
    )

    # test release
    mutation = f"""
        mutation {{
            releasePokemon(id: "{trainer_id}", input: {{
                pokemonNo: "0025"
            }}) {{
                id
                team {{
                    no
                    name
                }}
            }}
        }}
    """
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('errors') is None
    assert len(data['data']['releasePokemon']['team']) == 0


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_trainer'])
async def test_trade_pokemon(client):
    # pre-work: create 2 pokemon and 2 trainers
    await client.post(
        '/graphql',
        json={
            'query': """
            mutation {
                p1: createPokemon(input: { no: "0025", name: "Pikachu", typeNames: ["Electric"] }) { no }
                p2: createPokemon(input: { no: "0004", name: "Charmander", typeNames: ["Fire"] }) { no }
            }
        """
        },
    )
    response = await client.post(
        '/graphql',
        json={
            'query': """
            mutation {
                t1: createTrainer(input: { name: "Ash", region: "Kanto", badgeCount: 0 }) { id }
                t2: createTrainer(input: { name: "Gary", region: "Kanto", badgeCount: 0 }) { id }
            }
        """
        },
    )
    data = response.json()['data']
    trainer_id = data['t1']['id']
    other_trainer_id = data['t2']['id']

    # catch pokemon
    await client.post(
        '/graphql',
        json={
            'query': f"""
            mutation {{
                catchPokemon(id: "{trainer_id}", input: {{ pokemonNo: "0025" }}) {{ id }}
            }}
        """
        },
    )
    await client.post(
        '/graphql',
        json={
            'query': f"""
            mutation {{
                catchPokemon(id: "{other_trainer_id}", input: {{ pokemonNo: "0004" }}) {{ id }}
            }}
        """
        },
    )

    # test trade
    mutation = f"""
        mutation {{
            tradePokemon(input: {{
                trainerId: "{trainer_id}",
                otherTrainerId: "{other_trainer_id}",
                pokemonNo: "0025",
                otherPokemonNo: "0004"
            }}) {{
                trainer {{
                    id
                    team {{ no name }}
                }}
                otherTrainer {{
                    id
                    team {{ no name }}
                }}
            }}
        }}
    """
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('errors') is None
    assert data['data']['tradePokemon']['trainer']['team'][0]['no'] == '0004'
    assert data['data']['tradePokemon']['otherTrainer']['team'][0]['no'] == '0025'
