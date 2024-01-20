```ascii
+-----------------------+    -+
| Frameworks & Drivers  |     |
| (graphql, http)       |     |
+-----------------------+     |  entrypoints/graphql/
     |            ^           |  entrypoints/http/
     v            |           |
+-----------------------+     |
| Interface Adapters    |     |
+-----------------------+    -+
     |            ^
     v            |
+-----------------------+    -+
| Application Business  |     |
|   +-------------+     |     |
|   | Entity      |     |     |  usecases/
|   +-------------+     |     |
+-----------------------+    -+
     |            ^
     v            |
+-----------------------+    -+
| Interface Adapters    |     |
+-----------------------+     |
     |            ^           |
     v            |           |  repositories/relational_db/
+-----------------------+     |  repositories/nosql/
| Frameworks & Drivers  |     |
| (database)            |     |
+-----------------------+    -+
```
