#!/bin/bash

PORT=${MONGO_PORT:-27017}

mongod --replSet rs0 --port "$PORT" --bind_ip_all &

sleep 1

mongosh --host "localhost:$PORT" --eval "
    rs.initiate({
    _id: \"rs0\",
    members: [{ _id: 0, host: \"localhost:$PORT\" }]
    })
"

tail -f /dev/null
