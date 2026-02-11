"""
Unit Testing the Usecase Layer.

In this module, we focus on testing the usecase layer of the application. The usecase layer (often termed as the service layer in some architectures) coordinates complex operations and is a primary point of interaction between the outer layers (like REST or GraphQL interfaces) and the inner layers (like repositories or domain models).

Key Aspects Covered:

1. Mocking:
    - The power of unit testing often comes from isolating the component or function you want to test. Here, we use mocking to simulate the behavior of complex dependencies.
    - In this specific test (`test_get_pokemon`), we mock the `async_uow` (Unit of Work) pattern, particularly the `pokemon_repo` which simulates interactions with the actual database.
    - By mocking, we ensure that the test remains fast, isn't dependent on external factors like database state, and strictly checks if our usecase functions are behaving as expected.

2. Assertions:
    - Once the function is called (in this case, `pokemon_ucase.get_pokemon('9999')`), we then proceed to check if it did what it's supposed to do.
    - The assertion `assert mock_async_uow.pokemon_repo.get.call_count == 1` verifies that our usecase method interacted with the repository exactly once, which is the expected behavior.

3. Async Testing:
    - Modern applications often involve asynchronous operations, especially when dealing with databases or external services.
    - Here, we mark our test with `@pytest.mark.anyio`, indicating that the test runs in an asynchronous context. It ensures that our test can handle `async/await` patterns in our usecase layer.

Overall, this test module showcases how to effectively unit test asynchronous usecase functions by mocking external dependencies, allowing us to verify the business logic without any side effects.
"""

import pytest

from common.type import PokemonNumberStr, UUIDStr
from models.exception import (
    TrainerAlreadyOwnsPokemon,
    TrainerDoesNotOwnPokemon,
    TrainerTeamFullError,
)
from models.pokemon import PokemonModel
from models.trainer import (
    CatchPokemonModel,
    CreateTrainerModel,
    ReleasePokemonModel,
    TradePokemonModel,
    TrainerModel,
    TrainerPokemonModel,
)
from usecases import pokemon as pokemon_ucase
from usecases import trainer as trainer_ucase


@pytest.mark.anyio
async def test_get_pokemon(mock_async_unit_of_work):
    no = PokemonNumberStr('9999')
    await pokemon_ucase.get_pokemon(mock_async_unit_of_work, no)
    assert mock_async_unit_of_work.pokemon_repo.get.call_count == 1


@pytest.mark.anyio
async def test_create_trainer(mock_async_unit_of_work):
    mock_async_unit_of_work.trainer_repo.create.return_value = UUIDStr('a' * 32)
    mock_async_unit_of_work.trainer_repo.get.return_value = TrainerModel(
        id=UUIDStr('a' * 32), name='Ash', region='Kanto', badge_count=0, team=[]
    )
    data = CreateTrainerModel(name='Ash', region='Kanto', badge_count=0)
    result = await trainer_ucase.create_trainer(mock_async_unit_of_work, data)
    assert result.name == 'Ash'
    assert mock_async_unit_of_work.trainer_repo.create.call_count == 1


@pytest.mark.anyio
async def test_catch_pokemon_team_full(mock_async_unit_of_work):
    trainer_id = UUIDStr('a' * 32)
    full_team = [
        TrainerPokemonModel(no=PokemonNumberStr(f'000{i}'), name=f'P{i}') for i in range(1, 7)
    ]
    mock_async_unit_of_work.trainer_repo.get.return_value = TrainerModel(
        id=trainer_id, name='Ash', region='Kanto', badge_count=0, team=full_team
    )
    mock_async_unit_of_work.pokemon_repo.get.return_value = PokemonModel(
        no=PokemonNumberStr('0007'), name='Squirtle'
    )

    data = CatchPokemonModel(pokemon_no=PokemonNumberStr('0007'))
    with pytest.raises(TrainerTeamFullError):
        await trainer_ucase.catch_pokemon(mock_async_unit_of_work, trainer_id, data)


@pytest.mark.anyio
async def test_catch_pokemon_already_owned(mock_async_unit_of_work):
    trainer_id = UUIDStr('a' * 32)
    mock_async_unit_of_work.trainer_repo.get.return_value = TrainerModel(
        id=trainer_id,
        name='Ash',
        region='Kanto',
        badge_count=0,
        team=[TrainerPokemonModel(no=PokemonNumberStr('0001'), name='Bulbasaur')],
    )
    mock_async_unit_of_work.pokemon_repo.get.return_value = PokemonModel(
        no=PokemonNumberStr('0001'), name='Bulbasaur'
    )

    data = CatchPokemonModel(pokemon_no=PokemonNumberStr('0001'))
    with pytest.raises(TrainerAlreadyOwnsPokemon):
        await trainer_ucase.catch_pokemon(mock_async_unit_of_work, trainer_id, data)


@pytest.mark.anyio
async def test_release_pokemon_not_owned(mock_async_unit_of_work):
    trainer_id = UUIDStr('a' * 32)
    mock_async_unit_of_work.trainer_repo.get.return_value = TrainerModel(
        id=trainer_id, name='Ash', region='Kanto', badge_count=0, team=[]
    )

    data = ReleasePokemonModel(pokemon_no=PokemonNumberStr('0001'))
    with pytest.raises(TrainerDoesNotOwnPokemon):
        await trainer_ucase.release_pokemon(mock_async_unit_of_work, trainer_id, data)


@pytest.mark.anyio
async def test_trade_pokemon_not_owned_by_trainer(mock_async_unit_of_work):
    trainer_id = UUIDStr('a' * 32)
    other_id = UUIDStr('b' * 32)
    mock_async_unit_of_work.trainer_repo.get.side_effect = [
        TrainerModel(id=trainer_id, name='Ash', region='Kanto', badge_count=0, team=[]),
        TrainerModel(
            id=other_id,
            name='Gary',
            region='Kanto',
            badge_count=0,
            team=[TrainerPokemonModel(no=PokemonNumberStr('0002'), name='Ivysaur')],
        ),
    ]

    data = TradePokemonModel(
        trainer_id=trainer_id,
        other_trainer_id=other_id,
        pokemon_no=PokemonNumberStr('0001'),
        other_pokemon_no=PokemonNumberStr('0002'),
    )
    with pytest.raises(TrainerDoesNotOwnPokemon):
        await trainer_ucase.trade_pokemon(mock_async_unit_of_work, data)


@pytest.mark.anyio
async def test_trade_pokemon_already_owned_by_other(mock_async_unit_of_work):
    trainer_id = UUIDStr('a' * 32)
    other_id = UUIDStr('b' * 32)
    mock_async_unit_of_work.trainer_repo.get.side_effect = [
        TrainerModel(
            id=trainer_id,
            name='Ash',
            region='Kanto',
            badge_count=0,
            team=[
                TrainerPokemonModel(no=PokemonNumberStr('0001'), name='Bulbasaur'),
                TrainerPokemonModel(no=PokemonNumberStr('0002'), name='Ivysaur'),
            ],
        ),
        TrainerModel(
            id=other_id,
            name='Gary',
            region='Kanto',
            badge_count=0,
            team=[TrainerPokemonModel(no=PokemonNumberStr('0002'), name='Ivysaur')],
        ),
    ]

    data = TradePokemonModel(
        trainer_id=trainer_id,
        other_trainer_id=other_id,
        pokemon_no=PokemonNumberStr('0001'),
        other_pokemon_no=PokemonNumberStr('0002'),
    )
    with pytest.raises(TrainerAlreadyOwnsPokemon):
        await trainer_ucase.trade_pokemon(mock_async_unit_of_work, data)
