```ini
[HTTP Request: POST /pokemons]
    |
    v
[Frameworks & Drivers: FastAPI]
    |  (Raw Request -> DTO: CreatePokemonRequest)
    v
[Interface Adapters: Controller]
    |  (Mapper: DTO CreatePokemonRequest -> Entity/BO: CreatePokemonModel)
    v
[Application Business Rules: UseCase]
    |  (Business logic: Create Pokémon, Replace types, Replace evolutions)
    |  ┊  (Call abstract Repository to save Entity/BO data)
    |  ┊  (Return Entity/BO: PokemonModel)
    |  ┊
    |  └┄┄> [Interface Adapters: Repository/DAO] <┄┄> [Frameworks & Drivers: Database]
    |          (Save to DB using ORM: create, replace, get)
    v
[Interface Adapters: Controller]
    |  (Mapper: Entity/BO PokemonModel -> DTO: PokemonResponse)
    v
[Frameworks & Drivers: FastAPI]
    |  (Send HTTP Response: 201 Created)
    v
[HTTP Response]
```

### Additional Information for `ascii-flow.md`

This flow diagram is centered around the `POST /pokemons` endpoint, illustrating the detailed process of how a request to create a new Pokemon is handled within the application. It highlights the system's architecture and data flow, from request to response.

- **DTOs (Data Transfer Objects)**: Utilized at the system's boundary to encapsulate data received from and sent to the client. DTOs ensure a structured and consistent data format for external communication.
- **Entity/BO (Business Object)**: These models represent the domain data and rules. They are pivotal in carrying data across different layers of the application, serving both as business logic carriers and data representation entities.
- **Mappers**: Essential in the process of translating DTOs to Entity/BO models and vice versa. They facilitate a clear separation between external data structures and internal domain representations, ensuring that the application's core remains agnostic of external data formats.
- **Repository/DAO (Data Access Object)**: This layer abstracts the specifics of data persistence, employing ORM (Object-Relational Mapping) techniques to interact with the database.
