from pydantic import BaseModel, Field

from common.type import PokemonNumberStr, UUIDStr


class CreateTrainerRequest(BaseModel):
    name: str
    region: str
    badge_count: int = 0


class UpdateTrainerRequest(BaseModel):
    name: str | None = None
    region: str | None = None
    badge_count: int | None = None


class CatchPokemonRequest(BaseModel):
    pokemon_no: str = Field(..., description=PokemonNumberStr.__doc__)


class ReleasePokemonRequest(BaseModel):
    pokemon_no: str = Field(..., description=PokemonNumberStr.__doc__)


class TradePokemonRequest(BaseModel):
    trainer_id: str = Field(..., description=UUIDStr.__doc__)
    other_trainer_id: str = Field(..., description=UUIDStr.__doc__)
    pokemon_no: str = Field(..., description=PokemonNumberStr.__doc__)
    other_pokemon_no: str = Field(..., description=PokemonNumberStr.__doc__)


class TrainerPokemonResponse(BaseModel):
    no: str = Field(..., description=PokemonNumberStr.__doc__)
    name: str


class TrainerResponse(BaseModel):
    id: str = Field(..., description=UUIDStr.__doc__)
    name: str
    region: str
    badge_count: int
    team: list[TrainerPokemonResponse]


class TradeResponse(BaseModel):
    trainer: TrainerResponse
    other_trainer: TrainerResponse
