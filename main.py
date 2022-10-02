#!env python
"""Простой echo-скрипт """
import sys
import click
import aiohttp.web
from loguru import logger

LOGLEVELS = {1: "ERROR", 2: "INFO", 3: "DEBUG"}


async def echo(request):
    logger.debug(request)
    return aiohttp.web.Response(text=f"Hello {request.match_info['text']}!")


async def health(request):
    """Запрос проб"""
    logger.debug(request)
    return aiohttp.web.json_response({"status": "UP"})


@click.command(help="Простой HTTP-сервер для тестирования")
@click.option("-p", "--port", default=8080, type=int)
@click.option("-c", "--context-path", default="/", type=str)
@click.option("-v", "--verbose", type=int, count=True)
def main(port, context_path, verbose):
    logger.remove()
    routes = []
    if verbose:
        logger.add(sys.stderr, level=LOGLEVELS.get(verbose, "CRITICAL"))
    if not context_path.startswith("/"):
        logger.critical(f"Context path должен начинаться с /")
        sys.exit()
    if not context_path.endswith("/"):
        context_path += "/"
    if context_path != "/":
        routes += [
            aiohttp.web.get("/health/liveness", health),
            aiohttp.web.get("/health/readiness", health),
        ]
    routes += [
        aiohttp.web.get(context_path + "health/liveness", health),
        aiohttp.web.get(context_path + "health/readiness", health),
        aiohttp.web.get(context_path + "{text}", echo)
    ]
    logger.debug(routes)
    logger.info(f"Сервис запущен на порту {port}, context {context_path}")
    app = aiohttp.web.Application()
    app.add_routes(routes)
    aiohttp.web.run_app(app, port=port)


if __name__ == "__main__":
    main(auto_envvar_prefix="TELEPRESENCE")
