  
from aiohttp import web
from aiohttp import WSMsgType

class WebSocket(web.View):
    async def get(self):

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.text:
                if msg.data == 'close':
                    await ws.close()
            elif msg == WSMsgType.error:
                print('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)