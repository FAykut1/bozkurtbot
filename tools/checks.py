import os,json
from discord.ext import commands
import discord


def is_owner_check(ctx):
    _id = ctx.message.author.id
    if os.path.isfile("./veriler/kings.json"):
        with open("./veriler/kings.json","r") as fp:
            server = json.load(fp)
        return _id in server["Owners"]


def is_owner():
    return commands.check(is_owner_check)


def is_admin_check(ctx):
    if ctx.message.author.guild_permissions.administrator or is_owner_check(ctx):
        return True
    else:
        return False


def is_admin():
    return commands.check(is_admin_check)


def message_admin_check(user): ##ON_MESSAGE KOMUTLARINDA CHECK YAPMAK İÇİN
    if os.path.isfile("./veriler/kings.json"):
        with open("./veriler/kings.json","r") as fp:
            server = json.load(fp)
    if user.guild_permissions.administrator or user.id in server["Owners"]:
        return True
    else:
        return False