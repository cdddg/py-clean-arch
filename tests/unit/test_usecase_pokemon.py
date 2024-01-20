"""
Unit Testing the Usecase Layer for Pokémon.

In this module, we focus on testing the usecase layer of the Pokémon application. The usecase layer (often termed as the service layer in some architectures) coordinates complex operations and is a primary point of interaction between the outer layers (like HTTP or GraphQL interfaces) and the inner layers (like repositories or domain models).

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

from common.type import PokemonNumberStr
from usecases import pokemon as pokemon_ucase


@pytest.mark.anyio
async def test_get_pokemon(mock_async_unit_of_work):
    no = PokemonNumberStr('9999')
    await pokemon_ucase.get_pokemon(mock_async_unit_of_work, no)
    assert mock_async_unit_of_work.pokemon_repo.get.call_count == 1
