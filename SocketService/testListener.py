import aiohttp
import asyncio

async def main():
    session = aiohttp.ClientSession()
    print("StaRTED")
    async with session.ws_connect('http://134.209.248.84:8000/ws') as ws:
        print("Started")
        async for msg in ws:
            print(ws)
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close cmd':
                    await ws.close()
                    break
                else:
                    print(msg.data)
                    #await ws.send_str(msg.data + '/answer')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
    print("End")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())