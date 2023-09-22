#!/bin/bash

mongod --replSet rs0 --bind_ip_all &

sleep 1;

mongosh --host localhost:27017 --eval '
    rs.initiate({
    _id: "rs0",
    members: [{ _id: 0, host: "localhost:27017" }]
    })
'
tail -f /dev/null