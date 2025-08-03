# FAQ

### 1. What is the main objective of this project?

This project is a practical example that demonstrates how to apply **Clean Architecture** principles to build a Pokémon API using the **FastAPI** framework. The goal is to provide a reference to help you understand how to design a system architecture that is testable, maintainable, and easily extensible.

---

### 2. Why does this project support both GraphQL and REST APIs, and multiple databases?

This is an intentional design choice to highlight the core values of **Clean Architecture**:

- **Interface Independence**: The same business logic can serve external requests through different API styles. For instance, **GraphQL** is well-suited for complex queries, while **REST** is appropriate for standard CRUD (Create, Read, Update, Delete) operations.
- **Database Independence**: Business logic is completely decoupled from specific storage technologies. You can freely switch between relational, document-based, key-value, and other database types without changing the core functionality.

In a real-world project, you would typically choose only one or two technologies. The diversity here is meant to demonstrate the architecture's flexibility. The key takeaway is learning to design abstraction layers, not necessarily using all options at once.

------

### 3. Can I remove databases or API types that I don't need?

Yes, that's exactly the purpose of **Clean Architecture**.

You can remove or replace code within the `src/controllers` folder to suit your project's needs. For example:

- If you only need the **REST API**, you can simply delete the `src/controllers/graphql` folder.
- If you only need **MongoDB**, you can remove other `src/repositories`-related code and only provide a MongoDB instance during dependency injection.

Removing unused parts will not affect the core business logic in the **`usecases`** layer, which is the main benefit of this decoupled architecture.

---

### 4. What considerations went into naming the outer layers of the Clean Architecture?

This project uses **`controllers`** for the outer interface, which is a convention commonly found in the FastAPI community. Clean Architecture is flexible and allows for various naming conventions, such as:

- **`handlers`** (event-driven)
- **`endpoints`** (API-oriented)
- **`routes`** (Express.js style)
- **`api`** (concise)
- **`interfaces`** (DDD style)
- **`gateways`** (microservices)
- **`entrypoints`** (original Clean Architecture)

The emphasis is not on the name itself, but on the **separation of concerns**. The best naming approach is one that aligns with your team's technical vocabulary and project context to facilitate clear communication.

---

### 5. Is this architectural layering a standard? Can it be simplified?

No, the architectural layering in this project is designed to fully demonstrate the concepts of **Clean Architecture**, and you should adjust it based on your project's complexity.

Clean Architecture is not a rigid set of rules, but a collection of design principles. Its core is the **"Dependency Rule"**—inner circle code should not depend on outer circle code. As long as you follow this principle, you can design an architecture that best suits your project's scale and your team's practices.

The following table shows architectural design strategies for different project phases. The key factor for splitting layers is when technical details (such as a specific database or framework) begin to couple with core business rules.

| Project Phase    | Architecture Strategy                                        | Notes                                                        |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Early Stage**  | **Domain** + **Application** + **Adapters** (simplified three-layer) | Simplified Dependency Injection (DI), Unit of Work (UoW) is embedded in the Repository, with a focus on business logic separation. |
| **Growth Phase** | **Domain** + **Application** + **Infrastructure** + **Controllers** (standard four-layer) | Clear responsibilities for each layer, complete dependency injection, and support for multiple external interfaces. |
| **Mature Phase** | Standard four layers + Aspect-Oriented Programming (AOP)     | Adds cross-cutting concerns like monitoring, logging, caching, and security to support large-scale deployment. |

---

### **6. Why is this not a production-grade template? What are its limitations?**

`py-clean-arch` is a practical example focused on demonstrating Clean Architecture principles in Python, not a template designed for production environments.

Its main limitations include:

- **Features**: It lacks production-grade features such as **OAuth2 authentication**, **structured logging**, **error recovery mechanisms**, and **API rate limiting**.
- **Performance**: It is not optimized for high-traffic scenarios, and its configurations are relatively simplified.
- **Testing**: ood unit and integration test coverage, but lacking end-to-end tests and load tests.

Therefore, if you want to use this for a production environment, you will need to enhance the relevant features and security mechanisms based on your actual requirements.