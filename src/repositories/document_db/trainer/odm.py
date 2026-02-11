"""Object-Document Mapper (ODM) Definition for Trainer Entities.

This file outlines the intended setup for an Object-Document Mapper (ODM) for MongoDB to manage Trainer entities.

Anticipated Document Structure for Trainer:
    +-------------------------------------------------+
    | Trainer                                         |
    +-------------------------------------------------+
    | id: String (UUID hex)                           |  # Unique identifier for the Trainer
    | name: String                                    |  # Name of the Trainer
    | region: String                                  |  # Home region of the Trainer
    | badge_count: Integer                            |  # Number of badges earned (0-8)
    | team: List[String]                              |  # List of Pokemon numbers in the team
    +-------------------------------------------------+
"""
