from aiohttp import web

class ItemController(web.View):
    async def post(self):
        body =  await self.request.post()

        for _ws in self.request.app['websockets']:
            await _ws.send_json(body)

        return web.Response()