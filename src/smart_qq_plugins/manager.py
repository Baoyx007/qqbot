# coding: utf-8
from random import randint
import re
from smart_qq_bot.handler import (
    list_handlers,
    list_active_handlers,
    activate,
    inactivate,
)
from smart_qq_bot.logger import logger
from smart_qq_bot.messages import GroupMsg, PrivateMsg,DiscussMsg
from smart_qq_bot.signals import on_all_message, on_bot_inited

cmd_hello = re.compile(r"!hello")
cmd_list_plugin = re.compile(r"!list_plugin")
cmd_inactivate = re.compile(r"!inactivate \{(.*?)\}")
cmd_activate = re.compile(r"!activate \{(.*?)\}")


def do_activate(text):
    result = re.findall(cmd_activate, text)
    if result:
        activate(result[0])
        return "Plugin [%s] activated successfully" % result[0]


def do_inactivate(text):
    re.findall(cmd_inactivate, text)
    result = re.findall(cmd_inactivate, text)
    if result:
        inactivate(result[0])
        return "Plugin [%s] inactivated successfully" % result[0]


def do_hello(text):
    if re.match(cmd_hello, text):
        return "鹅是 SB!"

def do_reminder(text):
    if re.match(cmd_remaind,text):
        return         


def do_list_plugin(text):
    if re.match(cmd_list_plugin, text):
        return "All: %s\n\nActive: %s" % (
            str(list_handlers()), str(list_active_handlers())
        )


@on_bot_inited("PluginManager")
def manager_init(bot):
    logger.info("Plugin Manager is available now:)")


@on_all_message(name="PluginManger")
def hello_bot(msg, bot):
    """
    :type bot: smart_qq_bot.bot.QQBot
    :type msg: smart_qq_bot.messages.GroupMsg
    """
    msg_id = randint(1, 10000)

    group_handlers = (
        do_hello,
    )
    private_handlers = (
        do_hello,do_inactivate, do_activate, do_list_plugin
    )
    if isinstance(msg, GroupMsg):
        #logger.info("GroupMsg msg : " + msg)
        for handler in group_handlers:
            result = handler(msg.content)
            if result is not None:
                return bot.reply_msg(msg, result)
    elif isinstance(msg, PrivateMsg):
        logger.info(msg)
        for handler in private_handlers:
            result = handler(msg.content)
            if result is not None:
                return bot.reply_msg(msg, result)
    elif isinstance(msg, DiscussMsg):
        for handler in group_handlers:
            result = handler(msg.content)
            if result is not None:
                return bot.reply_msg(msg, result)
