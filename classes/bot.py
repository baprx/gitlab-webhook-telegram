#!/usr/bin/env python3

"""
gitlab-webhook-telegram
"""

import logging
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from classes.context import Context

MODE_ADD_PROJECT = 1
MODE_REMOVE_PROJECT = 2
MODE_CHANGE_VERBOSITY_1 = 3
MODE_CHANGE_VERBOSITY_2 = 4
MODE_NONE = 0

V = 0
VV = 1
VVV = 2
VVVV = 3

VERBOSITIES = [
    (
        V,
        (
            "Print all except issues descriptions, assignees, due dates, labels, commit"
            " messages and URLs and reduce commit messages to 1 line"
        ),
    ),
    (
        VV,
        (
            "Print all except issues descriptions, assignees, due dates and labels and"
            " reduce commit messages to 1 line"
        ),
    ),
    (
        VVV,
        "Print all but issues descriptions and reduce commit messages to 1 line",
    ),
    (
        VVVV,
        "Print all",
    ),
]


class Bot:
    """
    A wrapper for the telegram bot
    """

    def __init__(self, token: str, context: Context) -> None:
        self.token = token
        self.context = context
        self.application = Application.builder().token(self.token).build()
        self.application.add_handler(CommandHandler("start", self.start, block=False))
        self.application.add_handler(CommandHandler("addProject", self.add_project, block=False))
        self.application.add_handler(
            CommandHandler("removeProject", self.remove_project, block=False)
        )
        self.application.add_handler(
            CommandHandler("changeVerbosity", self.change_verbosity, block=False)
        )
        self.application.add_handler(
            CommandHandler("listProjects", self.list_projects, block=False)
        )
        self.application.add_handler(CommandHandler("help", self.help, block=False))
        self.application.add_handler(CallbackQueryHandler(self.button, block=False))
        self.application.add_handler(MessageHandler(filters.TEXT, self.message, block=False))
        self.bot = self.application.bot
        self.username = None

    async def run(self):
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        self.username = self.bot.username
        logging.info("Bot " + self.username + " grabbed. Let's go.")

    async def send_message(
        self, chat_id: int, message: str, markup: InlineKeyboardMarkup = None
    ) -> int:
        """
        Send a message to a chat ID, split long text in multiple messages
        """
        max_message_length = 4096
        if len(message) <= max_message_length:
            message = await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=markup,
                parse_mode="HTML",
            )
            return message.message_id
        parts = []
        while len(message) > 0:
            if len(message) > max_message_length:
                part = message[:max_message_length]
                first_lnbr = part.rfind("\n")
                if first_lnbr != -1:
                    parts.append(part[:first_lnbr])
                    message = message[first_lnbr:]
                else:
                    parts.append(part)
                    message = message[max_message_length:]
            else:
                parts.append(message)
                break
        for part in parts:
            message = await self.bot.send_message(
                chat_id=chat_id, text=part, reply_markup=markup, parse_mode="HTML"
            )
            time.sleep(0.25)
        return message.message_id

    async def start(self, update: Update, context: CallbackContext) -> None:
        """
        Defines the handler for /start command
        """
        chat_id = update.message.chat_id
        bot = context.bot
        self.username = context.bot.username
        await bot.send_message(
            chat_id=chat_id, text="Hi. I'm a simple bot triggered by GitLab webhooks."
        )
        if chat_id in self.context.verified_chats:
            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "Since your chat is already verified, send /help to see the"
                    " available commands."
                ),
            )
        elif not self.context.config["passphrase"]:
            self.context.verified_chats.append(chat_id)
            self.context.write_verified_chats()
            await bot.send_message(
                chat_id=chat_id,
                text=("Your chat is now verified, send /help to see the available" " commands."),
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "First things first : you need to verify this chat. Just send me"
                    " the passphrase."
                ),
            )
            self.context.wait_for_verification = True

    async def add_project(self, update: Update, context: CallbackContext) -> None:
        """
        Defines the handler for /addProject command
        """
        chat_id = update.message.chat_id
        bot = context.bot
        if chat_id in self.context.verified_chats:
            self.context.button_mode = MODE_ADD_PROJECT
            inline_keyboard = []
            projects = [
                project
                for project in self.context.config["gitlab-projects"]
                if (
                    str(chat_id) in project["user-ids"]
                    and (
                        (
                            project["token"] in self.context.table
                            and chat_id not in self.context.table[project["token"]]
                        )
                        or project["token"] not in self.context.table
                    )
                )
            ]
            if not projects:
                await bot.send_message(chat_id=chat_id, text="No project to add.")
            for project in projects:
                inline_keyboard.append(
                    [InlineKeyboardButton(text=project["name"], callback_data=project["token"])]
                )
            replyKeyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await bot.send_message(
                chat_id=chat_id,
                reply_markup=replyKeyboard,
                text="Choose the project you want to add.",
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text="This chat is not verified, start with the command /start.",
            )

    async def change_verbosity(self, update: Update, context: CallbackContext) -> None:
        """
        Defines the handler for /changeVerbosity command
        """
        chat_id = update.message.chat_id
        bot = context.bot
        if chat_id in self.context.verified_chats:
            self.context.button_mode = MODE_CHANGE_VERBOSITY_1
            inline_keyboard = []
            projects = [
                project
                for project in self.context.config["gitlab-projects"]
                if (
                    project["token"] in self.context.table
                    and chat_id in self.context.table[project["token"]]["users"]
                )
            ]
            if not projects:
                await bot.send_message(chat_id=chat_id, text="No project configured on this chat.")
            for project in projects:
                inline_keyboard.append(
                    [InlineKeyboardButton(text=project["name"], callback_data=project["token"])]
                )
            replyKeyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await bot.send_message(
                chat_id=chat_id,
                reply_markup=replyKeyboard,
                text="Choose the project from which you want to change verbosity.",
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text="This chat is not verified, start with the command /start.",
            )

    async def remove_project(self, update: Update, context: CallbackContext) -> None:
        """
        Defines the handler for /removeProject command
        """
        chat_id = update.message.chat_id
        bot = context.bot
        if chat_id in self.context.verified_chats:
            self.context.button_mode = MODE_REMOVE_PROJECT
            inline_keyboard = []
            projects = [
                project
                for project in self.context.config["gitlab-projects"]
                if (
                    project["token"] in self.context.table
                    and chat_id in self.context.table[project["token"]]["users"]
                )
            ]
            if not projects:
                await bot.send_message(chat_id=chat_id, text="No project to remove.")
            for project in projects:
                inline_keyboard.append(
                    [InlineKeyboardButton(text=project["name"], callback_data=project["token"])]
                )
            replyKeyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await bot.send_message(
                chat_id=chat_id,
                reply_markup=replyKeyboard,
                text="Choose the project you want to remove.",
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text="This chat is not verified, start with the command /start.",
            )

    async def button(self, update: Update, context: CallbackContext) -> None:
        """
        Defines the handler for a click on button
        """
        query = update.callback_query
        bot = context.bot
        if self.context.button_mode == MODE_ADD_PROJECT:
            token = query.data
            chat_id = query.message.chat_id
            if token in self.context.table and chat_id in self.context.table[token]["users"]:
                await bot.edit_message_text(
                    text="Project was already there. Changing nothing.",
                    chat_id=chat_id,
                    message_id=query.message.message_id,
                )
            else:
                if token not in self.context.table:
                    self.context.table[token] = {"users": {chat_id: {}}}
                elif chat_id not in self.context.table[token]["users"]:
                    self.context.table[token]["users"][chat_id] = {}
                self.context.table[token]["users"][chat_id]["verbosity"] = VVVV
                self.context.write_table()
                await bot.edit_message_text(
                    text="The project was successfully added.",
                    chat_id=chat_id,
                    message_id=query.message.message_id,
                )
            self.context.button_mode = MODE_NONE
        elif self.context.button_mode == MODE_REMOVE_PROJECT:
            chat_id = query.message.chat_id
            token = query.data
            if token not in self.context.table or chat_id not in self.context.table[token]["users"]:
                await bot.edit_message_text(
                    text="Project was not there. Changing nothing.", chat_id=chat_id
                )
            else:
                del self.context.table[token]["users"][chat_id]
                self.context.write_table()
                await bot.edit_message_text(
                    text="The project was successfully removed.",
                    chat_id=chat_id,
                    message_id=query.message.message_id,
                )
        elif self.context.button_mode == MODE_CHANGE_VERBOSITY_1:
            chat_id = query.message.chat_id
            self.context.button_mode = MODE_CHANGE_VERBOSITY_2
            self.context.selected_project = query.data
            inline_keyboard = []
            for i, verbosity in enumerate(VERBOSITIES):
                inline_keyboard.append(
                    [InlineKeyboardButton(text=str(i) + ":" + verbosity[1], callback_data=i + 1)]
                )
            replyKeyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            message_verbosities = "Verbosities : \n"
            for verb in VERBOSITIES:
                message_verbosities += "- " + str(verb[0]) + " : " + verb[1] + "\n"
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=query.message.message_id,
                reply_markup=replyKeyboard,
                text=message_verbosities + "\nChoose the new verbosity.",
            )
        elif self.context.button_mode == MODE_CHANGE_VERBOSITY_2:
            chat_id = query.message.chat_id
            self.context.button_mode = MODE_NONE
            verbosity = int(query.data) - 1
            self.context.table[self.context.selected_project][chat_id]["verbosity"] = verbosity
            self.context.write_table()
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=query.message.message_id,
                text="The verbosity of the project has been changed.",
            )
            self.context.selected_project = None
        else:
            pass

    async def message(self, update: Update, context: CallbackContext) -> None:
        """
        The handler in case a simple message is posted
        """
        bot = context.bot
        if self.context.wait_for_verification:
            if update.message.text == self.context.config["passphrase"]:
                self.context.verified_chats.append(update.message.chat_id)
                self.context.write_verified_chats()
                await bot.send_message(
                    chat_id=update.message.chat_id,
                    text=(
                        "Thank you, your user ID is now verified. Send /help to see the"
                        " available commands."
                    ),
                )
                self.context.wait_for_verification = False
            else:
                await bot.send_message(
                    chat_id=update.message.chat_id,
                    text="The passphrase is incorrect. Still waiting for verification.",
                )

    async def help(self, update: Update, context: CallbackContext) -> None:
        """
        Defines the handler for /help command
        """
        bot = context.bot
        message = "Project gitlab-webhook-telegram v1.0.0\n"
        message += "You can use the following commands : \n\n"
        message += "/listProjects : list tracked projects in this chat\n"
        message += "/addProject : add a project in this chat\n"
        message += "/removeProject : remove a project from this chat\n"
        message += "/changeVerbosity : change the level of information of a chat\n"
        message += "/help : display this message"
        await bot.send_message(chat_id=update.message.chat_id, text=message)

    async def list_projects(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        bot = context.bot
        projects = [
            project
            for project in self.context.config["gitlab-projects"]
            if (
                project["token"] in self.context.table
                and chat_id in self.context.table[project["token"]].get("users", [])
            )
        ]
        message = "Projects : \n"
        if not projects:
            message += "There is no project"
        for id, project in enumerate(projects):
            message += (
                f'{id+1} - <b>{project["name"]}</b> (Verbosity:'
                f' {self.context.table[project["token"]]["users"][chat_id]["verbosity"]})\n'
            )
        await bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
