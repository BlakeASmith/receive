import asyncio
from aiohttp import web


def get_request(route, host=None, port=None, loop=None):
    if port is None:
        port = 8080
    if host is None:
        host = "0.0.0.0"
    if loop is None:
        loop = asyncio.get_event_loop()

    def decorator(receiver):
        app = web.Application()

        return_value = asyncio.Future()
        shutdown = asyncio.Future()

        routes = web.RouteTableDef()

        @routes.get(route)
        async def handler(request):
            try:
                return_value.set_result(await receiver(request))
                await (await shutdown)()
            except Exception as e:
                return_value.set_exception(e)
                raise e

        app.add_routes(routes)

        async def run_server():
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, host, port)
            await site.start()

            shutdown.set_result(runner.cleanup)

            return return_value

        return run_server
    return decorator
