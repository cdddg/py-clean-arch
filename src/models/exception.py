class PokemonError(Exception):
    pass


class PokemonNotFound(PokemonError):
    pass


class PokemonAlreadyExists(PokemonError):
    pass


class PokemonUnknownError(PokemonError):
    pass


class TrainerError(Exception):
    pass


class TrainerNotFound(TrainerError):
    pass


class TrainerTeamFullError(TrainerError):
    pass


class TrainerAlreadyOwnsPokemon(TrainerError):
    pass


class TrainerDoesNotOwnPokemon(TrainerError):
    pass
