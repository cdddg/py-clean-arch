```ascii
+------------------------------------------+      +------------------------------------------+
| Frameworks & Drivers                     |      | Frameworks & Drivers                     |
| (FastAPI)                                |      | (FastAPI)                                |
|                                          |      |                                          |
| - DTO: CreatePokemonRequest              |      | - DTO: PokemonResponse                   |
|   Receive request data                   |      |   Send response data                     |
+------------------------------------------+      +------------------------------------------+
                |                                                                 ^
                V                                                                 |
+------------------------------------------+      +------------------------------------------+
| Interface Adapters                       |      | Interface Adapters                       |
| (Router)                                 |      | (Router)                                 |
|                                          |      |                                          |
| - DTO -> Entity:                         |      | - Entity -> DTO:                         |
|   PokemonRequestMapper                   |      |   PokemonResponseMapper                  |
|   Map request to entity model            |      |   Map entity model to response data      |
+------------------------------------------+      +------------------------------------------+
                |                                                                 ^
                V                                                                 |
+------------------------------------------+      +------------------------------------------+
| Application Business                     |      | Application Business                     |
| (Usecase)                                |      | (Usecase)                                |
|                                          |      |                                          |
| - BO/Entity:                             |      | - BO/Entity:                             |
|   CreatePokemonModel                     |      |   PokemonModel                           |
|   Business logic input model             |      |   Business logic result                  |
+------------------------------------------+      +------------------------------------------+
                |                                                                 ^
                V                                                                 |
+------------------------------------------+      +------------------------------------------+
| Interface Adapters                       |      | Interface Adapters                       |
| (Repository/DAO)                         |      | (Repository/DAO)                         |
|                                          |      |                                          |
| - Using ORM                              |      | - DAO -> Entity:                         |
|   Perform database operations            |      |   Map database result back to entity     |
+------------------------------------------+      +------------------------------------------+
                |                                                                 ^
                V                                                                 |
+---------------------------------------------------------------------------------------------+
|                                    Frameworks & Drivers                                     |
|                                        (Database)                                           |
|                                                                                             |
|                                    - Database operations                                    |
+---------------------------------------------------------------------------------------------+
```

### Additional Information for `ascii-flow.md`

- This flow diagram is centered around the `POST /pokemons` endpoint, illustrating the detailed process of how a request to create a new Pokemon is handled within the application. It highlights the system's architecture and data flow, from request to response.
- **DTOs (Data Transfer Objects)**: Utilized at the system's boundary to encapsulate data received from and sent to the client. DTOs ensure a structured and consistent data format for external communication.
- **Entity/BO (Business Object)**: These models represent the domain data and rules. They are pivotal in carrying data across different layers of the application, serving both as business logic carriers and data representation entities.
- **Mappers**: Essential in the process of translating DTOs to Entity/BO models and vice versa. They facilitate a clear separation between external data structures and internal domain representations, ensuring that the application's core remains agnostic of external data formats.
- **Repository/DAO (Data Access Object)**: This layer abstracts the specifics of data persistence, employing ORM (Object-Relational Mapping) techniques to interact with the database. 
