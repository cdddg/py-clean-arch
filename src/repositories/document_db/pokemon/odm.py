"""Object-Document Mapper (ODM) Definition for Pokemon Entities.

This file outlines the intended setup for an Object-Document Mapper (ODM) for MongoDB to manage Pokemon entities.
ODMs facilitate data conversion between incompatible type systems in object-oriented programming, similar to ORMs for relational databases.

The project currently uses async Motor with MongoDB and is exploring the potential integration of Beanie, an asynchronous Python ODM for MongoDB.
Learn more about Beanie at https://beanie-odm.dev/. Future updates will detail the progress of integrating Beanie into the project.

Anticipated Document Structure for Pokemon:
    +-------------------------------------------------+
    | Pokemon                                         |
    +-------------------------------------------------+
    | no: String                                      |  # Unique identifier for the Pokemon
    | name: String                                    |  # Name of the Pokemon
    | hp: Integer                                     |
    | attack: Integer                                 |
    | defense: Integer                                |
    | sp_atk: Integer                                 |
    | sp_def: Integer                                 |
    | speed: Integer                                  |
    | types: List[String]                             |  # List of types associated with the Pokemon
    | previous_evolution_object_ids: List[ObjectId]   |  # List of ObjectIds pointing to previous evolutionary forms
    | next_evolution_object_ids: List[ObjectId]       |  # List of ObjectIds pointing to subsequent evolutionary forms
    +-------------------------------------------------+
"""
