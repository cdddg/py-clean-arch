class PokemonError(Exception):
    pass


class PokemonNotFound(PokemonError):
    pass


class PokemonAlreadyExists(PokemonError):
    pass


class PokemonUnknownError(PokemonError):
    pass
