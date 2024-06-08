"""Key-Value Structure (KVM) Definition for Pokemon Entities.

This file outlines the intended key-value structure for storing Pokemon entities in Redis.
The structure is defined to facilitate understanding and consistency across the project.
KVMs (Key-Value Mappers) help in organizing and managing the data in a key-value database.

Anticipated Key-Value Structure for Pokemon:
    +-------------------------------------------------+
    | Pokemon                                         |
    +-------------------------------------------------+
    | Key: POKEMON:{no}:INFO                          |  # Hash storing basic info of the Pokemon
    | Fields:                                         |
    |   - no: String                                  |  # Unique identifier for the Pokemon
    |   - name: String                                |  # Name of the Pokemon
    |   - hp: Integer                                 |
    |   - attack: Integer                             |
    |   - defense: Integer                            |
    |   - sp_atk: Integer                             |
    |   - sp_def: Integer                             |
    |   - speed: Integer                              |
    +-------------------------------------------------+
    | Key: POKEMON:{no}:TYPE                          |  # Set storing the types of the Pokemon
    | Values:                                         |
    |   - type_name: String                           |  # Type name (e.g., "Fire", "Water")
    +-------------------------------------------------+
    | Key: POKEMON:{no}:PREVIOUS_EVOLUTION            |  # Set storing previous evolution identifiers
    | Values:                                         |
    |   - previous_evolution_no: String               |  # Identifier of the previous evolutionary form
    +-------------------------------------------------+
    | Key: POKEMON:{no}:NEXT_EVOLUTION                |  # Set storing next evolution identifiers
    | Values:                                         |
    |   - next_evolution_no: String                   |  # Identifier of the next evolutionary form
    +-------------------------------------------------+
"""
