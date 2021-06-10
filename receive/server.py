import logging
import asyncio
from aiohttp import web

logger = logging.getLogger(__name__)


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
            return_value.set_result(await receiver(request))
            shutdown.set_result(True)
            logger.info("Sending response")
            return web.Response(text="Received.")

        app.add_routes(routes)

        async def await_shutdown(server):
            await shutdown
            await server.cleanup()
            return await return_value

        async def run_server():
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, host, port)
            await site.start()
            logger.info("Started HTTP server.")

            return await_shutdown(runner)

        return run_server

        logger.info("decorated")
    return decorator
