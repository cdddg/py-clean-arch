import pytest


@pytest.mark.anyio
@pytest.mark.dependency
async def test_create_pokemon(client):
    # test create 0004, 0005, 0006
    mutation = '''
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
                beforeEvolutionNumbers: ["0004"]
            }) {
                no
            }
            mutation3: createPokemon(input: {
                no: "0006",
                name: "Charizard",
                typeNames: ["FIRE", "FLYING"],
                beforeEvolutionNumbers: ["0004", "0005"]
            }) {
                no
                name
                types {
                    name
                }
                beforeEvolutions {
                    no
                    name
                }
                afterEvolutions {
                    no
                    name
                }
            }
        }
    '''
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    for _, v in data.items():
        v.get('types', []).sort(key=lambda k: k['name'])
        v.get('beforeEvolutions', []).sort(key=lambda k: k['no'])
        v.get('afterEvolutions', []).sort(key=lambda k: k['no'])
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
                'beforeEvolutions': [
                    {'no': '0004', 'name': 'Charmander'},
                    {'no': '0005', 'name': 'Charmeleon'},
                ],
                'afterEvolutions': [],
            },
        }
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_pokemon'])
async def test_get_pokemon(client):
    # pre-work
    mutation = '''
        mutation {
            createPokemon(input: {
                no: "0004",
                name: "Charmander",
                typeNames: ["FIRE"],
            }) {
                no
            }
        }
    '''
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('error') is None

    # test get existed
    query = '''
        query {
            pokemon(no: "0004") {
                no
                name
                types {
                    name
                },
                beforeEvolutions {
                    no
                    name
                },
                afterEvolutions {
                    no
                    name
                }
            }
        }
    '''
    response = await client.post('/graphql', json={'query': query})
    data = response.json()
    data.get('data', {}).get('types', []).sort(key=lambda k: k['name'])
    data.get('data', {}).get('before_evolutions', []).sort(key=lambda k: k['no'])
    data.get('data', {}).get('after_evolutions', []).sort(key=lambda k: k['no'])
    assert response.status_code == 200
    assert data.get('error') is None
    assert data == {
        'data': {
            'pokemon': {
                'no': '0004',
                'name': 'Charmander',
                'types': [{'name': 'FIRE'}],
                'beforeEvolutions': [],
                'afterEvolutions': [],
            }
        }
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_pokemon'])
async def test_get_pokemons(client):
    # pre-work
    mutation = '''
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
                beforeEvolutionNumbers: ["0004"]
            }) {
                no
            }
            mutation3: createPokemon(input: {
                no: "0006",
                name: "Charizard",
                typeNames: ["FIRE", "FLYING"],
                beforeEvolutionNumbers: ["0004", "0005"]
            }) {
                no
            }
        }
    '''
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('error') is None

    # test get list
    query = '''
        query {
            pokemons {
                no
                name
                types {
                    name
                },
                beforeEvolutions {
                    no
                },
                afterEvolutions {
                    no
                }
            }
        }
    '''
    response = await client.post('/graphql', json={'query': query})
    data = response.json()
    data.get('data', {}).get('types', []).sort(key=lambda k: k['name'])
    data.get('data', {}).get('before_evolutions', []).sort(key=lambda k: k['no'])
    data.get('data', {}).get('after_evolutions', []).sort(key=lambda k: k['no'])
    assert response.status_code == 200
    assert data.get('error') is None
    assert data == {
        'data': {
            'pokemons': [
                {
                    'no': '0004',
                    'name': 'Charmander',
                    'types': [{'name': 'FIRE'}],
                    'beforeEvolutions': [],
                    'afterEvolutions': [{'no': '0005'}, {'no': '0006'}],
                },
                {
                    'no': '0005',
                    'name': 'Charmeleon',
                    'types': [{'name': 'FIRE'}],
                    'beforeEvolutions': [{'no': '0004'}],
                    'afterEvolutions': [{'no': '0006'}],
                },
                {
                    'no': '0006',
                    'name': 'Charizard',
                    'types': [
                        {'name': 'FIRE'},
                        {'name': 'FLYING'},
                    ],
                    'beforeEvolutions': [{'no': '0004'}, {'no': '0005'}],
                    'afterEvolutions': [],
                },
            ]
        }
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_pokemon'])
async def test_update_pokemon(client):
    # pre-work
    mutation = '''
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
                beforeEvolutionNumbers: ["9004", "9005"]
            }) {
                no
            }
        }
    '''
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('error') is None

    # test update
    mutation = '''
        mutation {
            updatePokemon(no: "9006", input: {
                name: "XXX",
                typeNames: ["X"],
                beforeEvolutionNumbers: [],
                afterEvolutionNumbers: ["9004", "9005"]
            }) {
                no
                name
                types {
                    name
                }
                beforeEvolutions {
                    no
                    name
                }
                afterEvolutions {
                    no
                    name
                }
            }
        }
    '''
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
                'beforeEvolutions': [],
                'afterEvolutions': [{'no': '9004', 'name': 'AAA'}, {'no': '9005', 'name': 'BBB'}],
            }
        }
    }


@pytest.mark.anyio
@pytest.mark.dependency(depends=['test_create_pokemon'])
async def test_delete_pokemon(client):
    # pre-work
    mutation = '''
        mutation {
            createPokemon(input: {
                no: "9004",
                name: "AAA",
                typeNames: ["A"],
            }) {
                no
            }
        }
    '''
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('error') is None

    # test delete
    mutation = '''
        mutation {
            deletePokemon(no: "9004")
        }
    '''
    response = await client.post('/graphql', json={'query': mutation})
    data = response.json()
    assert response.status_code == 200
    assert data.get('error') is None
    assert data == {'data': {'deletePokemon': None}}
