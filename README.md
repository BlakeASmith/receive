# Receive

`receive` is a python library for hosting temporary web servers and receiving values from their route handlers via futures. 

## Install

### Stable Release

```
pip install receive
```

### Latest Features

```
pip install git+https://github.com/BlakeASmith/receive
```

## Usage

### Handle a GET request

First, define a route handler as follows:
```python
import receive

@receive.get_request(route="/callback", port=5000)
async def get_query_param_from_request(req):
    return req.query["code"]
```

The `req` parameter is an [aiohttp.web.Request](https://docs.aiohttp.org/en/stable/web_reference.html) object. In this example
we return the `code` query parameter from the request. 

Now we can start a temporary web server, and get our return value from the first request that comes in.

```python
import asyncio

async def main():
    future = await get_query_param_from_request()
    code = await future
    print(code)
    
    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main)
```

The `get_query_param_from_request` function will start a web server in the background and return a `asyncio.Future` object providing access to the 
return value from the handler. `get_query_param_from_request` will return immediately, and invoking
`await` on the returned future will block until a `GET 0.0.0.0:5000/callback` request hits the server. At that time the future will be completed with the 
value returned from the request handler and the 
server will be shutdown.


## Tests

Run the unit tests using pytest

```
poetry install
poetry run pytest
```
