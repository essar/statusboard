# StatusBoard

_A simple display board for Raspberry Pi_

---

## About

A StatusBoard consists of 8 lights (LEDs) that can be turned on or off to display the status of different properties.

StatusBoard can be embedded in other Python applications as a library or called using its RESTful API.

## Physical Board

Coming soon.

## REST API

A REST API allows individual status indicators to be turned on or off.

#### Running the API server

```
python -m board.api [--test] [--host] [--port]
 test: run the API in development mode (does not connect to a physical board)
 host: specify the host to listen on (default: 127.0.0.1)
 port: specify the port to listen on (default: 5000)
```