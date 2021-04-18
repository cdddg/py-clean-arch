class PokedexError(Exception):
    pass


class PokemonNotFound(PokedexError):
    pass


class PokemonUnknownError(PokedexError):
    pass
