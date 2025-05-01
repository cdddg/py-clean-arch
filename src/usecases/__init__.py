"""
Usecase Package.

This module implements Pokemon-related business logic operations (usecases).

Key design considerations:

- **Function-based Usecases**:
    Recommended when usecase logic is stateless and simple, with clearly defined dependencies.

- **Class-based Usecase** (when to use?):
    Recommended if the usecase needs to maintain state or has complex/shared dependencies:

    e.g.:
    ```
    class PokemonUsecase:
        def __init__(self, unit_of_work):
            self.uow = unit_of_work

        async def create_pokemon(self, data):
            ...

        async def update_pokemon(self, data):
            ...
    ```

Current implementation summary:

- The current implementation uses a functional (stateless) usecase, explicitly injecting dependencies through function parameters (`unit_of_work`).
- This functional approach is simple, explicit, fully compatible with Clean Architecture principles, and thus appropriate and recommended.
- Dependencies should continue to be provided via Constructor Injection (using Dependency Injection) to clearly separate concerns and improve testability.

Why and when prefer class-based usecases?

- **Statefulness**: You need to retain state between method calls.
- **Complexity**: Multiple closely-related usecase methods share the same dependencies or logic.
"""
