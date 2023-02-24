#!/usr/bin/env python3

"""
gitlab-webhook-telegram
"""

import asyncio
import logging

from aiohttp import web

import handlers
from classes.bot import Bot
from classes.context import Context

PUSH = "Push Hook"
TAG = "Tag Push Hook"
RELEASE = "Release Hook"
ISSUE = "Issue Hook"
CONFIDENTIAL_ISSUE = "Confidential Issue Hook"
NOTE = "Note Hook"
CONFIDENTIAL_NOTE = "Confidential Note Hook"
MR = "Merge Request Hook"
JOB = "Job Hook"
WIKI = "Wiki Page Hook"
PIPELINE = "Pipeline Hook"

HANDLERS = {
    PUSH: handlers.push_handler,
    TAG: handlers.tag_handler,
    RELEASE: handlers.release_handler,
    ISSUE: handlers.issue_handler,
    CONFIDENTIAL_ISSUE: handlers.issue_handler,
    NOTE: handlers.note_handler,
    CONFIDENTIAL_NOTE: handlers.note_handler,
    MR: handlers.merge_request_handler,
    JOB: handlers.job_event_handler,
    WIKI: handlers.wiki_event_handler,
    PIPELINE: handlers.pipeline_handler,
}


routes = web.RouteTableDef()


class App:
    """
    A class to run the app.
    Override init and run command
    """

    def __init__(self, context: Context, bot: Bot) -> None:
        self.context = context
        self.bot = bot

    @routes.post("/")
    async def handle_post(self, request: web.Request) -> None:
        token = request.headers["X-Gitlab-Token"]
        if self.context.is_authorized_project(token):
            type = request.headers["X-Gitlab-Event"]
            body = await request.json()
            if type in HANDLERS:
                if token in self.context.table and self.context.table[token]:
                    chats = [
                        {
                            "id": chat,
                            "verbosity": self.context.table[token]["users"][chat]["verbosity"],
                        }
                        for chat in self.context.table[token]["users"]
                        if chat in self.context.verified_chats
                    ]
                    await HANDLERS[type](body, self.bot, chats, token)
                    raise web.HTTPOk
                else:
                    logging.warning("No user has subscribed to this project.")
                    raise web.HTTPOk
            else:
                logging.error("No handler for the event " + type)
                raise web.HTTPNotImplemented
        else:
            logging.warning("Unauthorized Gitlab webhook : token not in config.json")
            raise web.HTTPForbidden

    async def run_web_server(self) -> None:
        app = web.Application()
        app.add_routes([web.post("/", self.handle_post)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(
            runner=runner,
            host=self.context.config.get("address", "0.0.0.0"),
            port=self.context.config.get("port", 8080),
        )
        await site.start()

    async def run(self) -> None:
        """
        run is called when the app starts
        """
        logging.info(
            f"Starting gitlab-webhook-telegram app on http://localhost:{self.context.config.get('port', 8080)}"
        )
        await self.run_web_server()
        while True:
            await asyncio.sleep(15)
