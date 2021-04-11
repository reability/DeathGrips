from aiohttp import web

class ItemController(web.View):
    async def post(self):
        body =  await self.request.post()
        print(body)

        result = []
        for i in body.get("items"):
            print(i)
            result.append({
                "id": i["id"],
                "title": i["title"],
                "date": i["date"],
                "url": i["url"]
            })

        for _ws in self.request.app['websockets']:
            await _ws.send_json({
                "items": result
            })

        return web.Response()