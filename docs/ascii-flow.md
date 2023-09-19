```ascii
+-----------------------+    ^
| Frameworks & Drivers  |    |
| (graphql, http)       |    |
+-----------------------+    |
     |            ^          | deliveries/graphql/, http/
     v            |          |
+-----------------------+    |
| Interface Adapters    |    |
+-----------------------+    v
     |            ^
     v            |
+-----------------------+    ^
| Application Business  |    |
|   +-------------+     |    |
|   | Entity      |     |    |  usecases/
|   +-------------+     |    |
+-----------------------+    v
     |            ^
     v            |
+-----------------------+    ^
| Interface Adapters    |    |
+-----------------------+    |
     |            ^          |
     v            |          | repositories/relational_db/, nosql/
+-----------------------+    |
| Frameworks & Drivers  |    |
| (database)            |    |
+-----------------------+    v
```

