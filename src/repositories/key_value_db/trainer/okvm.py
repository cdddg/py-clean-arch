"""Key-Value Structure (KVM) Definition for Trainer Entities.

This file outlines the intended key-value structure for storing Trainer entities in Redis.

Anticipated Key-Value Structure for Trainer:
    +-------------------------------------------------+
    | Trainer                                         |
    +-------------------------------------------------+
    | Key: TRAINER:{id}:INFO                          |  # Hash storing basic info of the Trainer
    | Fields:                                         |
    |   - id: String (UUID hex)                       |  # Unique identifier for the Trainer
    |   - name: String                                |  # Name of the Trainer
    |   - region: String                              |  # Home region of the Trainer
    |   - badge_count: Integer                        |  # Number of badges earned (0-8)
    +-------------------------------------------------+
    | Key: TRAINER:{id}:TEAM                          |  # Set storing Pokemon numbers in team
    | Values:                                         |
    |   - pokemon_no: String                          |  # Pokemon number (e.g., "0025")
    +-------------------------------------------------+
"""
