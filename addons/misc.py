#!/usr/bin/env python3.6

import datetime
from discord import Member, errors
from discord.ext import commands


class Misc:
    """
    Miscellaneous commands
    """

    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Pong!"""
        mtime = ctx.message.created_at
        currtime = datetime.datetime.now()
        latency = currtime - mtime
        ptime = str(latency.microseconds / 1000.0)
        return await ctx.send(":ping_pong:! Pong! Response time: {} ms".format(ptime))

    @commands.command(pass_context=True, aliases=['mc'])
    async def membercount(self, ctx):
        """Prints current member count"""
        return await ctx.send(str(self.bot.guild.name) + " currently has " + str(len(self.bot.guild.members)) + " members!")

    @commands.command()
    async def about(self, ctx):
        """About SchmuckBot."""
        return await ctx.send("https://github.com/PhazonicRidley/SchmuckBot")

    @commands.command(pass_context=True)
    async def sudo(self, ctx):
        """Gain temp mod powers, only need by Bot Developers to fix the bot/server"""

        user = ctx.message.author
        await ctx.message.delete()

        if self.bot.botdev_role in user.roles:
            await user.add_roles(self.bot.sudo_role)
            await ctx.send(":ambulance: **{} is now a HalfOP! Welcome to the twilight zone!**".format(user))
        else:
            return await ctx.send("You do not have permission to use this command!")

    @commands.command(pass_context=True)
    async def unsudo(self, ctx):
        """Remove temp mod powers, only needed by Bot Developers"""
        user = ctx.message.author
        await ctx.message.delete()

        if self.bot.botdev_role in user.roles:
            if self.bot.sudo_role in user.roles:
                await user.remove_roles(self.bot.sudo_role)
                await ctx.send("**Problem Solved! {} is no longer a HalfOP!**".format(user.name))
            else:
                ctx.send("You are not currently a HalfOP!")

        else:
            return await ctx.send("You do not have permission to use this command!")

    @commands.command(pass_context=True)
    async def togglechannel(self, ctx, channel):
        """Toggle access to some hidden channels"""

        user = ctx.message.author
        await ctx.message.delete()

        if channel == "nsfw":

            if self.bot.nsfw_role in user.roles:
                await user.remove_roles(self.bot.nsfw_role)
                await user.send("Access to NSFW channels revoked.")
            else:
                await user.add_roles(self.bot.nsfw_role)
                await user.send("Access to NSFW channels granted.")
        else:
            await user.send("{} is not a togglable channel.".format(channel))

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def clear(self, ctx, amount: int):
        """Clears a given amount of messages. (Mods only)"""

        channel = ctx.message.channel

        amount += 1
        if amount <= 0:
            await ctx.send("Please mention a valid amount of messages!")
            return

        try:
            await channel.purge(limit=amount)
            await ctx.send("🗑️ Cleared {} messages in this channel!".format(amount))
        except errors.Forbidden:
            await ctx.say("💢 I don't have permission to do this.")

    @commands.command()
    async def bean(self, ctx, member: Member=None, *, reason: str=""):
        """Ban a member. (Staff Only)"""
        if not member:
            await ctx.send("Please mention a user.")
            return
        if member == ctx.message.author:
            await ctx.send("You cannot ban yourself!")
            return
        elif ctx.me is member:
            await ctx.send("I am unable to ban myself to prevent stupid mistakes.\n"
                           "Please ban me by hand!")
            return
        else:
            await ctx.send("I've banned {}.".format(member))

    @commands.command()
    async def kicc(self, ctx, member: Member=None, *, reason: str=""):
        """Kick a member. (Staff Only)"""
        if not member:
            await ctx.send("Please mention a user.")
            return
        elif member is ctx.message.author:
            await ctx.send("You cannot kick yourself!")
            return
        elif ctx.me is member:
            await ctx.send("I am unable to kick myself to prevent stupid mistakes.\n"
                           "Please kick me by hand!")
            return
        await ctx.send("I've kicked {}.".format(member))

    @commands.command()
    async def moot(self, ctx, member: Member, *, reason=""):
        """Mutes a user. (Staff Only)"""

        if member is ctx.message.author:
            await ctx.send("You cannot mute yourself!")
            return
        elif ctx.me is member:
            await ctx.send("I can not mute myself!")
            return
        await ctx.send("{} can no longer speak!".format(member))

    @commands.command()
    async def unmoot(self, ctx, member: Member, *, reason=""):
        """Unmutes a user. (Staff Only)"""

        await ctx.send("{} is no longer muted!".format(member))

    @commands.command()
    async def warm(self, ctx, member: Member, *, reason=""):
        """
        Warn members. (Staff Only)
        - First warn : nothing happens, a simple warning
        - Second warn : muted until an the admin who issued the warning decides to unmute the user.
        - Third warn : kicked
        - Fourth warn : kicked
        - Fifth warn : banned
        """

        if member is ctx.message.author:
            await ctx.send("You cannot warn yourself!")
            return
        elif ctx.me is member:
            await ctx.send("I can not warn myself!")
            return
        await ctx.send("🚩 I've warned {}.".format(member))


def setup(bot):
    bot.add_cog(Misc(bot))
