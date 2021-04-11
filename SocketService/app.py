import asyncio
from aiohttp import web
from middlewares import db_handler
from motor import motor_asyncio as ma

from controller import WebSocket
from restHandler import ItemController

HOST="0.0.0.0"
PORT=8000
SECRET_KEY="ASS"
MONGO_HOST="mongodb://127.0.0.1:27017"
MONGO_DB_NAME="test"

routes = [
    ('GET', '/ws',      WebSocket, 'service'),
    ('POST', '/item',   ItemController,     'Item'),
]

async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')


async def shutdown(server, app, handler):

    server.close()
    await server.wait_closed()
    app.client.close()  # database connection close
    await app.shutdown()
    await handler.finish_connections(10.0)
    await app.cleanup()


async def init(loop):
    app = web.Application(loop=loop, middlewares=[
    db_handler,
    ])

    setup_websokets(app)
    setup_mongo(app)

    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    app.on_shutdown.append(on_shutdown)
    handler = app.make_handler()
    serv_generator = loop.create_server(handler, HOST, PORT)
    
    return serv_generator, handler, app

def setup_websokets(app):
    sockets = []
    app['websockets'] = sockets

def setup_mongo(app):
    app.client = ma.AsyncIOMotorClient(MONGO_HOST)
    app.db = app.client[MONGO_DB_NAME]


loop = asyncio.get_event_loop()
serv_generator, handler, app = loop.run_until_complete(init(loop))
serv = loop.run_until_complete(serv_generator)
print('start server %s' % str(serv.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    print(' Stop server begin')
finally:
    loop.run_until_complete(shutdown(serv, app, handler))
    loop.close()
print('Stop server end')