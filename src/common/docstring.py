MAPPER_DOCSTRING = '''
Mapping Logic:

This documentation describes the conversion logic used across various mapper.py files in the project.
The purpose of these mappers is to convert between different data representations,
such as input data, data objects, and business logic models.

Advantages of placing conversion logic directly in models or data objects:
- Centralized Management: All conversion operations related to the data are in one place.
- Simplicity: Reduces code complexity by eliminating the need for additional converters or services.

Disadvantages:
- Coupling: Models or data objects now represent not just data structures but also a part of the conversion logic.
- Violation of Single Responsibility Principle: They now have multiple responsibilities, potentially making them harder to maintain.

Advantages of using mappers (converters):
- Separation of Concerns: Converters handle only the conversion, while models or data objects deal with data representation.
- Flexibility: Changes in business logic or data structure only require modifications in the converter, leaving models or data objects unaffected.

Disadvantages:
- Increased Complexity: Introduces the overhead of managing and maintaining additional converters or services.
'''
