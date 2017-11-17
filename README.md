My Answer to DSI Coding Challenge
====================

This is my answer to the DSI Coding Challenge (https://github.com/afreeorange/dsi-coding-challenge). You may view a demo of it @ (http://54.215.208.202/webpage/).


Requirements
----------------------

Python 2.7
  - flask
  - flask-cors


API Services
------------

Run the API web services:

```
Python run_server.py
```

Supported APIs:

Get exact matching of `City_Name`:

```
GET /cities/<City_Name>
```

Get fuzzy matching with `City_Name`, `latitude`, `longitude`

```
GET /cities?like=<City_Name>&latitude=<latitude>&longitude=<longitude>
```


