async def db_handler(app, handler):
    async def middleware(request):
        if request.path.startswith('/static/'):
            response = await handler(request)
            return response

        request.db = app.db
        response = await handler(request)
        return response
    return middleware